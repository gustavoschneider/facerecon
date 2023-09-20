from tortoise.models import Model
from tortoise import fields

class Client(Model):
    id = fields.BigIntField(pk=True)
    keycloak_id = fields.CharField(36, null=False, unique=True)
    user_id = fields.CharField(36, null=False)

    client_id = fields.CharField(255, null=False, unique=True)
    client_name = fields.CharField(255, null=False)
    client_description = fields.TextField()
    client_weborigins = fields.TextField(null=False)
    client_redirecturis = fields.TextField(null=False)

    deleted = fields.BooleanField(null=False, default=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    def __repr__(self):
        return "<Client(id='{}', keycloak_id='{}', user_id='{}', client_id='{}', client_name='{}', client_description='{}')>".format(
            self.id,
            self.keycloak_id,
            self.user_id,
            self.client_id,
            self.client_name,
            self.client_description
        )
    
    class Meta:
        table = 'clients'


