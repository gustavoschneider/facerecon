from tortoise.contrib.pydantic import pydantic_model_creator
from facerecon.models import management


Client_Pydantic = pydantic_model_creator(management.Client, name='Client')
ClientIn_Pydantic = pydantic_model_creator(management.Client, name='ClientIn', exclude_readonly=True, exclude=('keycloak_id', 'user_id', 'deleted',))
