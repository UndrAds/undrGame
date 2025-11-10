import Link from 'next/link';
import { notFound } from 'next/navigation';
import { getGameBySlug, getAllGames } from '@/lib/games';

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
      </main>
    </div>
  );
}
