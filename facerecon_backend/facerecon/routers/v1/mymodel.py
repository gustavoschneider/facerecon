# pylint: disable=E0611
from typing import List

from fastapi import APIRouter, HTTPException
from tortoise.contrib.fastapi import HTTPNotFoundError

from facerecon.models.mymodel import MyModel
from facerecon.schemas.mymodel import MyModel_Pydantic, MyModelIn_Pydantic

router = APIRouter(
    prefix='/mymodel',
    tags=['My Model']
)

@router.get('/', response_model = List[MyModel_Pydantic])
async def get_mymodels():
    return await MyModel_Pydantic.from_queryset(MyModel.all())

@router.post('/', response_model = MyModel_Pydantic)
async def post_mymodel(mymodel: MyModelIn_Pydantic):
    mymodel_obj = await MyModel.create(**mymodel.dict(exclude_unset=True))
    return await MyModel_Pydantic.from_tortoise_orm(mymodel_obj)


@router.get('/{mymodel_id}', response_model = MyModel_Pydantic, responses={404: {'model': HTTPNotFoundError }})
async def get_mymodel(mymodel_id: int):
    return await MyModel_Pydantic.from_queryset_single(MyModel.get(id = mymodel_id))

@router.put('/{mymodel_id}', response_model=MyModel_Pydantic, responses={404: {'model': HTTPNotFoundError }})
async def put_mymodel(mymodel_id: int, mymodel_data: MyModelIn_Pydantic):
    await MyModel.filter(id=mymodel_id).update(**mymodel_data.dict(exclude_unset=True))
    return await MyModel_Pydantic.from_queryset_single(MyModel.get(id = mymodel_id))

@router.delete('/{mymodel_id}', responses={404: {'models': HTTPNotFoundError}})
async def delete_mymodel(mymodel_id: int):
    delete_count = await MyModel.filter(id=mymodel_id).delete()
    if not delete_count:
        raise HTTPException(status_code=404, detail=f'MyModel {mymodel_id} not found')
    return f'MyModel {mymodel_id} deleted'
