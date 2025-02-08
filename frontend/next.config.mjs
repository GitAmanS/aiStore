/** @type {import('next').NextConfig} */
// const nextConfig = {};
const nextConfig = {
    output: "export",
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
