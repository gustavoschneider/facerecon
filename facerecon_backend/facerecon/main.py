from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from tortoise.contrib.fastapi import register_tortoise

from . import routers

app = FastAPI()

ORIGINS = [
    "http://localhost:4200",
    "https://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = ORIGINS,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

@app.get('/')
async def root():
    return { 'message': 'Nothing to see here!' }

app.include_router(
    routers.router
)

register_tortoise(
    app,
    db_url = 'postgres://facerecon:facerecon@localhost:15432/facerecon',
    modules = {
        'models': [
            'facerecon.models.management',
            'facerecon.models.face'
        ]
    },
    generate_schemas = True,
    add_exception_handlers = True,
)