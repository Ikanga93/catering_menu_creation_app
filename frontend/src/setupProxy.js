// src/setupProxy.js

const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  app.use(
    '/api', // Adjust this path based on your API routes
    createProxyMiddleware({
      target: 'http://127.0.0.1:8000',
      changeOrigin: true,
    })
  );
};

/*
Explanation:

/api: This path should match the prefix of your Django API endpoints. Adjust it if your API uses a different prefix.

target: The backend server's URL.

Remove the Proxy Field from package.json:

Ensure that the "proxy" field is removed to prevent conflicts.
*/