import time
import pickle
import numpy as np

from deepface.basemodels import DlibWrapper, VGGFace, Facenet, OpenFace, ArcFace
from deepface.commons import functions, distance as dst

MODELS = {
    'dlib': DlibWrapper.loadModel(),
    'vggface': VGGFace.loadModel(),
    'facenet': Facenet.loadModel(),
    'openface': OpenFace.loadModel(),
    'arcface': ArcFace.loadModel()
}

def get_models_names():
    return sorted(MODELS)


def get_face_encoding(image_path, model_name):
    try:
        processed_img = functions.preprocess_face(image_path, target_size=tuple(functions.find_input_shape(MODELS[model_name])))
        return MODELS[model_name].predict(processed_img)[0,:]
    except Exception as e:
        print(e)
        raise e


def get_match(image_path, model_name, know_encodings):
    try:
        start_time = time.time()
        img_encoding = get_face_encoding(image_path, model_name)
        for encoding in know_encodings:
            distance = dst.findEuclideanDistance(dst.l2_normalize(img_encoding), dst.l2_normalize(pickle.loads(encoding.face_encoding)))
            distance = np.float64(distance) #causes trobule for euclideans in api calls if this is not set (issue #175)
            threshold = dst.findThreshold(model_name, encoding.metrics_name)
            if distance <= threshold:
                return {
                    'face': encoding.face,
                    'model_name': encoding.model_name,
                    'distance': distance,
                    'threshold': threshold,
                    'metrics': encoding.metrics_name,
                    'time': (time.time() - start_time)
                }
        
        return None
    except Exception as e:
        print(e)
        raise e

