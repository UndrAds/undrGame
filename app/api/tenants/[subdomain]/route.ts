import { NextRequest, NextResponse } from 'next/server';
import { getTenant } from '@/lib/tenant';

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ subdomain: string }> }
) {
  const { subdomain } = await params;
  const tenant = await getTenant(subdomain);

  if (!tenant) {
    return NextResponse.json({ error: 'Tenant not found' }, { status: 404 });
  }

  return NextResponse.json({ tenant });
}
