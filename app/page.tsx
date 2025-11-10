import Link from 'next/link';
import { getAllGames, getCategories } from '@/lib/games';
import { GameGrid } from './components/game-grid';

export default function Home() {
  const games = getAllGames();
  const categories = getCategories();

  return (
    <div className='min-h-screen bg-zinc-50 dark:bg-black'>
      {/* Header */}
      <header className='sticky top-0 z-50 border-b border-zinc-200 bg-white/80 backdrop-blur-sm dark:border-zinc-800 dark:bg-black/80'>
        <div className='mx-auto max-w-7xl px-4 sm:px-6 lg:px-8'>
          <div className='flex h-16 items-center justify-between'>
            <Link href='/' className='text-2xl font-bold text-zinc-900 dark:text-zinc-50'>
              UndrPlay
            </Link>
            <nav className='hidden gap-6 md:flex'>
              {categories.map((category) => (
                <Link
                  key={category}
                  href={`#${category}`}
                  className='text-sm font-medium capitalize text-zinc-600 transition-colors hover:text-zinc-900 dark:text-zinc-400 dark:hover:text-zinc-50'>
                  {category}
                </Link>
              ))}
            </nav>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className='mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8'>
        <div className='text-center'>
          <h1 className='text-5xl font-bold tracking-tight text-zinc-900 dark:text-zinc-50 sm:text-6xl'>
            Play Free Games Online
          </h1>
          <p className='mt-6 text-lg leading-8 text-zinc-600 dark:text-zinc-400'>
            Discover and play thousands of free games in your browser
          </p>
        </div>
      </section>

      {/* Games Grid with Search and Filters */}
      <GameGrid games={games} categories={categories} />

      {/* Footer */}
      <footer className='border-t border-zinc-200 bg-white dark:border-zinc-800 dark:bg-black'>
        <div className='mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8'>
          <p className='text-center text-sm text-zinc-600 dark:text-zinc-400'>
            © {new Date().getFullYear()} UndrPlay. All rights reserved.
          </p>
        </div>
      </footer>
    </div>
  );
}
