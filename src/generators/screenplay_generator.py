import openai
from typing import Dict, List
from src.prompts.system_prompts import get_boxing_film_prompt
from config.settings import settings

class ScreenplayGenerator:
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model
    
    def generate_screenplay(self, prompt: str) -> str:
        """
        Generate a full screenplay from a single prompt.
        """
        system_prompt = get_boxing_film_prompt(prompt)
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=4000,
        )
        
        return response.choices[0].message.content
    
    def refine_screenplay(self, screenplay: str, feedback: str) -> str:
        """
        Refine screenplay based on user feedback.
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert screenwriter. Refine and improve the given screenplay based on feedback."
                },
                {
                    "role": "user",
                    "content": f"Original Screenplay:\n{screenplay}\n\nFeedback:\n{feedback}"
                }
            ],
            temperature=0.7,
            max_tokens=4000,
        )
        
        return response.choices[0].message.content
