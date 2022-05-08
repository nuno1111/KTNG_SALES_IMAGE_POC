module.exports = {
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: "http://13.125.65.7:5000/api/:path*",
        // destination: "http://127.0.0.1:5000/api/:path*",
      },
    ];
  },
  images: {
    domains: ["13.125.65.7"],
    // domains: ["127.0.0.1"],
  },
};
