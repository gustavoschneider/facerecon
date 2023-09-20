const proxy = [
  {
    context: '/api',
    target: 'http://localhost:8000'
  },
  {
    context: '/auth',
    target: 'http://localhost:8080'
  }
];
module.exports = proxy;
