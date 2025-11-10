'use client';

import Link from 'next/link';
import Image from 'next/image';
import { useState } from 'react';
import type { GameWithCategory } from '@/types/game';

interface GameGridProps {
  games: GameWithCategory[];
  categories: string[];
}

export function GameGrid({ games, categories }: GameGridProps) {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');

  // Filter games
  const filteredGames = games.filter((game) => {
    const matchesSearch =
      game.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      game.slug.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCategory = selectedCategory === 'all' || game.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  return (
    <>
      {/* Search and Filter Bar */}
      <div className='mx-auto max-w-7xl px-4 pb-8 sm:px-6 lg:px-8'>
        <div className='flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between'>
          {/* Search */}
          <div className='relative flex-1 max-w-md'>
            <input
              type='text'
              placeholder='Search games...'
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className='w-full rounded-lg border border-zinc-300 bg-white px-4 py-2 pl-10 text-sm text-zinc-900 placeholder-zinc-500 focus:border-zinc-500 focus:outline-none focus:ring-2 focus:ring-zinc-500 dark:border-zinc-700 dark:bg-zinc-800 dark:text-zinc-50 dark:placeholder-zinc-400'
            />
            <svg
              className='absolute left-3 top-1/2 h-5 w-5 -translate-y-1/2 text-zinc-400'
              fill='none'
              stroke='currentColor'
              viewBox='0 0 24 24'>
              <path
                strokeLinecap='round'
                strokeLinejoin='round'
                strokeWidth={2}
                d='M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z'
              />
            </svg>
          </div>

          {/* Category Filter */}
          <div className='flex gap-2 overflow-x-auto pb-2 sm:pb-0'>
            <button
              onClick={() => setSelectedCategory('all')}
              className={`whitespace-nowrap rounded-lg px-4 py-2 text-sm font-medium transition-colors ${
                selectedCategory === 'all'
                  ? 'bg-zinc-900 text-white dark:bg-zinc-50 dark:text-zinc-900'
                  : 'bg-white text-zinc-700 hover:bg-zinc-100 dark:bg-zinc-800 dark:text-zinc-300 dark:hover:bg-zinc-700'
              }`}>
              All
            </button>
            {categories.map((category) => (
              <button
                key={category}
                onClick={() => setSelectedCategory(category)}
                className={`whitespace-nowrap rounded-lg px-4 py-2 text-sm font-medium capitalize transition-colors ${
                  selectedCategory === category
                    ? 'bg-zinc-900 text-white dark:bg-zinc-50 dark:text-zinc-900'
                    : 'bg-white text-zinc-700 hover:bg-zinc-100 dark:bg-zinc-800 dark:text-zinc-300 dark:hover:bg-zinc-700'
                }`}>
                {category}
              </button>
            ))}
          </div>
        </div>

        {/* Results Count */}
        <p className='mt-4 text-sm text-zinc-600 dark:text-zinc-400'>
          {filteredGames.length} {filteredGames.length === 1 ? 'game' : 'games'} found
        </p>
      </div>

      {/* Games Grid */}
      {filteredGames.length > 0 ? (
        <div className='mx-auto max-w-7xl px-4 pb-16 sm:px-6 lg:px-8'>
          <div className='grid grid-cols-2 gap-4 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6'>
            {filteredGames.map((game) => (
              <Link
                key={game.slug}
                href={`/game/${game.slug}`}
                className='group relative overflow-hidden rounded-lg bg-white shadow-sm transition-all hover:scale-105 hover:shadow-lg dark:bg-zinc-800'>
                <div className='aspect-square w-full overflow-hidden bg-zinc-100 dark:bg-zinc-900'>
                  <Image
                    src={game.img}
                    alt={game.title}
                    fill
                    className='object-cover transition-transform group-hover:scale-110'
                    sizes='(max-width: 640px) 50vw, (max-width: 1024px) 33vw, (max-width: 1280px) 20vw, 16vw'
                  />
                </div>
                <div className='p-3'>
                  <h3 className='line-clamp-2 text-sm font-semibold text-zinc-900 dark:text-zinc-50'>
                    {game.title}
                  </h3>
                  <p className='mt-1 text-xs text-zinc-500 dark:text-zinc-400 capitalize'>
                    {game.category}
                  </p>
                </div>
              </Link>
            ))}
          </div>
        </div>
      ) : (
        <div className='mx-auto max-w-7xl px-4 pb-16 text-center sm:px-6 lg:px-8'>
          <p className='text-lg text-zinc-600 dark:text-zinc-400'>No games found</p>
        </div>
      )}
    </>
  );
}
