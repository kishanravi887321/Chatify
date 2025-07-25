import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from langchain_text_splitters import RecursiveCharacterTextSplitter

class VectorDBLogic:
    def __init__(self, raw_text,model_name="all-MiniLM-L6-v2"):
        
        self.model = SentenceTransformer(model_name)
        self.split_texts = self.load_and_split_text(raw_text)
        self.chunk_embeddings = self.model.encode(self.split_texts, show_progress_bar=True)

    def load_and_split_text(self,raw_text=None):
       
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=350, chunk_overlap=150)
        split_texts = text_splitter.split_text(raw_text)
        print(f"✅ Number of chunks: {len(split_texts)}")
        return split_texts

    def get_chunk(self, query):
        query_embedding = self.model.encode([query])[0]
        similarities = cosine_similarity([query_embedding], self.chunk_embeddings)[0]
        most_similar_index = np.argmax(similarities)
        return self.split_texts[most_similar_index]
    
    def get_unique_name(self,email,project_name):
        return f"{email}_{project_name}".replace(" ", "_").lower()
    #
        
    
