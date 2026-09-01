import os

from dotenv import load_dotenv
from groq import Groq


load_dotenv()


class LLMService:

    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError(
                "GROQ_API_KEY is not set in the environment."
            )

        self.client = Groq(api_key=api_key)

        self.model = "openai/gpt-oss-120b"

    def generate(
        self,
        question: str,
        context: str,
    ) -> str:

        prompt = f"""
You are DocuMind, a document question answering assistant.

Answer the user's question using only the provided context.

If the answer cannot be found in the context, say:
"I could not find the answer in the provided document."

Context:
{context}

Question:
{question}

Answer:
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0,
        )

        return response.choices[0].message.content.strip()


llm_service = LLMService()