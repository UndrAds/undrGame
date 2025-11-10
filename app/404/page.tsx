export default function NotFound() {
  return (
    <div className='flex min-h-screen items-center justify-center bg-zinc-50 dark:bg-black'>
      <div className='text-center'>
        <h1 className='text-6xl font-bold text-black dark:text-zinc-50'>404</h1>
        <h2 className='mt-4 text-2xl font-semibold text-black dark:text-zinc-50'>
          Subdomain Not Found
        </h2>
        <p className='mt-4 text-zinc-600 dark:text-zinc-400'>This subdomain doesn&apos;t exist.</p>
      </div>
    </div>
  );
}
