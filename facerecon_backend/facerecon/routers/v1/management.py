from typing import List, Any

from fastapi import APIRouter, Depends, HTTPException, status, Request
from facerecon.security import get_current_user

from facerecon.models.management import Client
from facerecon.schemas.management import Client_Pydantic, ClientIn_Pydantic

from facerecon.libs import keycloak_helpers

from tortoise.exceptions import DoesNotExist

import uuid

router = APIRouter(
    prefix='/management',
    tags=['Management']
)

@router.get('/me')
async def get_me(current_user = Depends(get_current_user)):
    return current_user

@router.get('/clients', response_model = List[Client_Pydantic])
async def get_clients(current_user = Depends(get_current_user)):
    try:
        return await Client_Pydantic.from_queryset(Client.filter(user_id = current_user['sub'], deleted=False))
    except Exception as e:
        print(e)
        raise HTTPException(e)

@router.post('/clients', response_model = Client_Pydantic)
async def post_clients(data: ClientIn_Pydantic, current_user = Depends(get_current_user)):
    try:
        client_keycloak = keycloak_helpers.create_client({
            'name': data.client_name,
            'description': data.client_description,
            'clientId': data.client_id,
            'redirectUris': [ uris.strip() for uris in data.client_redirecturis.split(',') ],
            'webOrigins': [ origins.strip() for origins in data.client_weborigins.split(',') ]
        })
        data = dict(data)
        data.update({'keycloak_id': client_keycloak['id'], 'user_id': current_user['sub'] })
        client_obj = await Client.create(**data)
        return await Client_Pydantic.from_tortoise_orm(client_obj)
    except Exception as e:
        print(e)
        raise HTTPException(e)

@router.get('/clients/{client_id}', response_model = Client_Pydantic)
async def get_client(client_id: str, current_user = Depends(get_current_user)):
    try:
        return await Client_Pydantic.from_queryset_single(Client.get(user_id = current_user['sub'], keycloak_id = client_id, deleted=False))
    except DoesNotExist as e:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = str(e)
        )
    except Exception as e:
        print(e)
        raise Exception(e)

@router.put('/clients/{client_id}', response_model = Client_Pydantic)
async def put_client(client_id: str, data: Client_Pydantic, current_user = Depends(get_current_user)):
    try:
        client = await Client.get(user_id = current_user['sub'], keycloak_id = client_id)
        client_keycloak = keycloak_helpers.update_client({
            'id': client_id,
            'name': data.client_name,
            'description': data.client_description,
            'clientId': data.client_id,
            'redirectUris': [ uris.strip() for uris in data.client_redirecturis.split(',') ],
            'webOrigins': [ origins.strip() for origins in data.client_weborigins.split(',') ]
        })

        client.update_from_dict(data.dict())
        await client.save()
        return Client_Pydantic.from_orm(client)
    
    except DoesNotExist as e:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = str(e)
        )
    except Exception as e:
        print(e)
        raise Exception(e)

@router.delete('/clients/{client_id}')
async def delete_client(client_id: str, current_user = Depends(get_current_user)):
    try:
        new_clientId = uuid.uuid4().hex
        client = await Client.get(user_id = current_user['sub'], keycloak_id=client_id)
        keycloak_helpers.delete_client(client_id)
        client.update_from_dict({'client_id': new_clientId, 'deleted': True})
        await client.save()
        return Client_Pydantic.from_orm(client)

    except DoesNotExist as e:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = str(e)
        )
    except Exception as e:
        print(e)
        raise Exception(e)
    
@router.get('/clients/{client_id}/credentials')
async def get_client_credentials(client_id: str, current_user = Depends(get_current_user)):
    try:
        client = await Client.get(user_id = current_user['sub'], keycloak_id = client_id)
        client_credentials = keycloak_helpers.get_client_credentials(client.keycloak_id)
        return client_credentials

    except DoesNotExist as e:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = str(e)
        )
    except Exceptions as e:
        print(e)
        raise Exception(e)