"""Module to generate markdown files using OpenAI API."""
import os
from typing import Optional, Dict
from openai import OpenAI
from dotenv import load_dotenv
from prompts import get_markdown_generation_prompt, get_example_markdown
import time

# Load environment variables
load_dotenv()


class MarkdownGenerator:
    """Generate SEO-optimized markdown files using OpenAI API."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4"):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable.")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = model or os.getenv('OPENAI_MODEL', 'gpt-4')
        self.rate_limit_delay = float(os.getenv('RATE_LIMIT_DELAY', '1'))
    
    def generate_markdown(
        self,
        game_title: str,
        game_slug: str,
        game_url: str,
        game_category: str,
        game_context: str,
        company_name: str,
        domain_name: str,
        current_date: str,
        genre: Optional[str] = None
    ) -> str:
        """Generate markdown content for a game."""
        
        # Determine genre from category if not provided
        if not genre:
            genre_mapping = {
                'racing': 'Racing',
                'running': 'Running',
                'puzzle': 'Puzzle',
                'shooting': 'Shooting',
                'simulator': 'Simulator',
                'sports': 'Sports',
                'skill': 'Skill',
                'stickman': 'Stickman'
            }
            genre = genre_mapping.get(game_category.lower(), 'Arcade')
        
        prompt = get_markdown_generation_prompt(
            game_title=game_title,
            game_slug=game_slug,
            game_url=game_url,
            game_category=game_category,
            game_context=game_context,
            company_name=company_name,
            domain_name=domain_name,
            current_date=current_date,
            genre=genre
        )
        
        # Get example markdown for reference
        example = get_example_markdown()
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an experienced SEO content writer who writes natural, human-like game descriptions. Write conversationally, avoid AI patterns and buzzwords, and make content that sounds like a real person wrote it. Always respond with valid markdown content only, without any explanations or additional text outside the markdown file itself."
                    },
                    {
                        "role": "user",
                        "content": f"Example markdown format:\n\n{example}\n\n\nNow generate the markdown for the following game:\n\n{prompt}"
                    }
                ],
                temperature=0.8,
                max_tokens=2500
            )
            
            markdown_content = response.choices[0].message.content.strip()
            
            # Clean up the response - remove any markdown code blocks if present
            if markdown_content.startswith("```"):
                # Remove markdown code block markers
                lines = markdown_content.split('\n')
                if lines[0].startswith("```"):
                    lines = lines[1:]
                if lines[-1].strip() == "```":
                    lines = lines[:-1]
                markdown_content = '\n'.join(lines)
            
            time.sleep(self.rate_limit_delay)
            return markdown_content
            
        except Exception as e:
            raise Exception(f"Error generating markdown: {e}")
    
    def generate_markdown_batch(
        self,
        games: list,
        game_contexts: Dict[str, Dict[str, Optional[str]]],
        company_name: str,
        domain_name: str,
        current_date: str
    ) -> Dict[str, str]:
        """Generate markdown for multiple games."""
        results = {}
        
        for game in games:
            try:
                context = game_contexts.get(game.slug, {})
                combined_context = context.get('combined_context', '')
                
                markdown = self.generate_markdown(
                    game_title=game.title,
                    game_slug=game.slug,
                    game_url=game.url,
                    game_category=game.category,
                    game_context=combined_context,
                    company_name=company_name,
                    domain_name=domain_name,
                    current_date=current_date
                )
                
                results[game.slug] = markdown
                
            except Exception as e:
                print(f"Error generating markdown for {game.title}: {e}")
                results[game.slug] = None
        
        return results
