import os
import shutil
import uuid

from fastapi import UploadFile

IMAGE_DIR = 'files'
IMAGE_TMP_DIR = 'files_tmp'

def save_image(keycloak_id, image: UploadFile):
    try:
        if image.filename.lower().endswith('jpg') or image.filename.lower().endswith('jpeg'):
            file_extension = 'jpg'
        else:
            file_extension = image.filename[-3:]
            
        filename = f'{IMAGE_DIR}/{keycloak_id}/{str(uuid.uuid4())}.{file_extension}'
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        with open(filename, 'wb') as buffer:
            shutil.copyfileobj(image.file, buffer)
        
        return filename
    except Exception as e:
        print('Erro: {}'.format(e))
        raise e

def save_image_tmp(keycloak_id, image: UploadFile):
    try:
        if image.filename.lower().endswith('jpg') or image.filename.lower().endswith('jpeg'):
            file_extension = 'jpg'
        else:
            file_extension = image.filename[-3:]
            
        filename = f'{IMAGE_DIR}/{keycloak_id}/{str(uuid.uuid4())}.{file_extension}'
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        with open(filename, 'wb') as buffer:
            shutil.copyfileobj(image.file, buffer)
        
        return filename
    except Exception as e:
        print('Erro: {}'.format(e))
        raise e

def remove_image_tmp(filename):
    if os.path.exists(filename):
        os.remove(filename)