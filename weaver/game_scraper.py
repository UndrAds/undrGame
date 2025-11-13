"""Module to scrape game descriptions from poki.com and crazygames.com."""
import requests
from bs4 import BeautifulSoup
from typing import Optional, Dict
import time


class GameScraper:
    """Scraper to fetch game information from various game websites."""
    
    def __init__(self, rate_limit_delay: float = 1.0):
        self.rate_limit_delay = rate_limit_delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def fetch_poki(self, game_slug: str) -> Optional[Dict[str, str]]:
        """Fetch game description from Poki.com using direct URL format."""
        try:
            # Direct Poki game URL: https://poki.com/en/g/{game-slug}
            game_url = f"https://poki.com/en/g/{game_slug}"
            
            response = self.session.get(game_url, timeout=10)
            
            # Skip if game not found (404 or other errors)
            if response.status_code != 200:
                return None
            
            soup = BeautifulSoup(response.content, 'html.parser')
            description = None
            
            # Try meta description first
            meta_desc = soup.find('meta', {'name': 'description'})
            if meta_desc and meta_desc.get('content'):
                description = meta_desc.get('content')
            
            # Try Open Graph description
            if not description:
                og_desc = soup.find('meta', {'property': 'og:description'})
                if og_desc and og_desc.get('content'):
                    description = og_desc.get('content')
            
            # Try to find description in page content
            if not description:
                # Look for description in various possible locations
                desc_selectors = [
                    'meta[name="description"]',
                    'meta[property="og:description"]',
                    '[class*="description"]',
                    'p[class*="description"]',
                    '.game-description',
                    '.description'
                ]
                
                for selector in desc_selectors:
                    desc_elem = soup.select_one(selector)
                    if desc_elem:
                        if selector.startswith('meta'):
                            description = desc_elem.get('content', '')
                        else:
                            description = desc_elem.get_text(strip=True)
                        if description and len(description) > 50:  # Ensure it's substantial
                            break
            
            if description:
                time.sleep(self.rate_limit_delay)
                return {
                    'source': 'poki.com',
                    'description': description.strip(),
                    'url': game_url
                }
            
            time.sleep(self.rate_limit_delay)
            return None
            
        except Exception as e:
            # Silently skip if game not found or error occurs
            return None
    
    def fetch_crazygames(self, game_slug: str) -> Optional[Dict[str, str]]:
        """Fetch game description from CrazyGames.com using direct URL format."""
        try:
            # Direct CrazyGames game URL: https://www.crazygames.com/game/{game-slug}
            game_url = f"https://www.crazygames.com/game/{game_slug}"
            
            response = self.session.get(game_url, timeout=10)
            
            # Skip if game not found (404 or other errors)
            if response.status_code != 200:
                return None
            
            soup = BeautifulSoup(response.content, 'html.parser')
            description = None
            
            # Try meta description first
            meta_desc = soup.find('meta', {'name': 'description'})
            if meta_desc and meta_desc.get('content'):
                description = meta_desc.get('content')
            
            # Try Open Graph description
            if not description:
                og_desc = soup.find('meta', {'property': 'og:description'})
                if og_desc and og_desc.get('content'):
                    description = og_desc.get('content')
            
            # Try to find description in page content
            if not description:
                desc_selectors = [
                    'meta[name="description"]',
                    'meta[property="og:description"]',
                    '.game-description',
                    '.description',
                    '[class*="description"]',
                    'p[class*="about"]',
                    '[class*="summary"]'
                ]
                
                for selector in desc_selectors:
                    desc_elem = soup.select_one(selector)
                    if desc_elem:
                        if selector.startswith('meta'):
                            description = desc_elem.get('content', '')
                        else:
                            description = desc_elem.get_text(strip=True)
                        if description and len(description) > 50:
                            break
            
            if description:
                time.sleep(self.rate_limit_delay)
                return {
                    'source': 'crazygames.com',
                    'description': description.strip(),
                    'url': game_url
                }
            
            time.sleep(self.rate_limit_delay)
            return None
            
        except Exception as e:
            # Silently skip if game not found or error occurs
            return None
    
    def get_game_context(self, game_slug: str) -> Dict[str, Optional[str]]:
        """Get game context from multiple sources using direct URLs."""
        context = {
            'poki_description': None,
            'crazygames_description': None,
            'combined_context': None
        }
        
        # Try Poki first using direct URL: https://poki.com/en/g/{game-slug}
        poki_data = self.fetch_poki(game_slug)
        if poki_data:
            context['poki_description'] = poki_data['description']
        
        # Try CrazyGames using direct URL: https://www.crazygames.com/game/{game-slug}
        crazygames_data = self.fetch_crazygames(game_slug)
        if crazygames_data:
            context['crazygames_description'] = crazygames_data['description']
        
        # Combine contexts
        descriptions = []
        if context['poki_description']:
            descriptions.append(f"Poki.com: {context['poki_description']}")
        if context['crazygames_description']:
            descriptions.append(f"CrazyGames.com: {context['crazygames_description']}")
        
        if descriptions:
            context['combined_context'] = "\n\n".join(descriptions)
        
        return context
