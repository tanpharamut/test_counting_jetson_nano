import argparse 
import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
import cv2
import os
import datetime
from urllib.parse import urlparse
import requests
import json
import matplotlib.pyplot as plt

# import library for API
from flask import Flask, render_template , request, make_response
import requests
import os
import glob
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.video.io.VideoFileClip import VideoFileClip
import moviepy.editor as moviepy
import subprocess
from moviepy.editor import VideoFileClip

# import library for Yolo-V3
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
import sys
import cv2
from yolo_v3 import Yolo_v3
from utils import load_images, load_class_names, draw_boxes, draw_frame

os.chdir('/media/jetson/data/code/drawbox_ui/Main-forjetson')
_MODEL_SIZE = (416, 416)
_CLASS_NAMES_FILE = './data/labels/coco.names'
_MAX_OUTPUT_SIZE = 20
    
iou_threshold = 0.5
confidence_threshold = 0.5
class_names = load_class_names(_CLASS_NAMES_FILE)
n_classes = len(class_names)

model = Yolo_v3(n_classes=n_classes, model_size=_MODEL_SIZE,
                    max_output_size=_MAX_OUTPUT_SIZE,
                    iou_threshold=iou_threshold,
                    confidence_threshold=confidence_threshold)

batch_size = 1
inputs = tf.placeholder(tf.float32, [batch_size, *_MODEL_SIZE, 3])
detections = model(inputs, training=False)
saver = tf.train.Saver(tf.global_variables(scope='yolo_v3_model'))
                   
def main(type, input_names, model, class_names, n_classes, detections, saver):
    
    if type == 'images':
        batch = load_images(input_names, model_size=_MODEL_SIZE)
        with tf.Session() as sess:
            saver.restore(sess, '/media/jetson/data/code/drawbox_ui/Main-forjetson/weights/model.ckpt')
            detection_result = sess.run(detections, feed_dict={inputs: batch})


        boxes_dict_result = draw_boxes(input_names, detection_result, class_names, _MODEL_SIZE)
        return boxes_dict_result
    
        print('Detections have been saved successfully.')

    else:
        raise ValueError("Inappropriate data type. Please choose either 'video' or 'images'.")

def counting_people(path, second, fps, dff, path_folder, img_save):

    result_count = pd.DataFrame(columns= ['round', 'idp', 'count', 'gender','gender prob', 'category',
                                                  'category prob','distance', 'path_cerrent', 'path_before', ])
    print('test')
    see = 0
    img_middle = f'{path}'
    
    images_to_delete = []
    images_to_delete.append(img_middle)
    
    #📍 yolo v3 model ------------------------------------------------------------------------------------

    boxes_dict_result = main('images', [img_middle], model, class_names, n_classes, detections, saver)

    # don't detect
    if len(boxes_dict_result) == 0:
        totalR = 0
        stratf = 0
    else: 
        

    #📍 Create .CSV file for VISUALIZATION ----------------------------------------------------------------
        i = -1
        data_list = []
        for j in range(len(boxes_dict_result)):
            i = i+1
            result_person = boxes_dict_result[j]
            data_list.append({'Person_no':i, 'Image':img_middle, 
                                'Xmin':result_person[0], 'Xmax':result_person[2],
                                'Ymin':result_person[1], 'Ymax':result_person[3], 
                                'cX':int((result_person[0] + result_person[2]) / 2.0),
                                'cY':int((result_person[1] + result_person[3]) / 2.0)})
        resultdf = pd.DataFrame(data_list)

    #📍 Counting people ------------------------------------------------------------------------------------
    
        X1 = list(dff['X1'])[0]
        X4 = list(dff['X4'])[0]
        Y1 = list(dff['Y1'])[0]
        Y4 = list(dff['Y4'])[0]

        totalR = 0
        for per in range(len(resultdf)):
            id_0 = resultdf[resultdf['Person_no'] == per]
            counted = False
            centroid_x = list(id_0['cX'])[0]
            centroid_y = list(id_0['cY'])[0]
            if not counted:
                if (centroid_x >= X1 and centroid_x <= X4)&(centroid_y >= Y1 and centroid_y <= Y4):
                    totalR += 1
                    counted = True

            if counted == True:
                see = see + 1
                
                img = plt.imread(list(id_0['Image'])[0])
                img_crop = img[int(id_0['Ymin']):int(id_0['Ymax']), int(id_0['Xmin']):int(id_0['Xmax'])]
                print(img_crop.shape)

                path_new = path_folder+'/person_'+ str(per)+'_'+ str(date.strftime("%H-%M-%S"))
                if not os.path.exists(path_new):
                    os.makedirs(path_new)
                savepath = path_new +'/'
                img_name = img_middle.split('/')[-1].split('.jpg')[0]+'_'+str(per)+'.jpg'
                plt.imsave(os.path.join(savepath, img_name), img_crop) 

                ############################################
                ###### EffNet model - Gender classify ######
                ############################################
                
                img_path = savepath + img_name
                
                if (per == 0) & (see == 1):
                    img_path_old = img_path
                elif (per == 0) & (see != 1):
                    img_path_old = img_path_old
                else:
                    img_path_old = 'None'
                    

                import requests
                import json
                url = 'http://10.177.191.30:5007/request'  
                myobj = {'img_path': img_path,
                            'see': see,
                            'per': per}
                x = requests.post(url, data = json.dumps(myobj))
                result = list(x.text.split(" "))
                df = pd.DataFrame([{'round':0 , 'idp':per , 'count':result[5] , 
                                    'gender':result[0], 'gender prob':result[1], 
                                    'category':result[2], 'category prob':result[3], 
                                    'distance':result[4], 'path_cerrent': img_path, 'path_before': img_path_old}])
                result_count = result_count.append(df)
                print(f'/media/jetson/data/code/drawbox_ui/Main-forjetson/static/result-csv/{img_path_}.csv')    
                result_count.to_csv(f'/media/jetson/data/code/drawbox_ui/Main-forjetson/static/result-csv/{img_path_}.csv')
                #img_path_old = savepath+img_name
                
    # for img_path in images_to_delete:
    #     try:
    #         os.remove(img_path)
    #         print(f"Deleted: {img_path}")
    #     except OSError as e:
    #         print(f"Error deleting {img_path}: {e}")
            
    totalclip = totalclip + totalR                  
    print(totalclip) 
    done = f"Counting have been saved successfully."
    return done

def parse_input():
    parser = argparse.ArgumentParser(description='Input:')
    parser.add_argument(
        '-f',
        type = int,
        help = 'value of fps')
    
    parser.add_argument(
        '-second',
        type = int,
        default = 5, # values - [5, 10]
        help = 'value of se')
    
    parser.add_argument(
        '-img_save',
        type = str,
        help = 'value of image_save')
    
    args = parser.parse_args()
    return args

if __name__ == "__main__": 
    save_interval = 5 # The default value for setting the number of seconds of the desired image

    folder_res = 'CCTV_Storage1' # [1] Setting name folder for save save frame in subfolder
    #name = os.path.join('/media/jetson/data/code/drawbox_ui/Main-forjetson/static/vid_storage', folder_res) # Create head path name for save image
    name = os.path.join('./static/vid_storage', folder_res) # Create head path name for save image
    print("ALl logs saved in dir:", name)
    os.makedirs(name, exist_ok=True) # Create head path

    df = pd.read_csv('static/link_count_people.csv')

    # Filter out rows with missing data
    df = df.dropna()

    # Get the link and name values from the filtered DataFrame
    links = df['Link'].tolist()
    names = df['Name'].tolist()

    # Repeat the link and name values twice
    cap_list = links * 2
    cctv = names * 2

    print(cctv)
    print(cap_list)
    args = parse_input()
    fps = args.f
    
    while True: # Endless loop repeat
        for i in range(len(cctv)):
            ############################################################################################
            cap = cv2.VideoCapture(cap_list[i]) # CCTV6 
            cctv_name = cctv[i]
            ############################################################################################   
            #fps = int(cap.get(cv2.CAP_PROP_FPS)) # Keep fps of CCTV
            fps = args.f
            print(fps)

            # Extract the IP address from the link using urlparse
            parsed_url = urlparse(cap_list[i])
            ip_address = parsed_url.netloc.split('@')[-1].replace('/', '_')
        
            date = datetime.datetime.now() # First timer
            dir = os.path.join(ip_address, cctv_name + str(date.strftime("%Y")) + str(date.strftime("%m")) + str(
                date.strftime("%d")) + '_' + str(date.strftime("%H-%M-%S")))
            path = os.path.join(name, dir) # Create name path for keep image
            os.makedirs(path, exist_ok=True) # Create sub path
            print(path)
            print((int(cap.get(3)), int(cap.get(4)))) # Show resolution of image

            #count = 1 # The default value for count frame
            # while cap.isOpened(): # Started capturing the frames
            #     end_frame = (fps*2)+1
            #     for i in range(1, end_frame): # [3] Setting count frame by computing fps*sec
            #         ret, frame = cap.read() # Read the frames from our video. It return ret and actual frame
            #         if ret == True: # The ret is true if the frame is read successfully
            #                 cv2.imwrite(path + '/' + str(i) + '.jpg', frame) 
            #                 if count % (fps * save_interval) == 0: # Condition keep image every 2 sec.
            #                     print(count % (fps * save_interval))
            #                 count += 1
            #     cap.release()
            #     break

            # cap.release() # Release the camera when it's done.
            
            while cap.isOpened():
                ret, frame = cap.read()

                if ret == True:
                    # Find the highest-numbered image in the path
                    existing_images = [f for f in os.listdir(path) if f.endswith('.jpg')]
                    if existing_images:
                        highest_number = max([int(os.path.splitext(img)[0]) for img in existing_images])
                    else:
                        highest_number = 0

                    # Save the new image with the next sequential number
                    new_image_path = os.path.join(path, str(highest_number + 1) + '.jpg')
                    cv2.imwrite(new_image_path, frame)
                    break

            cap.release()
            
            cv2.destroyAllWindows() #  Simply destroys all the windows we created
            
            args = parse_input()
            fps = args.f
            img_path = new_image_path
            second = args.second
            img_save = args.img_save

            img_path_ = img_path.split('/')[-1]
            path_folder = f'/media/jetson/data/code/drawbox_ui/Main-forjetson/static/output_images/{img_path_}/'
            #path_folder = f'./static/output_images/{img_path_}/'
            if not os.path.exists(path_folder):
                os.mkdir(path_folder)
            path = img_path 

    
            import pandas as pd 
            import os
            dff = pd.read_csv(f'/media/jetson/data/code/drawbox_ui/Main-forjetson/static/output/{ip_address}.csv') #area box
            #dff = pd.read_csv(f'./static/output/{ip_address}.csv') #area box
            #os.chdir('/media/hdd/code/VDO-DEMO-BearHouse/Counting-People/')# -----------------------แก้ save cut video
            ##################### แก้ 
            result = counting_people(path, second, fps, dff, path_folder, img_save)
            print(result)
            #result.to_csv(f'/media/jetson/data/code/drawbox_ui/test_count_jetson/static/result-csv/{img_path_}.csv')# -----------------------แก้
            #result.to_csv(f'./static/result-csv/{img_path_}.csv')# -----------------------แก้
            # $ python python_script_label.py -s 0 -e 1560 -second 5 -f 20 -clip '/media/tohn/HDD/VDO-DEMO-KKU/IP Camera18_Complex_Complex_20230606112617_20230606115925_5345751422.mp4'