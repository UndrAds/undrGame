"""Prompt templates for markdown generation."""
from typing import Dict, Optional
from datetime import datetime


def get_markdown_generation_prompt(
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
    """Generate the prompt for markdown generation."""
    
    # Generate keywords based on game title
    base_keywords = [
        game_title,
        f"{game_title} Online",
        f"{game_title} unblocked",
        f"{game_title} game",
    ]
    
    # Add variations
    title_words = game_title.split()
    if len(title_words) > 1:
        # Add shorter variations
        base_keywords.extend([
            " ".join(title_words[:-1]) if len(title_words) > 2 else title_words[0],
            title_words[0] if len(title_words) > 1 else game_title,
        ])
    
    keywords_list = ", ".join([f'"{kw}"' for kw in base_keywords])
    
    # Determine genre if not provided
    if not genre:
        genre_mapping = {
            'racing': ['Racing'],
            'running': ['Running', 'Action'],
            'puzzle': ['Puzzle'],
            'shooting': ['Shooting', 'Action'],
            'simulator': ['Simulator'],
            'sports': ['Sports'],
            'skill': ['Skill', 'Arcade'],
            'stickman': ['Stickman', 'Action']
        }
        genre = genre_mapping.get(game_category.lower(), ['Arcade'])
        if isinstance(genre, list):
            genre = genre[0]
    
    prompt = f"""You are an experienced SEO content writer who writes natural, human-like game descriptions that rank well on Google. Generate a comprehensive, SEO-optimized markdown file for the game "{game_title}".

Game Information:
- Title: {game_title}
- Slug: {game_slug}
- URL: {game_url}
- Category: {game_category}
- Genre: {genre}

Game Context (from external sources):
{game_context if game_context else "No external context available. Use your knowledge of the game."}

Website Information:
- Website Name: {company_name}
- Domain: {domain_name}
- Current Date: {current_date}

IMPORTANT RULES:
1. {company_name} is the WEBSITE NAME where the game is hosted, NOT the developer. Do NOT say "{company_name} developed this game" or "{company_name} created this game". Instead, mention {company_name} naturally as the platform/website where players can access the game. For example: "Play {game_title} on {company_name}" or "You can find {game_title} on {company_name} along with other great games."

2. Write like a REAL HUMAN, not an AI. Avoid:
   - Buzzwords like "revolutionary", "cutting-edge", "state-of-the-art", "game-changing", "next-level"
   - Overly enthusiastic marketing language
   - Repetitive phrases
   - Generic filler content
   - AI-sounding patterns

3. Write naturally and conversationally, as if you're explaining the game to a friend.

Requirements:
1. Create a frontmatter section with:
   - title: "{game_title} Unblocked - Online {genre} Game" (or similar, keep it natural)
   - description: A natural, SEO-optimized description (150-160 characters) that sounds human-written
   - keywords: A list of relevant keywords including: {keywords_list}
   - published_on: {current_date}
   - updated_on: {current_date}
   - rating: {{ value: 4.3, total_users: 234 }} (use realistic values)
   - genre: ["{genre}", "{game_category.capitalize()}"]

2. Write detailed content with UP TO 5 MAIN SECTIONS (use H2 headings):
   - Introduction: A natural opening paragraph (2-3 sentences) that hooks the reader naturally
   - Game Overview: 2-3 short paragraphs explaining what the game is about
   - Key Features: Detailed section with 3-5 features, each with H3 subheadings and 2-3 sentence descriptions
   - Gameplay Details: Section explaining how the game works, controls, mechanics (use lists or tables for controls)
   - Why Play This Game: A natural conclusion section explaining why someone should try it

3. Formatting Requirements:
   - Use SHORT PARAGRAPHS (2-4 sentences max)
   - Include BULLET POINTS or NUMBERED LISTS where appropriate
   - Use TABLES for controls/key bindings if applicable
   - Use H2 for main sections, H3 for subsections
   - Break up text with proper spacing
   - Make it scannable and easy to read

4. SEO Best Practices:
   - Use the game title naturally 3-5 times throughout (not forced)
   - Include relevant keywords naturally in context
   - Write for humans first, search engines second
   - Use natural language variations
   - Keep content valuable and informative
   - Target word count: 500-800 words

5. Writing Style:
   - Write in a conversational, friendly tone
   - Use simple, clear language
   - Avoid jargon and technical terms unless necessary
   - Be specific and concrete (avoid vague statements)
   - Include real details about gameplay
   - Sound like a real person wrote it, not a marketing bot

6. Content Quality:
   - Be accurate about the game features
   - Highlight what makes the game interesting or fun
   - Explain gameplay mechanics clearly
   - Mention {company_name} naturally as the website/platform (2-3 times max)
   - Do NOT mention {company_name} as the developer
   - Make it useful and informative for readers

Generate the complete markdown file following the exact format shown in the example. Write naturally, avoid AI patterns, and make it sound like a real person wrote it. Do not include any explanations or additional text outside the markdown file itself."""
    
    return prompt


def get_example_markdown() -> str:
    """Return example markdown format for reference."""
    return """---
title: 3D Moto Simulator 2 Unblocked - Online Racing Adventure Game
description: Experience adrenaline-pumping action with 3D Moto Simulator 2. Drive through stunning landscapes, perform daring stunts, and race against friends. Play now!
keywords: [3D Moto Simulator 2, 3D Moto Simulator 2 Online, 3D Moto Simulator 2 unblocked, 3D Moto Simulator 2 game, 3D Moto Simulator, 3D Moto Simulator Online, 3D Moto Simulator game, 3D Moto, 3D Moto online, 3D Moto game, 3D Moto unblocked, 3D Moto Simulator unblocked]
published_on: 1 March 2024 5:30 UTC
updated_on: 1 April 2024 5:30 UTC
rating: {
    value: 4.3,
    total_users: 234,
}
genre: ["Racing", "Simulator"]
---

If you enjoy motorcycle racing games, 3D Moto Simulator 2 is worth checking out. It's a straightforward racing game where you ride different bikes through various environments. The controls are simple, and you can perform basic stunts as you race around.

## Game Overview

3D Moto Simulator 2 lets you choose from several motorcycle types. You can pick street bikes, off-road bikes, or even a police motorcycle. Each bike handles differently, so you'll need to get used to how they feel when turning and accelerating.

The game has three main locations to race through. One is set in a desert city, another in a busy urban area, and the third in a wasteland setting. Each area has different terrain and obstacles, which keeps things interesting as you play.

## Key Features

### Multiple Bike Options

You can switch between different motorcycles during gameplay. Street bikes are faster but harder to control, while off-road bikes handle better on rough terrain. The police bike is fun to try, especially with the siren feature.

### Different Environments

The three locations each have their own feel. The desert city has wide open spaces, the urban area is more cramped with buildings, and the wasteland has challenging terrain. Switching between them helps keep the game from feeling repetitive.

### Stunt Mechanics

You can perform wheelies and bunny hops while riding. These don't really affect gameplay much, but they're fun to try. The physics feel decent, though the stunts are more for show than anything else.

### Simple Controls

The game uses basic keyboard controls that are easy to learn. You don't need to memorize complicated button combinations. This makes it accessible for casual players who just want to jump in and race.

## How to Play

The controls are straightforward:

| Action | Key |
|--------|-----|
| Drive | WASD |
| Change Bike | 1, 2, 3 |
| Handbrake | Space |
| Change View | C |
| Reset Game | R |
| Reset Bike | G |
| Police Lights | E |

Use WASD to move around. The handbrake helps with sharp turns. You can switch bikes mid-game if you want to try something different. The reset options are handy if you get stuck or flip your bike.

## Why Play This Game

3D Moto Simulator 2 works well if you want a simple racing game without much complexity. It's not trying to be a realistic simulator, which actually makes it more fun for quick sessions. The bike variety and different locations give you enough to explore without overwhelming you.

The game runs smoothly in most browsers, so you don't need powerful hardware. It's the kind of game you can play for a few minutes when you have some downtime. If you're looking for something more serious, this might not be for you. But if you want a casual racing experience, it's worth trying.

You can find 3D Moto Simulator 2 on various gaming websites. Just search for it and you should be able to play it directly in your browser without any downloads."""
