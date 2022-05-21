from tortoise import fields, models
from typing import Union
from tortoise.contrib.pydantic import pydantic_model_creator




class Repas(models.Model):
    id_repas = fields.IntField(pk=True)
    #restaurant =  fields.OneToOneRelation("models.Restorant")
    restaurant = fields.ForeignKeyField(
        "models.Restorant", related_name="events", description="The Tournement this happens in")
    nom = fields.CharField(max_length=250)




class Restorant(models.Model):
    restaurant_id = fields.IntField(pk=True)
    nom = fields.CharField(max_length=250)
    description = fields.CharField(max_length=250)





    class PydanticMeta:
        pass

Restorant_Pydantic = pydantic_model_creator(Restorant, name="Restorant")
RestorantIn_Pydantic = pydantic_model_creator(Restorant,name="RestorantIn",exclude_readonly=True)



Repas_Pydantic = pydantic_model_creator(Repas, name="Repas")
RepasIn_Pydantic = pydantic_model_creator(Repas,name="Repas",exclude_readonly=True)