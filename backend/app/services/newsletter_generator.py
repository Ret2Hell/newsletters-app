import os

import groq


class NewsletterGenerator:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set")
        self.client = groq.Client(api_key=api_key)
        self.model = os.getenv("GROQ_MODEL", "gemma2-9b-it")

    def generate_content(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a newsletter content generator. Create professional and engaging newsletter content.",
                    },
                    {
                        "role": "user",
                        "content": f"Generate a newsletter based on this prompt: {prompt}",
                    },
                ],
                temperature=0.7,
                max_tokens=1024,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error generating content: {str(e)}"
