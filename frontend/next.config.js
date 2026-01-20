/** @type {import('next').NextConfig} */
const nextConfig = {
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  },
  async rewrites() {
    return [
      {
        source: '/api/auth/:path*',
        destination: `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/auth/:path*`,
      },
    ];
  },
  webpack: (config, { isServer, webpack }) => {
    // Fix for: Module build failed: UnhandledSchemeError: Reading from "node:crypto" is not handled by plugins
    if (!isServer) {
        config.resolve.fallback = {
            ...config.resolve.fallback,
            crypto: false, // Polyfill or disable if not needed on client
            fs: false,
            path: false,
            os: false,
        };
    }

    // Handle node: protocol imports
    config.plugins.push(
      new webpack.NormalModuleReplacementPlugin(
        /^node:/,
        (resource) => {
          resource.request = resource.request.replace(/^node:/, "");
        }
      )
    );

    return config;
  },
}

module.exports = nextConfig
