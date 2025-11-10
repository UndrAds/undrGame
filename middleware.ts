import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';
import { getSubdomain, getTenant } from './lib/tenant';

export async function middleware(request: NextRequest) {
  const hostname = request.headers.get('host') || '';
  const subdomain = getSubdomain(hostname);

  // Root domain - proceed normally
  if (!subdomain) {
    return NextResponse.next();
  }

  // Subdomain - check if tenant exists
  const tenant = await getTenant(subdomain);

  if (!tenant) {
    // Tenant not found - show 404
    const url = request.nextUrl.clone();
    url.pathname = '/404';
    return NextResponse.rewrite(url);
  }

  // Tenant exists - add to headers
  const headers = new Headers(request.headers);
  headers.set('x-tenant-subdomain', tenant.subdomain);
  headers.set('x-tenant-publisher-email', tenant.publisher_email);
  headers.set('x-tenant-data', JSON.stringify(tenant));

  return NextResponse.next({
    request: { headers },
  });
}

export const config = {
  matcher: ['/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp|ico)).*)'],
};
