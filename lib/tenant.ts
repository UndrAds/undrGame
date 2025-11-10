/**
 * Simple tenant utilities - subdomain extraction and tenant lookup
 */

import type { Tenant } from '@/types/tenant';

const ROOT_DOMAIN = 'undrplay.com';

// Simple in-memory cache
const cache = new Map<string, { tenant: Tenant | null; expiresAt: number }>();

/**
 * Extract subdomain from hostname
 */
export function getSubdomain(hostname: string): string | null {
  const host = hostname.split(':')[0].toLowerCase();

  if (host === ROOT_DOMAIN || host === `www.${ROOT_DOMAIN}`) {
    return null;
  }

  if (host.endsWith(`.${ROOT_DOMAIN}`)) {
    const subdomain = host.replace(`.${ROOT_DOMAIN}`, '');
    if (/^[a-z0-9]([a-z0-9-]*[a-z0-9])?$/.test(subdomain)) {
      return subdomain;
    }
  }

  // Local development support
  if (host.includes('localhost') || host.includes('127.0.0.1')) {
    const parts = host.split('.');
    if (parts.length > 1 && parts[0] !== 'www' && parts[0] !== 'localhost') {
      return parts[0];
    }
  }

  return null;
}

/**
 * Fetch tenant from API
 */
async function fetchTenant(subdomain: string): Promise<Tenant | null> {
  try {
    const apiUrl = `https://api.undrads.com/undrplay/${encodeURIComponent(subdomain)}`;

    const response = await fetch(apiUrl, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      if (response.status === 404) {
        return null;
      }
      throw new Error(`API error: ${response.status} ${response.statusText}`);
    }

    const result = await response.json();

    if (result.data) {
      // Map API response to Tenant type
      return {
        subdomain: result.data.sub_domain,
        publisher_email: result.data.publisher_email,
      };
    }

    return null;
  } catch (error) {
    console.error(`Error fetching tenant for subdomain ${subdomain}:`, error);
    return null;
  }
}

/**
 * Get tenant by subdomain with simple caching (5 min TTL)
 */
export async function getTenant(subdomain: string): Promise<Tenant | null> {
  // Check cache
  const cached = cache.get(subdomain);
  if (cached && Date.now() < cached.expiresAt) {
    return cached.tenant;
  }

  // Fetch from database/API
  const tenant = await fetchTenant(subdomain);

  // Cache for 5 minutes
  cache.set(subdomain, {
    tenant,
    expiresAt: Date.now() + 5 * 60 * 1000,
  });

  return tenant;
}
