module.exports = {
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: "http://13.125.65.7:5000/api/:path*",
      },
    ];
  },
  images: {
    domains: ["13.125.65.7"],
  },
};
