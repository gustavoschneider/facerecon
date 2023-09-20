from typing import Optional
import time
import pickle

from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, status
from facerecon.security import get_current_client

from facerecon.models.management import Client
from facerecon.schemas.management import Client_Pydantic

from facerecon.models.face import Face, FaceEncoding
from facerecon.schemas.face import Face_Pydantic, FaceOut_Pydantic

from facerecon.libs import image_helper, face


import concurrent.futures

router = APIRouter(
    prefix='/face',
    tags=['Face Recognition']
)

@router.post('/', response_model = FaceOut_Pydantic)
async def post_add(name: str, image: UploadFile = File(...), current_client = Depends(get_current_client)):
    try:
        client = await Client_Pydantic.from_queryset_single(Client.get(client_id = current_client['clientId'], deleted = False))
        filename = image_helper.save_image(client.keycloak_id, image)
        face_obj = await Face.create(**{
            'name': name,
            'image_path': filename,
            'client_id': client.id
        })
        await face_obj.save()


        for model_name in face.get_models_names():
            face_encoding_obj = await FaceEncoding.create(**{
                'face_id': face_obj.id,
                'model_name': model_name,
                'metrics_name': 'euclidean_l2',
                'face_encoding': pickle.dumps(face.get_face_encoding(filename, model_name))
            })
            await face_encoding_obj.save()
        
        return FaceOut_Pydantic.from_orm(face_obj)

    except Exception as e:
        print(e)
        raise e

@router.post('/find')
async def post_find(model_names: Optional[str] = None, image: UploadFile = File(...), current_client = Depends(get_current_client)):
    try:
        start_time = time.time()
        client = await Client_Pydantic.from_queryset_single(Client.get(client_id = current_client['clientId'], deleted = False))
        filename = image_helper.save_image_tmp(client.keycloak_id, image)
        if not model_names:
            model_names = face.get_models_names()
        else:
            model_names = [ name.strip().lower() for name in model_names.split(',') ]

        know_face_encodings = await FaceEncoding.filter(face__client_id = client.id, model_name__in = model_names).prefetch_related('face')
        response = dict()

        for m_name in model_names:
            response[m_name] = face.get_match(filename, m_name, [ know_face for know_face in know_face_encodings if know_face.model_name == m_name])
            
        
        image_helper.remove_image_tmp(filename)
        response['time'] = (time.time() - start_time)
        return response

    except Exception as e:
        print(e)
        raise e

# @router.post('/find_with_threads')
# async def post_find_with_threads(model_names: Optional[str] = None, image: UploadFile = File(...), current_client = Depends(get_current_client)):
#     try:
#         start_time = time.time()
#         client = await Client_Pydantic.from_queryset_single(Client.get(client_id = current_client['clientId'], deleted = False))
#         filename = image_helper.save_image_tmp(client.keycloak_id, image)
#         if not model_names:
#             model_names = face.get_models_names()
#         else:
#             model_names = [ name.strip().lower() for name in model_names.split(',') ]

#         know_face_encodings = await FaceEncoding.filter(face__client_id = client.id, model_name__in = model_names).prefetch_related('face')
#         response = dict()

#         param_list = []
#         for m_name in model_names:
#             param_list.append((filename, m_name, [ enc for enc in know_face_encodings if enc.model_name == m_name]))
        
#         futures = []
#         #with concurrent.futures.ThreadPoolExecutor() as executor:
#         with concurrent.futures.ProcessPoolExecutor() as executor:
#             futures = [ executor.submit(face.get_match, *param) for param in param_list ]

#         # print('results:')
#         # print([f.result() for f in futures])
#         # for m_name in model_names:
#         #     response[m_name] = face.get_match(filename, m_name, [ know_face for know_face in know_face_encodings if know_face.model_name == m_name])
            
#         results = [f.result() for f in futures]
#         image_helper.remove_image_tmp(filename)
#         index = 0
#         for m_name in model_names:
#             response[m_name] = results[index]
#             index += 1
#         response['time'] = (time.time() - start_time)
#         return response

#     except Exception as e:
#         print(e)
#         raise e

# @router.post('/add', response_model = FaceOut_Pydantic)
# async def post_add(name: str, image: UploadFile = File(...), current_user: User_Pydantic = Depends(get_current_active_user)):
    
#     try:
#         if image.filename.lower().endswith('jpg') or image.filename.lower().endswith('jpeg'):
#             file_extension = 'jpg'
#         else:
#             file_extension = image.filename[-3:]
        
#         filename = f'files/{str(uuid.uuid4())}.{file_extension}'
        
#         with open(filename, 'wb') as buffer:
#             shutil.copyfileobj(image.file, buffer)
        
#         face_encoding = face_recognition.face_encodings(
#             face_recognition.load_image_file(filename)
#         )[0]

#         face_dict = {
#             'name': name,
#             'face_encoding': pickle.dumps(face_encoding),
#             'face_image': filename,
#             'owner_id': current_user.id
#         }

#         face_obj = await Face.create(**face_dict)
#         return await FaceOut_Pydantic.from_tortoise_orm(face_obj)

#     except Exception as e:
#         print(e)
#         return HTTPException(e)

# @router.post('/find_face_recognition')
# async def post_find_face_recognition(image: UploadFile = File(...), current_user: User_Pydantic = Depends(get_current_active_user)):
#     try:
#         # time
#         start_time = time.time()

#         if image.filename.lower().endswith('jpg') or image.filename.lower().endswith('jpeg'):
#             file_extension = 'jpg'
#         else:
#             file_extension = image.filename[-3:]
        
#         tmp_filename = f'files-find/{str(uuid.uuid4())}.{file_extension}'

#         know_encodings = await Face_Pydantic.from_queryset(Face.filter(owner_id = current_user.id))
        
#         know_faces_encoding = [ pickle.loads(faces.face_encoding) for faces in know_encodings ]
        

#         with open(tmp_filename, 'wb') as buffer:
#             shutil.copyfileobj(image.file, buffer)
        
#         face_encoding = face_recognition.face_encodings(
#             face_recognition.load_image_file(tmp_filename)
#         )[0]

#         os.remove(tmp_filename)
#         matches = face_recognition.compare_faces(know_faces_encoding, face_encoding, tolerance = 0.582)
        
#         if True in matches:
#             print("Best Match Index: {}".format(matches.index(True)))
#             print("Found: %s" % know_encodings[matches.index(True)].name)
#             # time
#             print("--- %s seconds ---" % (time.time() - start_time))
#             return FaceOut_Pydantic.from_orm(know_encodings[matches.index(True)])
#         else:
#             face_distances = face_recognition.face_distance(know_faces_encoding, face_encoding)
#             best_match_index = np.argmin(face_distances)

#             if matches[best_match_index]:
#                 print("Best Match Index: {}".format(best_match_index))
#                 print("Found: %s" % know_encodings[best_match_index].name)
#                 # time
#                 print("--- %s seconds ---" % (time.time() - start_time))
#                 return FaceOut_Pydantic.from_orm(know_encodings[best_match_index])
        
        
#         return HTTPException(
#             status_code = status.HTTP_404_NOT_FOUND,
#             detail = 'Could not find matches',
#         )

#     except Exception as e:
#         print(e)
#         os.remove(tmp_filename)
#         return HTTPException(e)
    

# @router.post('/add_deepface', response_model = FaceOut_Pydantic)
# async def post_add(name: str, image: UploadFile = File(...), current_user: User_Pydantic = Depends(get_current_active_user)):
#     try:
#         if image.filename.lower().endswith('jpg') or image.filename.lower().endswith('jpeg'):
#             file_extension = 'jpg'
#         else:
#             file_extension = image.filename[-3:]
        
#         filename = f'files/{str(current_user.id)}/{str(uuid.uuid4())}.{file_extension}'
        
#         os.makedirs(os.path.dirname(filename), exist_ok=True)

#         with open(filename, 'wb+') as buffer:
#             shutil.copyfileobj(image.file, buffer)
        
#         pre_process_image = dict()
#         for k in MODELS:
#             img = functions.preprocess_face(filename, target_size=tuple(functions.find_input_shape(MODELS[k])))
            
#             pre_process_image.update({
#                 k: img
#             })
        
#         face_dict = {
#             'name': name,
#             'face_image': filename,
#             'owner_id': current_user.id
#         }
#         face_obj = await Face.create(**face_dict)

#         for k in MODELS:
#             face_encoding_dict = {
#                 'model': k,
#                 'metrics': 'euclidean_l2',
#                 'encoding': pickle.dumps(MODELS[k].predict(pre_process_image[k])[0,:]),
#                 'face': face_obj
#             }

#             await FaceEncoding.create(**face_encoding_dict)
        
#         return await FaceOut_Pydantic.from_tortoise_orm(face_obj)

#     except Exception as e:
#         print(e)
#         return HTTPException(e)
    
# @router.post('/find_deepface')
# async def post_find_deepface(image: UploadFile = File(...), current_user: User_Pydantic = Depends(get_current_active_user)):
#     try:
        
#         if image.filename.lower().endswith('jpg') or image.filename.lower().endswith('jpeg'):
#             file_extension = 'jpg'
#         else:
#             file_extension = image.filename[-3:]
        
#         tmp_filename = f'files-find/{str(uuid.uuid4())}.{file_extension}'

#         with open(tmp_filename, 'wb') as buffer:
#             shutil.copyfileobj(image.file, buffer)
        
#         face_img_processed = dict()
#         for k in MODELS:
#             # time
#             start_time = time.time()
#             face_img_processed.update({
#                 k: functions.preprocess_face(tmp_filename, target_size = tuple(functions.find_input_shape(MODELS[k])))
#             })
#             # time
#             print("face_img_processed for {}".format(k))
#             print("--- %s seconds ---" % (time.time() - start_time))

#         face_embedding = dict()
#         for k in MODELS:
#             # time
#             start_time = time.time()
#             face_embedding.update({
#                 k: MODELS[k].predict(face_img_processed[k])[0,:]
#             })
#             # time
#             print("face_embedding for {}".format(k))
#             print("--- %s seconds ---" % (time.time() - start_time))
#         # face_img_processed = functions.preprocess_face(tmp_filename, target_size = input_shape, enforce_detection = False)
        
#         # face_embedding = MODEL.predict(face_img_processed)[0,:]
        
#         #know_encodings = await Face_Pydantic.from_queryset(Face.filter(owner_id = current_user.id).prefetch_related('face_encodings'))
#         know_encodings = await Face.filter(owner_id=current_user.id)
        
#         print('know_encodings.face_encodings')
        
#         information = {}

#         for encoding in know_encodings:
#             qntd_identified = 0
#             await encoding.fetch_related('face_encodings')
#             for face_encoding in encoding.face_encodings:
                
#                 # time
#                 print('------------')
#                 print('verify for: {}'.format(encoding))
#                 start_time = time.time()
#                 distance = dst.findEuclideanDistance(dst.l2_normalize(face_embedding[face_encoding.model]), dst.l2_normalize(pickle.loads(face_encoding.encoding)))
#                 distance = np.float64(distance) #causes trobule for euclideans in api calls if this is not set (issue #175)
#                 threshold = dst.findThreshold(face_encoding.model, face_encoding.metrics)
                
#                 print('distance: {}'.format(distance))
#                 print('threshold: {}'.format(threshold))

#                 if distance <= threshold:
#                     identified = True
#                     qntd_identified += 1
#                     face = FaceOut_Pydantic.from_orm(encoding)
#                     print('face: ')
#                     print(face)
#                     information = {
#                         'face': face,
#                         'model': {
#                             "verified": identified,
#                             "distance": distance,
#                             "max_threshold_to_verify": threshold,
#                             "model": face_encoding.model,
#                             "similarity_metric": face_encoding.metrics
#                         }
#                     }
                    
#                 else:
#                     identified = False
                	
#                 resp_obj = {
# 					"verified": identified,
#                     "distance": distance,
#                     "max_threshold_to_verify": threshold,
#                     "model": face_encoding.model,
#                     "similarity_metric": face_encoding.metrics
#                 }
                 

#                 print('response: {}'.format(resp_obj))
                
#                 # time
#                 print("verify for {}".format(face_encoding.model))
#                 print("--- %s seconds ---" % (time.time() - start_time))
        
        
#                 print('\n\n\n\n')
#                 print('qntd_identified:')
#                 print(qntd_identified)
#                 if qntd_identified/len(MODELS) > 0.5:
#                     return information
        
#         return HTTPException(
#             status_code = status.HTTP_404_NOT_FOUND,
#             detail = 'Could not find matches',
#         )

#     except Exception as e:
#         print(e)
#         os.remove(tmp_filename)
#         return HTTPException(e)

