import logging

from app.config import settings
from groq import Client, GroqError

logger = logging.getLogger(__name__)


class NewsletterGenerator:
    """
    Service for generating newsletter content using Groq AI.

    This class handles the connection to Groq's API and provides
    methods to generate newsletter content based on user prompts.
    """

    def __init__(self):
        """
        Initialize the newsletter generator service.

        Establishes a connection to the Groq API using the configured
        API key and sets up the model specified in application settings.

        Raises:
            Exception: If initialization fails (invalid API key, network issues, etc.)
        """
        try:
            self.client = Client(api_key=settings.GROQ_API_KEY)
            self.model = settings.GROQ_MODEL
            logger.info(f"Newsletter generator initialized with model: {self.model}")
        except Exception as e:
            logger.error(f"Failed to initialize newsletter generator: {e}")
            raise

    def generate_content(self, prompt: str) -> str:
        """
        Generate newsletter content based on a user prompt.

        Uses the Groq API to create newsletter content with a predefined
        system prompt that guides the AI to produce professional and engaging content.

        Args:
            prompt: User input describing the desired newsletter content

        Returns:
            str: Generated newsletter content

        Raises:
            GroqError: If the Groq API returns an error (rate limits, invalid requests, etc.)
            Exception: For other errors during content generation
        """
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
