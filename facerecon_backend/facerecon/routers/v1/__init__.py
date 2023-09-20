from fastapi import APIRouter

#from . import mymodel
from . import face
from . import management

router = APIRouter(
    prefix = '/v1'
)

#router.include_router(mymodel.router)
router.include_router(face.router)
router.include_router(management.router)