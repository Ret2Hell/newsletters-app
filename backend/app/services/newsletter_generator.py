import logging

from app.config import settings
from groq import Client, GroqError

logger = logging.getLogger(__name__)


class NewsletterGenerator:
    def __init__(self):
        try:
            self.client = Client(api_key=settings.GROQ_API_KEY)
            self.model = settings.GROQ_MODEL
            logger.info(f"Newsletter generator initialized with model: {self.model}")
        except Exception as e:
            logger.error(f"Failed to initialize newsletter generator: {e}")
            raise

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
        except GroqError as e:
            logger.error(f"Groq API error: {e}")
            raise
        except Exception as e:
            logger.error(f"Failed to generate content: {e}")
            raise
