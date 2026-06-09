import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()


class QAService:

    def __init__(self):
        genai.configure(
            api_key=os.getenv("GEMINI_API_KEY")
        )

        self.model = genai.GenerativeModel(
            "gemini-2.5-flash"
        )

    def generate_answer(
        self,
        question,
        context_chunks
    ):
        context = "\n\n".join(context_chunks)

        prompt = f"""
You are a helpful assistant.

Use the context to answer the question.

You may infer reasonable conclusions from the context,
but do not invent facts not supported by the context."

Context:
{context}

Question:
{question}
"""

        response = self.model.generate_content(
            prompt
        )

        return response.text