import os
import cv2
import dlib
import psycopg2

con = psycopg2.connect(
        host = "172.22.0.2",
        database='postgres',
        user='postgres',
        password='OpenCV'
)
cur = con.cursor()


face_rec_model_path = './Data/dlib_face_recognition_resnet_model_v1.dat'
predictor_path = './Data/shape_predictor_5_face_landmarks.dat'
work_dir = './LFW/'

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

def retrieve(emb):
    query_string = """
    select face_table.id as tabid, face_table.name as tabname,
        euclidian ('{0}', face_table.face_embedding) as eucl from face_table
    order by eucl ASC
    limit 1
    """.format(emb).replace('[','{').replace(']','}')
    # print(query_string)
    cur.execute(query_string)
    result = cur.fetchall()
    return result

