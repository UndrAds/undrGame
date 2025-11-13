import Link from 'next/link';
import { notFound } from 'next/navigation';
import { getGameBySlug, getAllGames } from '@/lib/games';
import { getGameMarkdown } from '@/lib/markdown';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

interface GamePageProps {
  params: Promise<{ slug: string }>;
}

export async function generateStaticParams() {
  const games = getAllGames();
  return games.map((game) => ({
    slug: game.slug,
  }));
}

export async function generateMetadata({ params }: GamePageProps) {
  const { slug } = await params;
  const game = getGameBySlug(slug);

  if (!game) {
    return {
      title: 'Game Not Found',
    };
  }

  return {
    title: `${game.title} - UndrPlay`,
    description: `Play ${game.title} for free on UndrPlay`,
  };
}

export default async function GamePage({ params }: GamePageProps) {
  const { slug } = await params;
  const game = getGameBySlug(slug);

  if (!game) {
    notFound();
  }

  const markdownContent = getGameMarkdown(slug);

  return (
    <div className='min-h-screen bg-zinc-900'>
      {/* Header */}
      <header className='sticky top-0 z-50 border-b border-zinc-800 bg-zinc-900/80 backdrop-blur-sm'>
        <div className='mx-auto max-w-7xl px-4 sm:px-6 lg:px-8'>
          <div className='flex h-16 items-center justify-between'>
            <Link
              href='/'
              className='text-xl font-bold text-zinc-50 transition-colors hover:text-zinc-300'>
              ← Back to Games
            </Link>
            <h1 className='text-lg font-semibold text-zinc-50'>{game.title}</h1>
            <div className='w-32' /> {/* Spacer for centering */}
          </div>
        </div>
      </header>

      {/* Game Container */}
      <main className='mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8'>
        <div className='relative aspect-video w-full overflow-hidden rounded-lg bg-zinc-950 shadow-2xl'>
          <iframe
            src={game.url}
            className='h-full w-full border-0'
            title={game.title}
            allow='fullscreen; gamepad; microphone; camera'
            allowFullScreen
          />
        </div>

        {/* Game Info */}
        <div className='mt-6 text-center'>
          <h2 className='text-2xl font-bold text-zinc-50'>{game.title}</h2>
          <p className='mt-2 text-sm text-zinc-400 capitalize'>{game.category}</p>
        </div>

        {/* Game Description */}
        {markdownContent && (
          <div className='mt-8 rounded-lg bg-zinc-800/50 p-6 lg:p-8'>
            <div className='prose prose-invert prose-zinc max-w-none prose-headings:text-zinc-50 prose-h1:text-3xl prose-h1:font-bold prose-h2:text-2xl prose-h2:font-semibold prose-h2:mt-8 prose-h2:mb-4 prose-h3:text-xl prose-h3:font-semibold prose-h3:mt-6 prose-h3:mb-3 prose-p:text-zinc-300 prose-p:leading-7 prose-p:my-4 prose-strong:text-zinc-50 prose-strong:font-semibold prose-a:text-blue-400 prose-a:no-underline hover:prose-a:text-blue-300 prose-ul:text-zinc-300 prose-ul:my-4 prose-li:my-2 prose-table:text-zinc-300 prose-th:text-zinc-50 prose-th:font-semibold prose-th:border-zinc-700 prose-td:border-zinc-700 prose-code:text-zinc-200 prose-code:bg-zinc-900/50 prose-code:px-1 prose-code:py-0.5 prose-code:rounded prose-pre:bg-zinc-950 prose-pre:border prose-pre:border-zinc-800'>
              <ReactMarkdown remarkPlugins={[remarkGfm]}>{markdownContent}</ReactMarkdown>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
