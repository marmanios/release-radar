# ai_models/o4_mini_openai.py

from openai import OpenAI
from prompts import generate_user_prompt, system_prompt
from dotenv import load_dotenv
from typing import Literal
import tiktoken
import os

load_dotenv()


class O4MiniByOpenAI:
    def __init__(self):
        self.encoding = tiktoken.get_encoding("o200k_base")  # Encoder for OpenAI models
        self.base_url = "https://api.openai.com/v1/chat/completions"

    def call_o4_api(
        self,
        data: str,
        reasoning_effort: Literal["low", "medium", "high"] = "low",
    ) -> str:
        """
        Makes an API call to OpenAI o4-mini and returns the response.

        Args:
            system_prompt (str): The instruction/system prompt
            data (dict): Dictionary of variables to format into the user message
            api_key (str | None): Optional custom API key

        Returns:
            str: o4-mini's response text
        """
        # Create the user message with the html data
        user_message = generate_user_prompt(data)

        # Create client
        client = OpenAI(api_key=os.getenv(key="OPENAI_APIKEY"))

        try:
            print("Making an API call to o4-mini with API key")

            completion = client.chat.completions.create(
                model="o4-mini-2025-04-16",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message},
                ],
                max_completion_tokens=12000, 
                temperature=1,
                reasoning_effort=reasoning_effort,
            )

            print("API call completed successfully")

            if completion.choices[0].message.content is None:
                raise ValueError("No content returned from OpenAI o4-mini")

            return completion.choices[0].message.content

        except Exception as e:
            print(f"Error in OpenAI o4-mini API call: {str(e)}")
            raise

    def count_tokens(self, prompt: str) -> int:
        """
        Counts the number of tokens in a prompt.

        Args:
            prompt (str): The prompt to count tokens for

        Returns:
            int: Estimated number of input tokens
        """
        num_tokens = len(self.encoding.encode(prompt))
        return num_tokens