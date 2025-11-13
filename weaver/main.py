"""Main script to generate markdown files for games."""
import os
import sys
from pathlib import Path
from typing import List, Optional
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from datetime import datetime

from game_parser import (
    get_all_games,
    get_all_categories,
    get_games_by_slugs,
    filter_games_by_category,
    Game
)
from game_scraper import GameScraper
from markdown_generator import MarkdownGenerator

console = Console()


def get_user_inputs() -> dict:
    """Get user inputs for markdown generation."""
    console.print("\n[bold cyan]Weaver - Game Markdown Generator[/bold cyan]\n")
    
    # Get company information
    company_name = Prompt.ask(
        "[bold]Enter company name[/bold]",
        default="UndrPlay"
    )
    
    domain_name = Prompt.ask(
        "[bold]Enter domain name[/bold]",
        default="undrplay.com"
    )
    
    # Get current date
    current_date_str = Prompt.ask(
        "[bold]Enter current date (format: 1 March 2024 5:30 UTC)[/bold]",
        default=datetime.now().strftime("%d %B %Y %H:%M UTC")
    )
    
    # Get output directory
    output_dir = Prompt.ask(
        "[bold]Enter output directory path for markdown files[/bold]",
        default="./output"
    )
    
    # Ask about directory structure
    use_category_structure = Confirm.ask(
        "[bold]Organize output by category? (category_name/game_name.md)[/bold]",
        default=False
    )
    
    return {
        'company_name': company_name,
        'domain_name': domain_name,
        'current_date': current_date_str,
        'output_dir': output_dir,
        'use_category_structure': use_category_structure
    }


def display_games_table(games: List[Game], title: str = "Available Games"):
    """Display games in a table."""
    table = Table(title=title)
    table.add_column("Slug", style="cyan")
    table.add_column("Title", style="magenta")
    table.add_column("Category", style="green")
    table.add_column("URL", style="blue")
    
    for game in games:
        table.add_row(
            game.slug,
            game.title,
            game.category,
            game.url[:50] + "..." if len(game.url) > 50 else game.url
        )
    
    console.print(table)


def select_games(output_dir: Path, use_category_structure: bool) -> List[Game]:
    """Allow user to select games to generate markdown for."""
    all_games = get_all_games()
    all_categories = get_all_categories()
    
    if not all_games:
        console.print("[bold red]No games found![/bold red]")
        sys.exit(1)
    
    console.print(f"\n[bold]Found {len(all_games)} games in {len(all_categories)} categories[/bold]\n")
    
    # Check existing files and show statistics
    status = analyze_generation_status(all_games, output_dir, use_category_structure)
    
    if status['generated'] > 0:
        console.print(f"\n[bold yellow]Generation Status:[/bold yellow]")
        console.print(f"  [green]Already generated: {status['generated']} games[/green]")
        console.print(f"  [yellow]Remaining: {status['remaining']} games[/yellow]")
        console.print(f"  [cyan]Total: {status['total']} games[/cyan]\n")
        
        if status['remaining'] == 0:
            console.print("[bold green]All games have been generated![/bold green]")
            if not Confirm.ask("[bold]Do you want to regenerate any games?[/bold]"):
                sys.exit(0)
    
    # Ask user how they want to select games
    if status['remaining'] > 0:
        selection_mode = Prompt.ask(
            "[bold]How would you like to select games?[/bold]",
            choices=["remaining", "all", "category", "specific", "limit"],
            default="remaining"
        )
    else:
        selection_mode = Prompt.ask(
            "[bold]How would you like to select games?[/bold]",
            choices=["all", "category", "specific", "limit"],
            default="limit"
        )
    
    selected_games = []
    
    if selection_mode == "remaining":
        selected_games = status['remaining_games']
        console.print(f"\n[bold]Selected {len(selected_games)} remaining games[/bold]")
    
    elif selection_mode == "all":
        selected_games = all_games
    
    elif selection_mode == "category":
        console.print(f"\nAvailable categories: {', '.join(all_categories)}")
        category_input = Prompt.ask(
            "[bold]Enter category name(s) separated by commas[/bold]"
        )
        categories = [cat.strip() for cat in category_input.split(',')]
        selected_games = filter_games_by_category(all_games, categories)
    
    elif selection_mode == "specific":
        display_games_table(all_games[:20], "Games (showing first 20)")
        slugs_input = Prompt.ask(
            "[bold]Enter game slug(s) separated by commas[/bold]"
        )
        slugs = [slug.strip() for slug in slugs_input.split(',')]
        selected_games = get_games_by_slugs(slugs)
    
    elif selection_mode == "limit":
        limit = int(Prompt.ask(
            "[bold]Enter maximum number of games to generate[/bold]",
            default="10"
        ))
        display_games_table(all_games[:limit], f"First {limit} Games")
        
        if Confirm.ask(f"\n[bold]Generate markdown for first {limit} games?[/bold]"):
            selected_games = all_games[:limit]
        else:
            # Let user select specific games from the list
            slugs_input = Prompt.ask(
                "[bold]Enter game slug(s) separated by commas[/bold]"
            )
            slugs = [slug.strip() for slug in slugs_input.split(',')]
            selected_games = get_games_by_slugs(slugs)
    
    if not selected_games:
        console.print("[bold red]No games selected![/bold red]")
        sys.exit(1)
    
    # Check if any selected games already exist
    existing_files = get_existing_markdown_files(output_dir, use_category_structure)
    existing_selected = [g for g in selected_games if g.slug in existing_files]
    new_selected = [g for g in selected_games if g.slug not in existing_files]
    
    if existing_selected:
        console.print(f"\n[bold yellow]Warning: {len(existing_selected)} selected games already have markdown files[/bold yellow]")
        console.print(f"[bold green]New games to generate: {len(new_selected)}[/bold green]")
    
    console.print(f"\n[bold green]Selected {len(selected_games)} games[/bold green]\n")
    return selected_games


def get_existing_markdown_files(output_dir: Path, use_category_structure: bool = False) -> set:
    """Get set of existing markdown file slugs."""
    existing_files = set()
    
    if not output_dir.exists():
        return existing_files
    
    if use_category_structure:
        # Check category subdirectories
        for category_dir in output_dir.iterdir():
            if category_dir.is_dir():
                for md_file in category_dir.glob("*.md"):
                    existing_files.add(md_file.stem)
    else:
        # Check root directory
        for md_file in output_dir.glob("*.md"):
            existing_files.add(md_file.stem)
    
    return existing_files


def get_markdown_file_path(output_dir: Path, game: Game, use_category_structure: bool = False) -> Path:
    """Get the file path for a game's markdown file."""
    if use_category_structure:
        category_dir = output_dir / game.category
        category_dir.mkdir(parents=True, exist_ok=True)
        return category_dir / f"{game.slug}.md"
    else:
        output_dir.mkdir(parents=True, exist_ok=True)
        return output_dir / f"{game.slug}.md"


def save_markdown_file(output_dir: Path, game: Game, markdown_content: str, 
                       use_category_structure: bool = False, append_mode: bool = False):
    """Save markdown content to file."""
    output_file = get_markdown_file_path(output_dir, game, use_category_structure)
    
    if append_mode and output_file.exists():
        # Append mode - add to existing file
        with open(output_file, 'a', encoding='utf-8') as f:
            f.write("\n\n---\n\n")
            f.write(markdown_content)
    else:
        # Write mode - overwrite existing file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
    
    return output_file


def analyze_generation_status(games: List[Game], output_dir: Path, 
                             use_category_structure: bool = False) -> dict:
    """Analyze which games have been generated and which are remaining."""
    existing_files = get_existing_markdown_files(output_dir, use_category_structure)
    
    generated_games = []
    remaining_games = []
    
    for game in games:
        if game.slug in existing_files:
            generated_games.append(game)
        else:
            remaining_games.append(game)
    
    return {
        'total': len(games),
        'generated': len(generated_games),
        'remaining': len(remaining_games),
        'generated_games': generated_games,
        'remaining_games': remaining_games
    }


def main():
    """Main function."""
    try:
        # Get user inputs
        user_inputs = get_user_inputs()
        
        # Create output directory
        output_dir = Path(user_inputs['output_dir']).resolve()
        use_category_structure = user_inputs.get('use_category_structure', False)
        
        # Select games (this will also show generation status)
        selected_games = select_games(output_dir, use_category_structure)
        
        # Check for existing files in selected games
        existing_files = get_existing_markdown_files(output_dir, use_category_structure)
        existing_selected = [g for g in selected_games if g.slug in existing_files]
        
        # Ask about append/rewrite mode if there are existing files
        append_mode = False
        if existing_selected:
            console.print(f"\n[bold yellow]Found {len(existing_selected)} existing markdown files in selection[/bold yellow]")
            append_mode = Confirm.ask(
                "[bold]Append to existing files? (No = overwrite)[/bold]",
                default=False
            )
        
        # Display selected games
        display_games_table(selected_games, "Selected Games")
        
        if not Confirm.ask("\n[bold]Proceed with markdown generation?[/bold]"):
            console.print("[yellow]Cancelled.[/yellow]")
            sys.exit(0)
        
        # Initialize scraper and generator
        console.print("\n[bold]Initializing scraper and generator...[/bold]")
        scraper = GameScraper(rate_limit_delay=1.0)
        generator = MarkdownGenerator()
        
        # Scrape game contexts
        console.print("\n[bold]Fetching game contexts from external sources...[/bold]")
        game_contexts = {}
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Scraping games...", total=len(selected_games))
            
            for game in selected_games:
                progress.update(task, description=f"Scraping {game.title}...")
                context = scraper.get_game_context(game.slug)
                game_contexts[game.slug] = context
                progress.advance(task)
        
        # Generate markdown files
        console.print("\n[bold]Generating markdown files...[/bold]")
        generated_files = []
        failed_games = []
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Generating markdown...", total=len(selected_games))
            
            for game in selected_games:
                try:
                    progress.update(task, description=f"Generating {game.title}...")
                    
                    context = game_contexts.get(game.slug, {})
                    combined_context = context.get('combined_context', '')
                    
                    markdown = generator.generate_markdown(
                        game_title=game.title,
                        game_slug=game.slug,
                        game_url=game.url,
                        game_category=game.category,
                        game_context=combined_context,
                        company_name=user_inputs['company_name'],
                        domain_name=user_inputs['domain_name'],
                        current_date=user_inputs['current_date']
                    )
                    
                    # Save markdown file
                    output_file = get_markdown_file_path(output_dir, game, use_category_structure)
                    file_existed = output_file.exists()
                    
                    save_markdown_file(
                        output_dir, 
                        game, 
                        markdown,
                        use_category_structure=use_category_structure,
                        append_mode=append_mode
                    )
                    generated_files.append(output_file)
                    
                    mode_text = "Appended to" if (append_mode and file_existed) else "Generated"
                    console.print(f"[green]✓[/green] {mode_text}: {game.title} -> {output_file}")
                    
                except Exception as e:
                    console.print(f"[red]✗[/red] Failed: {game.title} - {e}")
                    failed_games.append(game.title)
                
                progress.advance(task)
        
        # Summary
        console.print(f"\n[bold green]Generation complete![/bold green]")
        console.print(f"[green]Successfully generated: {len(generated_files)} files[/green]")
        console.print(f"[green]Output directory: {output_dir}[/green]")
        
        if failed_games:
            console.print(f"\n[red]Failed games: {len(failed_games)}[/red]")
            for game in failed_games:
                console.print(f"  - {game}")
        
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted by user.[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[bold red]Error: {e}[/bold red]")
        sys.exit(1)


if __name__ == "__main__":
    main()
