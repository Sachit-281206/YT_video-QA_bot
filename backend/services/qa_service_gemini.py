import os
from dotenv import load_dotenv
from google import genai

load_dotenv()


class QAService:

    def __init__(self):

        self.client = genai.Client(
            api_key=os.getenv(
                "GEMINI_API_KEY"
            )
        )

    def generate_answer(
        self,
        question,
        context_chunks
    ):

        context = "\n\n".join(
            context_chunks
        )

        prompt = f"""
You are a helpful assistant.

Use the context to answer the question.

You may infer reasonable conclusions from the context,
but do not invent facts not supported by the context.

Context:
{context}

Question:
{question}
"""

        response = (
            self.client.models
            .generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
        )

        return response.text