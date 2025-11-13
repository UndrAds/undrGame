"""Module to parse game JSON files from the games directory."""
import json
import os
from pathlib import Path
from typing import List, Dict, Optional


class Game:
    """Game data model."""
    def __init__(self, slug: str, title: str, url: str, img: str, category: str):
        self.slug = slug
        self.title = title
        self.url = url
        self.img = img
        self.category = category

    def __repr__(self):
        return f"Game(slug='{self.slug}', title='{self.title}', category='{self.category}')"


def get_games_directory() -> Path:
    """Get the games directory path (parent directory of weaver)."""
    current_file = Path(__file__).resolve()
    project_root = current_file.parent.parent
    return project_root / "games"


def load_games_from_category(category: str) -> List[Game]:
    """Load games from a specific category JSON file."""
    games_dir = get_games_directory()
    json_file = games_dir / f"{category}.json"
    
    if not json_file.exists():
        return []
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            games_data = json.load(f)
        
        games = []
        for game_data in games_data:
            game = Game(
                slug=game_data.get('slug', ''),
                title=game_data.get('title', ''),
                url=game_data.get('url', ''),
                img=game_data.get('img', ''),
                category=category
            )
            games.append(game)
        
        return games
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading games from {json_file}: {e}")
        return []


def get_all_categories() -> List[str]:
    """Get all category names from JSON files in games directory."""
    games_dir = get_games_directory()
    
    if not games_dir.exists():
        return []
    
    categories = []
    for json_file in games_dir.glob("*.json"):
        categories.append(json_file.stem)
    
    return sorted(categories)


def get_all_games() -> List[Game]:
    """Get all games from all category JSON files."""
    categories = get_all_categories()
    all_games = []
    
    for category in categories:
        games = load_games_from_category(category)
        all_games.extend(games)
    
    return all_games


def get_games_by_slugs(slugs: List[str]) -> List[Game]:
    """Get games by their slugs."""
    all_games = get_all_games()
    return [game for game in all_games if game.slug in slugs]


def filter_games_by_category(games: List[Game], categories: Optional[List[str]] = None) -> List[Game]:
    """Filter games by category."""
    if not categories:
        return games
    
    return [game for game in games if game.category in categories]
