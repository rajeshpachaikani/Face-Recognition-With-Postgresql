import os
import cv2
import dlib

face_rec_model_path = 'C://Users//RajeshPachaikani//PycharmProjects//Postgresql-FaceRec//Data//dlib_face_recognition_resnet_model_v1.dat'
predictor_path = 'C://Users//RajeshPachaikani//PycharmProjects//Postgresql-FaceRec//Data//shape_predictor_5_face_landmarks.dat'
# work_dir = os.listdir('C:\\Users\\RajeshPachaikani\\Documents\\Dataset\\lfw')
work_dir = 'C:\\Users\\RajeshPachaikani\\Documents\\Dataset\\lfw\\'

facerec = dlib.face_recognition_model_v1(face_rec_model_path)
shapepredictor = dlib.shape_predictor(predictor_path)
detector = dlib.get_frontal_face_detector()


def vec2list(vec):
    out_list = []
    for i in vec:
        out_list.append(i)
    return out_list


def get_face_embedding(img):
    face_descriptor = []
    try:
        dets = detector(img, 1)
        for k, d in enumerate(dets):
            shape = shapepredictor(img, d)
            try:
                face_descriptor = facerec.compute_face_descriptor(img, shape)
            except:
                face_descriptor = []
    except:
        face_descriptor = []
    return face_descriptor


def folder_exec():
    x = 0
    for name in os.listdir(work_dir):
        print(name)
        img = dlib.load_rgb_image(work_dir + name + '\\' + name + '_0001.jpg')
        face_desc = get_face_embedding(img)
        face_emb = vec2list(face_desc)
        # if len(face_emb)==128:
        #     update_table(x,name,face_emb)
        cv2.imshow('img', cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
        key = cv2.waitKey(1) & 0XFF
        if key == ord('q'):
            break
        if x > 10:
            break
        x += 1
