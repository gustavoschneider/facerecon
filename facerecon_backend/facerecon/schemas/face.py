from tortoise.contrib.pydantic import pydantic_model_creator
from facerecon.models import face

Face_Pydantic = pydantic_model_creator(face.Face, name='Face')
FaceIn_Pydantic = pydantic_model_creator(face.Face, name='FaceIn', exclude_readonly=True)
FaceOut_Pydantic = pydantic_model_creator(face.Face, name='FaceOut', exclude=['face_encodings'])
