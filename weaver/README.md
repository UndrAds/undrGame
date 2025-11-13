# Weaver

A Python subproject that weaves together SEO-optimized markdown files for games using OpenAI's LLM API. Weaver fetches game descriptions from external sources (Poki.com, CrazyGames.com) and creates comprehensive, SEO-friendly markdown files for each game.

## Features

- 🎮 Read games from JSON files in the parent `games/` directory
- 🔍 Scrape game descriptions from Poki.com and CrazyGames.com
- 🤖 Generate SEO-optimized markdown using OpenAI's GPT-4
- 📝 Create markdown files in the exact format required
- 🎯 Select games by category, specific slugs, or limit
- ⚡ Batch processing with progress tracking
- 🔒 Rate limiting to avoid API throttling

## Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Internet connection (for scraping game descriptions)

## Setup

1. **Create virtual environment:**
```bash
cd weaver
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables:**
Create a `.env` file in the `weaver` directory:
```bash
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4
RATE_LIMIT_DELAY=1
```

## Usage

1. **Activate virtual environment:**
```bash
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. **Run the generator:**
```bash
python main.py
```

3. **Follow the interactive prompts:**
   - Enter company name (default: UndrPlay)
   - Enter domain name (default: undrplay.com)
   - Enter current date (default: current date)
   - Enter output directory path
   - Select games (all, category, specific, or limit)
   - Confirm generation

## Game Selection Modes

### 1. All Games
Generate markdown for all games in all categories.

### 2. Category
Select games by category (e.g., racing, puzzle, simulator).

### 3. Specific
Enter specific game slugs separated by commas.

### 4. Limit (Default)
Generate markdown for the first N games, or select specific games from the list.

## Output Format

The generated markdown files follow this structure:

```markdown
---
title: Game Title Unblocked - Online Genre Adventure Game
description: SEO-optimized description (150-160 characters)
keywords: [keyword1, keyword2, ...]
published_on: 1 March 2024 5:30 UTC
updated_on: 1 April 2024 5:30 UTC
rating: {
    value: 4.3,
    total_users: 234,
}
genre: ["Genre", "Category"]
---

# Game content with SEO-optimized sections
```

## Project Structure

```
weaver/
├── main.py                 # Main entry point
├── game_parser.py          # Parse game JSON files
├── game_scraper.py         # Scrape game descriptions
├── markdown_generator.py   # Generate markdown using OpenAI
├── prompts.py              # Prompt templates
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create this)
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## Configuration

### Environment Variables

- `OPENAI_API_KEY` (required): Your OpenAI API key
- `OPENAI_MODEL` (optional): Model to use (default: gpt-4)
- `RATE_LIMIT_DELAY` (optional): Delay between API calls in seconds (default: 1)

### Rate Limiting

The generator includes rate limiting to avoid API throttling:
- Default delay: 1 second between requests
- Configurable via `RATE_LIMIT_DELAY` environment variable

## Error Handling

- If a game description cannot be scraped, the generator will continue with available context
- If markdown generation fails for a game, it will be skipped and reported in the summary
- All errors are logged to the console

## Notes

- The generator uses OpenAI's GPT-4 model by default (configurable)
- Game contexts are fetched from Poki.com and CrazyGames.com
- Generated markdown files are saved to the specified output directory
- The generator respects rate limits to avoid API throttling

## Troubleshooting

### OpenAI API Key Error
Make sure you have set the `OPENAI_API_KEY` environment variable in your `.env` file.

### Scraping Errors
If scraping fails for a game, the generator will continue with limited context. This is normal and the LLM will generate content based on available information.

### Rate Limiting
If you encounter rate limiting issues, increase the `RATE_LIMIT_DELAY` value in your `.env` file.

## License

This project is part of the undrPlay main project.
