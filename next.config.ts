import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  reactStrictMode: true,
  output: 'standalone',
  // Enable middleware for subdomain routing
  // The middleware will handle subdomain detection and tenant routing
};

export default nextConfig;
