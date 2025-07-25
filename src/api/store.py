import os
import requests
import re
from dotenv import load_dotenv

# Flexible imports to handle different deployment scenarios

from ..vectordb.connectvdb import upsert_to_vectordb, get_relevant_chunks_from_vectordb
from ..db.utils import ExistUser
from ..db.connect import SessionLocal

load_dotenv()

class ChatifyService:

    @staticmethod
    def handle_query(api_key: str, query: str):
       
        if not api_key:
            return {"message": "API key is required."}, 400

        # Retrieve relevant chunks
        relevant_chunks = get_relevant_chunks_from_vectordb(query, api_key)
        if not relevant_chunks:
            return {"message": "No relevant chunks found."}, 404

        # Ask Gemini
        response, status = ChatifyService.ask_gemini(query, relevant_chunks[0])
        return response, status

    @staticmethod
   
    def ask_gemini(query: str, relevant_chunk: str):
        gemini_api_key = os.getenv("GOOGLE_API_KEY")
        if not gemini_api_key:
            return {"message": "Server configuration error: Missing Gemini API key."}, 500

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_api_key}"

        prompt = f"""
        Context:
        {relevant_chunk}

        Question:
        {query +" make the answer as concise as possible. if the user asks long question, try to answer long . And if short then provied in the 20 tokens or more then "}
        """

        payload = {
            "contents": [
                {
                    "parts": [{"text": prompt.strip()}]
                }
            ]
        }

        try:
            response = requests.post(
                url,
                headers={"Content-Type": "application/json"},
                json=payload
            )
        except requests.exceptions.RequestException:
            return {"message": "Service unavailable: Failed to connect to Gemini API."}, 503

        if response.status_code != 200:
            return {
                "message": "Gemini API request failed.",
                "status_code": response.status_code,
                "error": response.text
            }, response.status_code

        try:
            data = response.json()
            answer = data['candidates'][0]['content']['parts'][0]['text']

            # 🧹 Clean up response: remove "Based on the provided text..." if exists
            if answer.lower().startswith("based on") or "provided text" in answer.lower():
                # Keep only the relevant clean part
                cleaned_answer = answer.split(":", 1)[-1].strip()
            else:
                cleaned_answer = answer.strip()

            return {
                "answer": cleaned_answer,
                "context_used": relevant_chunk
            }, 200

        except (KeyError, IndexError, ValueError) as e:
            return {
                "message": "Failed to process Gemini API response.",
                "error": str(e),
                "raw_response": response.text
            }, 500


    @staticmethod
    def upsert_text_and_generate_api_key(raw_text: str, email: str):
        if not ExistUser(email).check_user_exists(db_session=SessionLocal()):
            print
            return {"message": "User already exists."}, 400
       
        api_key = upsert_to_vectordb(raw_text, email)
        print('api_key', api_key)
        if not api_key:
            return {"message": "Failed to store data in vector DB."}, 500
        return {"api_key": api_key}, 201
