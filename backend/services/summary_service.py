import ollama


class SummaryService:

    def __init__(self):

        self.model = (
            "hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF"
        )

    def summarize_section(
        self,
        chunks
    ):

        context = "\n\n".join(
            chunks
        )

        prompt = f"""
You are summarizing a section of a YouTube video.

Summarize the following content in 3-5 concise bullet points.

Focus on:
- Main ideas
- Important concepts
- Key takeaways

Content:
{context}
"""

        response = ollama.chat(
            model=self.model,
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

    def summarize_video(
        self,
        chunks,
        section_size=5
    ):

        section_summaries = []

        # Create groups of chunks
        for i in range(
            0,
            len(chunks),
            section_size
        ):

            section_chunks = (
                chunks[
                    i:i + section_size
                ]
            )

            summary = (
                self.summarize_section(
                    section_chunks
                )
            )

            section_summaries.append(
                summary
            )

        combined_summaries = (
            "\n\n".join(
                section_summaries
            )
        )

        final_prompt = f"""
You are creating a final summary of a YouTube video.

The following are summaries of different sections of the video.

Create:

1. A short overview (2-3 paragraphs)

2. Key topics discussed

3. Main takeaways

Section Summaries:

{combined_summaries}
"""

        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": final_prompt
                }
            ]
        )

        return (
            response["message"]["content"]
        )