export const environment = {
  production: true,
  api: {
    url: 'http://localhost:4200/api/v1'
  },
  keycloak: {
    url: 'http://localhost:4200/auth',
    realm: 'facerecon',
    clientId: 'facerecon_backend'
  }
};
