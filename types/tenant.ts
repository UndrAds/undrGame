export interface Tenant {
  subdomain: string;
  publisher_email: string;
  // Add more fields as needed
  [key: string]: unknown;
}

/**
 * API response structure
 */
export interface ApiResponse {
  data?: {
    publisher_email: string;
    sub_domain: string;
  };
  message?: string;
}
