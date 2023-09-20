from tortoise.models import Model
from tortoise import fields

class Face(Model):
    id = fields.BigIntField(pk=True)
    name = fields.CharField(255, null=False)
    image_path = fields.CharField(255, null=False, unique=True)

    client = fields.ForeignKeyField('models.Client', related_name='faces')

    def __repr__(self):
        return "<Face(id='{}', name='{}', image_path='{}', client='{}')>".format(
            self.id,
            self.name,
            self.image_path,
            self.client
        )

class FaceEncoding(Model):
    id = fields.BigIntField(pk=True)
    model_name = fields.CharField(30, null=False)
    metrics_name = fields.CharField(30, nullable=False)
    face_encoding = fields.BinaryField(null=False)

    face = fields.ForeignKeyField('models.Face', related_name='face_encodings')

    def __repr__(self):
        return "<FaceEncoding(id='{}', face='{}', model_name='{}', metrics_name='{}', face_encoding='{}')>".format(
            self.id,
            self.face,
            self.model_name,
            self.metrics_name,
            self.face_encoding
        )
