"""
The code here is using D-Lib by Davis E. King's pre-trained face recognition model
@Article{dlib09,
  author = {Davis E. King},
  title = {Dlib-ml: A Machine Learning Toolkit},
  journal = {Journal of Machine Learning Research},
  year = {2009},
  volume = {10},
  pages = {1755-1758},
}
"""

from socket import timeout
import psycopg2
import cv2
import dlib
from psycopg2.extras import execute_values
import os
from FaceRecognitionFunctions import *



work_dir = './LFW/'


def update_table(id, name, face_emb):
    id = str(id)
    name = str(name)
    try:
        print(f"id:{id}, name: {name}, face embedding: {face_emb}")
        cur.execute("INSERT INTO face_table (id,name,face_embedding) VALUES (%s,%s,%s)", (id, name, face_emb))
    except psycopg2.DatabaseError as e :
        print('Error! face_table', e)
    con.commit()


def folder_exec():
    x = 0
    for name in os.listdir(work_dir):
        print(name)
        img = dlib.load_rgb_image(work_dir + name + '/' + name + '_0001.jpg')
        face_desc = get_face_embedding(img)
        face_emb = vec2list(face_desc)
        if len(face_emb) == 128:
            update_table(x, name, face_emb)
        cv2.imshow('img', cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
        key = cv2.waitKey(1) & 0XFF
        if key == ord('q'):
            break
        # if x > 10:
        #     break
        x += 1
    con.commit()
    cur.close()
    con.close()


def cam_exec():
    x = 1001
    name = 'Rajesh'
    cam = cv2.VideoCapture(0)
    while cam.isOpened():
        b, img = cam.read()
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        face_desc = get_face_embedding(img)
        face_emb = vec2list(face_desc)
        cv2.imshow('img', cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
        key = cv2.waitKey(1) & 0XFF
        if len(face_emb) == 128 and key == ord('r'):
            update_table(x, name, face_emb)
            x += 1
            print("UPDATED Successfully")
        if key == ord('q'):
            break


if __name__ == "__main__":
    folder_exec()
    # cam_exec()
