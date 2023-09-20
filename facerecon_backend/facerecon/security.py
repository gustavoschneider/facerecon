import warnings

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from pydantic import Json

from facerecon.libs.oauth2 import OAuth2ClientCredentials

with warnings.catch_warnings():
    # TODO: remove when fixed: https://github.com/mpdavis/python-jose/issues/208
    warnings.filterwarnings("ignore", message="int_from_bytes is deprecated")
    from keycloak import KeycloakOpenID
    from jose import jwt


KEYCLOAK_URL = "http://127.0.0.1:8080/auth/"
KEYCLOAK_REALM = "facerecon"
KEYCLOAK_CLIENT_ID = "facerecon_backend"

keycloak_openid = KeycloakOpenID(
    server_url=KEYCLOAK_URL,
    realm_name=KEYCLOAK_REALM,
    client_id=KEYCLOAK_CLIENT_ID
)

oauth2_user_login_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{KEYCLOAK_URL}realms/{KEYCLOAK_REALM}/protocol/openid-connect/token"
)

oauth2_client_login_scheme = OAuth2ClientCredentials(
    tokenUrl=f"{KEYCLOAK_URL}realms/{KEYCLOAK_REALM}/protocol/openid-connect/token"
)



async def get_current_user(token: str = Depends(oauth2_user_login_scheme)) -> Json:
    try:
        KEYCLOAK_PUBLIC_KEY = (
            "-----BEGIN PUBLIC KEY-----\n"
            + keycloak_openid.public_key()
            + "\n-----END PUBLIC KEY-----"
        )
        return keycloak_openid.decode_token(
            token,
            key=KEYCLOAK_PUBLIC_KEY,
            options={"verify_signature": True, "verify_aud": True, "exp": True},
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_current_client(token: str = Depends(oauth2_client_login_scheme)) -> Json:
    try:

        token_decoded = jwt.decode(token, key=[], options={
            'verify_signature': False,
            'verify_aud': False,
            'verify_iat': False,
            'verify_exp': False
        })

        k_openid = KeycloakOpenID(
            server_url=KEYCLOAK_URL,
            realm_name=KEYCLOAK_REALM,
            client_id=token_decoded['clientId']
        )
        k_public_key = (
            "-----BEGIN PUBLIC KEY-----\n"
            + k_openid.public_key()
            + "\n-----END PUBLIC KEY-----"
        )
        return k_openid.decode_token(
            token,
            key=k_public_key,
            options = {"verify_signature": True, "verify_aud": True, "exp": True},
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
