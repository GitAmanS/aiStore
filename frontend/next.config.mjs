/** @type {import('next').NextConfig} */
// const nextConfig = {};
const nextConfig = {
    images: {
      remotePatterns: [
        {
          protocol: "https",
          hostname: "cdn.dummyjson.com",
        },
      ],
    },
  };
export default nextConfig;
