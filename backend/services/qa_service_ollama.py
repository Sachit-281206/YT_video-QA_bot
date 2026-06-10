import ollama


class QAService:

    def generate_answer(
        self,
        question,
        context_chunks
    ):

        context = "\n\n".join(
            context_chunks
        )

        prompt = f"""
You are answering questions about a YouTube video.

The following context was retrieved from the video's transcript.

Use the context to answer the question.

If asked about the video's topic, summarize the main subject discussed.

Context:
{context}

Question:
{question}
"""

        response = ollama.chat(
            model="hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return (
            response["message"]["content"]
        )