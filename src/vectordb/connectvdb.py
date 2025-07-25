from pinecone import Pinecone, ServerlessSpec, describe_index
from dotenv import load_dotenv
import os
from sentence_transformers import SentenceTransformer
from ..services.script import SecretKeyGenerator
from .logics import VectorDBLogic

load_dotenv()   

# 📦 Initialize Pinecone client
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# 🏷️ Index name
index_name = os.getenv("PINECONE_INDEX_NAME")


if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=384, 
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region=os.getenv("PINECONE_REGION", "us-east-1")  
        )
    )
    print("✅ Index created:", index_name)
else:
    print("✅ Using existing index:", index_name)

index = pc.Index(index_name)
description = pc.describe_index(index_name)
print("Metric used:", description['metric'])


def upsert_to_vectordb(raw_text, email ):
    api_key=SecretKeyGenerator().get_secret_key()
    try:
        # Initialize VectorDBLogic with the raw text
        vector_db_logic = VectorDBLogic(raw_text)
        
        # Prepare data for upsert
        upsert_data = []
        for i, chunk in enumerate(vector_db_logic.split_texts):
            unique_name = vector_db_logic.get_unique_name(email,"for_saksin")
            upsert_data.append({
                "id": f"{unique_name}_{i}",
                "values": vector_db_logic.model.encode([chunk])[0].tolist(),
                "metadata": {
                    "email": email,
                   
                    "chunk_index": i,
                    "chunk_text": chunk,
                    "api_key": api_key
                }
            })

        # Upsert the data to Pinecone
        index.upsert(vectors=upsert_data)

        print(f"✅ Upserted {len(upsert_data)} chunks to Pinecone.")

        # ✅ Return the api_key if successful
        return api_key

    except Exception as e:
        print(f"❌ Failed to upsert data: {e}")
        return None


from fastapi import HTTPException


def get_relevant_chunks_from_vectordb(query, api_key, top_k=12):
    # Load the model
    model = SentenceTransformer("all-MiniLM-L6-v2")
    
    # Encode the query into embedding
    query_embedding = model.encode(query).tolist()

    # First, check if API key exists in metadata
    key_check_result = index.query(
        vector=query_embedding,
        top_k=1,  # Just need one match to confirm existence
        include_metadata=True,
        filter={"email": {"$eq": api_key}}
    )
    
    if not key_check_result.get("matches"):  # ❌ No match = API key not found
        raise HTTPException(
            status_code=401,
            detail="❌ Wrong email address: No matching metadata found."
        )

    # ✅ API key valid — Now query for top_k relevant chunks
    result = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True,
        filter={"email": {"$eq": api_key}}
    )

    matches = result.get("matches", [])
    
    if not matches:
        raise HTTPException(
            status_code=404,
            detail="⚠️ No relevant chunks found for this query."
        )

    # Return matched text chunks
    return [match["metadata"]["chunk_text"] for match in matches]
