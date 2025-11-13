import { readFileSync, existsSync } from 'fs';
import { join } from 'path';

const POSTS_DIR = join(process.cwd(), 'games', 'posts');

/**
 * Get markdown content for a game by slug
 * Returns the content without frontmatter, or null if file doesn't exist
 */
export function getGameMarkdown(slug: string): string | null {
  try {
    const filePath = join(POSTS_DIR, `${slug}.md`);

    if (!existsSync(filePath)) {
      return null;
    }

    const fileContent = readFileSync(filePath, 'utf-8');

    // Remove frontmatter (content between --- markers)
    const frontmatterRegex = /^---\s*\n([\s\S]*?)\n---\s*\n/;
    const content = fileContent.replace(frontmatterRegex, '').trim();

    return content || null;
  } catch {
    return null;
  }
}

/**
 * Check if a markdown file exists for a game
 */
export function hasGameMarkdown(slug: string): boolean {
  const filePath = join(POSTS_DIR, `${slug}.md`);
  return existsSync(filePath);
}
