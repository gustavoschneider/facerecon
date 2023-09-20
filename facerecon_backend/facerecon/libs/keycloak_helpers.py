import requests
import json

KEYCLOAK_URL_ADMIN = 'http://localhost:8080/auth/admin/realms/facerecon/'
KEYCLOAK_URL_LOGIN = 'http://localhost:8080/auth/realms/master/protocol/openid-connect/token'
KEYCLOAK_URL_LOGOUT = 'http://localhost:8080/auth/realms/master/protocol/openid-connect/logout'
KEYCLOAK_LOGIN_INFO = {
    'username': 'schneider@onlab.org',
    'password': 'agressor',
    'grant_type': 'password',
    'client_id': 'admin-cli'
}

KEYCLOAK_CLIENT_INFO_DEFAULTS = {
    'enabled': True,
    'authorizationServicesEnabled': True,
    'serviceAccountsEnabled': True,
    'name': None,
    'description': None,
    'clientId': None,
    'publicClient': False,
    'redirectUris': None,
    'webOrigins': None
}

KEYCLOAK_CLIENT_SCOPES_DEFAULTS = {
    'name': None,
    'protocol': 'openid-connect',
    'attributes': {
        'include.in.token.scope': True,
        'display.on.consent.screen': True
    },
    'protocolMappers': [{
        'name': None,
        'protocol': 'openid-connect',
        'protocolMapper': 'oidc-audience-mapper',
        'consentRequired': False,
        'config': {
            'access.token.claim': True,
            'id.token.claim': False,
            'included.client.audience': None
        }
    }]
}

def get_tokens():
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    req = requests.post(KEYCLOAK_URL_LOGIN, headers = headers, data=KEYCLOAK_LOGIN_INFO)
    if req.status_code != 200:
        raise Exception('Error: {}'.format(req.status_code))
    
    return {'access_token': req.json()['access_token'], 'refresh_token': req.json()['refresh_token'] }

def update_tokens(tokens):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = KEYCLOAK_LOGIN_INFO.copy()
    del data['username']
    del data['password']
    data['grant_type'] = 'refresh_token'
    data['refresh_token'] = tokens['refresh_token']
    req = requests.post(KEYCLOAK_URL_LOGIN, headers = headers, data=data)
    if req.status_code != 200:
        raise Exception('Error: {}'.format(req.status_code))
    return {'access_token': req.json()['access_token'], 'refresh_token': req.json()['refresh_token'] }

def logout(tokens = dict()):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer {}'.format(tokens['access_token'])
        }
    logout_data = KEYCLOAK_LOGIN_INFO.copy()
    del logout_data['username']
    del logout_data['password']
    del logout_data['grant_type']
    logout_data['refresh_token'] = tokens['refresh_token']
    req = requests.post(KEYCLOAK_URL_LOGOUT, headers = headers, data = logout_data)
    return req

def list_clients():
    tokens = get_tokens()
    headers = {'Authorization': 'Bearer {}'.format(tokens['access_token'])}
    req = requests.get(KEYCLOAK_URL_ADMIN + 'clients', headers = headers)
    if req.status_code != 200:
        logout(access_token)
        raise Exception('Error: {}'.format(req.status_code))
    logout(tokens)
    return req.json()

def get_clients_in_ids(clients_ids = []):
    if len(clients_ids) <= 0:
        return []
    all_clients = list_clients()
    return [ client for client in all_clients if client['id'] in clients_ids ]

def create_client_audience(client_info, tokens):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(tokens['access_token']),
    }
    scopes_data = KEYCLOAK_CLIENT_SCOPES_DEFAULTS.copy()
    scopes_data['name'] = client_info['clientId']
    scopes_data['protocolMappers'][0]['name'] = client_info['clientId'] + '_audience'
    scopes_data['protocolMappers'][0]['config']['included.client.audience'] = client_info['clientId']
    req = requests.post(KEYCLOAK_URL_ADMIN + 'client-scopes', headers = headers, data = json.dumps(scopes_data))
    return req.headers.get('Location').split('/')[-1]



def create_client(client_info = dict()):
    if 'name' not in client_info:
        raise Exception('\'name\' key not in dict')
    if 'description' not in client_info:
        raise Exception('\'description\' key not in dict')
    if 'clientId' not in client_info:
        raise Exception('\'clientId\' key not in dict')
    if 'redirectUris' not in client_info:
        raise Exception('\'redirectUris\' key not in dict')
    if 'webOrigins' not in client_info:
        raise Exception('\'webOrigins\' key not in dict')
    
    tokens = get_tokens()
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(tokens['access_token']),
    }
    client_data = KEYCLOAK_CLIENT_INFO_DEFAULTS.copy()
    client_data.update(client_info)
    req = requests.post(KEYCLOAK_URL_ADMIN + 'clients', headers = headers, data=json.dumps(client_data))
    if req.status_code != 201:
        logout(tokens)
        raise Exception('Error: {}'.format(req.status_code))
    location = req.headers.get('Location')
    scope_id = create_client_audience(client_info, tokens)
    req_scope_add = requests.put(KEYCLOAK_URL_ADMIN + 'clients/{}/default-client-scopes/{}'.format(location.split('/')[-1], scope_id), headers = headers)
    if req_scope_add.status_code != 204:
        logout(tokens)
        raise Exception('Error: {}'.format(req_scope_add.status_code))
    logout(tokens)
    return { 'id': location.split('/')[-1], 'url': location }

def update_client(client_info = dict()):
    if 'id' not in client_info:
        raise Exception('\id\' key not in dict')
    keycloak_id = client_info.pop('id')
    tokens = get_tokens()
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(tokens['access_token']),
    }
    client_data = dict()
    
    client_data.update(client_info)
    req = requests.put(KEYCLOAK_URL_ADMIN + 'clients/' + keycloak_id, headers = headers, data=json.dumps(client_data))
    if req.status_code != 204:
        logout(tokens)
        raise Exception('Error: {}'.format(req.status_code))
    return req

def get_client_credentials(client_id):
    tokens = get_tokens()
    headers = {'Authorization': 'Bearer {}'.format(tokens['access_token'])}
    req_client = requests.get(KEYCLOAK_URL_ADMIN + 'clients/' + client_id, headers = headers)
    if req_client.status_code != 200:
        logout(tokens)
        raise Exception('Error: {}'.format(req_client.status_code))
    clientId = req_client.json()['clientId']
    req_secret = requests.get(KEYCLOAK_URL_ADMIN + 'clients/' + client_id + '/client-secret', headers = headers)
    if req_secret.status_code != 200:
        logout(tokens)
        raise Exception('Error: {}'.format(req.status_code))
    logout(tokens)
    return { 'client_id': clientId, 'client_secret': req_secret.json()['value'] }


def delete_client(client_id):
    tokens = get_tokens()
    headers = {'Authorization': 'Bearer {}'.format(tokens['access_token'])}
    req_client_get = requests.get(KEYCLOAK_URL_ADMIN + 'clients/{}'.format(client_id), headers = headers)
    if req_client_get.status_code != 200:
        logout(tokens)
        raise Exception('Error: {}'.format(req_client_get.status_code))
    clientId = req_client_get.json()['clientId']
    req_client_scopes_get = requests.get(KEYCLOAK_URL_ADMIN + 'client-scopes', headers = headers)
    if req_client_scopes_get.status_code != 200:
        logout(tokens)
        raise Exception('Error: {}'.format(req_client_scopes_get.status_code))
    clients_scopes = req_client_scopes_get.json()
    client_scope_id = [ c_scope['id'] for c_scope in clients_scopes if c_scope['name'] == clientId ][0]
    req = requests.delete(KEYCLOAK_URL_ADMIN + 'clients/{}'.format(client_id), headers = headers)
    if req.status_code != 204:
        logout(tokens)
        raise Exception('Error: {}'.format(req.status_code))
    req_client_scope_delete = requests.delete(KEYCLOAK_URL_ADMIN + 'client-scopes/{}'.format(client_scope_id), headers = headers)
    if req_client_scope_delete.status_code != 204:
        logout(tokens)
        raise Exception('Error: {}'.format(req_client_scope_delete.status_code))
    logout(tokens)
    return req