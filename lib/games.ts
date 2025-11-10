import type { Game, GameWithCategory } from '@/types/game';
import { readFileSync, readdirSync } from 'fs';
import { join } from 'path';

const GAMES_DIR = join(process.cwd(), 'games');

/**
 * Get all game categories (JSON file names)
 */
export function getCategories(): string[] {
  try {
    const files = readdirSync(GAMES_DIR);
    return files
      .filter((file: string) => file.endsWith('.json'))
      .map((file: string) => file.replace('.json', ''));
  } catch {
    return [];
  }
}

/**
 * Load games from a specific category
 */
export function getGamesByCategory(category: string): Game[] {
  try {
    const filePath = join(GAMES_DIR, `${category}.json`);
    const fileContent = readFileSync(filePath, 'utf-8');
    return JSON.parse(fileContent) as Game[];
  } catch {
    return [];
  }
}

/**
 * Get all games with their categories
 */
export function getAllGames(): GameWithCategory[] {
  const categories = getCategories();
  const allGames: GameWithCategory[] = [];

  for (const category of categories) {
    const games = getGamesByCategory(category);
    for (const game of games) {
      allGames.push({
        ...game,
        category,
      });
    }
  }

  return allGames;
}

/**
 * Get a game by slug
 */
export function getGameBySlug(slug: string): GameWithCategory | null {
  const allGames = getAllGames();
  return allGames.find((game) => game.slug === slug) || null;
}
