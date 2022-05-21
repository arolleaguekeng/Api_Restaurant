from typing import TypeVar, Generic
from fastapi import FastAPI, HTTPException
from tortoise import Tortoise

from models import Restorant, Restorant_Pydantic, RestorantIn_Pydantic, Repas_Pydantic, RepasIn_Pydantic, Repas
from pydantic.typing import List
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise
from pydantic import BaseModel
import uvicorn



class Message(BaseModel):
    message: str

app = FastAPI(
    title="Cibus",
    description="Api pour la gestion de la base de donnée de l'application des restaurants",
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Deadpoolio the Amazing",
        "url": "http://x-force.example.com/contact/",
        "email": "dp@x-force.example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)
list_restau = []
print(list_restau)


# T = TypeVar('T')
# class Requests(Generic[T]):
#     @classmethod


@app.get("/")
async def hello():
    return {"hello": "world"}


# Add resquests for restaurant
@app.post("/restorant", response_model=RestorantIn_Pydantic)
async def create_restaurant(restaurant: RestorantIn_Pydantic):
    obj = await Restorant.create(**restaurant.dict(exclude_unset=True))
    return await RestorantIn_Pydantic.from_tortoise_orm(obj)


@app.get("/restorant/{id}", response_model=RestorantIn_Pydantic, responses={404: {"model": HTTPNotFoundError}})
async def get_one_restaurant(id: int):
    return await RestorantIn_Pydantic.from_queryset_single(Restorant.get(id=id))


@app.put("/restorant/{id}", response_model=Restorant_Pydantic, responses={404: {"model": HTTPNotFoundError}})
async def update_restaurant(id: int, restaurant: RestorantIn_Pydantic):
    await Restorant.filter(id=id).update(**restaurant.dict(exclude_unset=True))
    return await Restorant_Pydantic.from_queryset_single(Restorant.get(id=id))


@app.delete("/restorant/{id}", response_model=Message, responses={404: {"model": HTTPNotFoundError}})
async def delete_restaurant(id: int):
    delete_obj = await Restorant.filter(id=id).delete()
    if not delete_obj:
        raise HTTPException(status_code=404, detail="this restaurant, is not found")
    return Message(message="Succesfully deleted")


# get all restaurant
@app.get("/restorant/", response_model=List[RestorantIn_Pydantic])
async def get_all_restaurants():
    return await RestorantIn_Pydantic.from_queryset(Restorant.all())


# resuest for repas

@app.post("/repas/{restaurant_id}", response_model=RepasIn_Pydantic)
async def create_repas(repas: Repas_Pydantic, restaurant_id: int):
    obj = await Repas.filter(restaurant_id=restaurant_id).create(**repas.dict(exclude_unset=True))
    return await RepasIn_Pydantic.from_tortoise_orm(obj)


@app.get("/repas/{id}", response_model=RepasIn_Pydantic, responses={404: {"model": HTTPNotFoundError}})
async def get_one_repas(id: int):
    return await RepasIn_Pydantic.from_queryset_single(Repas.get(id=id))


@app.put("/repas/{id}", response_model=Repas_Pydantic, responses={404: {"model": HTTPNotFoundError}})
async def update_repas(id: int, repas: RepasIn_Pydantic):
    await Repas.filter(id=id).update(**repas.dict(exclude_unset=True))
    return await Repas_Pydantic.from_queryset_single(Repas.get(id=id))


@app.delete("/repas/{id}", response_model=Message, responses={404: {"model": HTTPNotFoundError}})
async def delete_repas(id: int):
    delete_obj = await Repas.filter(id=id).delete()
    if not delete_obj:
        raise HTTPException(status_code=404, detail="this repas, is not found")
    return Message(message="Succesfully deleted")


# get all repas
@app.get("/repas/", response_model=List[RepasIn_Pydantic])
async def get_all_repas():
    return await RepasIn_Pydantic.from_queryset(Repas.all())


if __name__ == "__main__":
    uvicorn.run("main:app", host="192.168.137.1", port=5000, log_level="info")

# "postgresql://user:password@postgresserver/db"
register_tortoise(
    app,
    db_url="postgres://postgres:root@localhost/restaurant",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True
)

