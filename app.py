from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session
import pandas as pd
import cv2
import os
import subprocess
import io
import glob
import re
import requests
from moviepy.editor import VideoFileClip
from time import sleep
from main import create_dash_application

app = Flask(__name__)

df = pd.DataFrame(columns=['Username', 'Password', 'Name', 'IP', 'Type_box', 'X1', 'Y1', 'X2', 'Y2', 'X3', 'Y3', 'X4', 'Y4', 'Up to', 'Down to', 'Left to', 'Right to'])  # Create an empty DataFrame with columns
df1 = pd.DataFrame(columns=['Username', 'Password', 'Name', 'IP', 'Type_box', 'X1', 'Y1', 'X2', 'Y2', 'X3', 'Y3', 'X4', 'Y4', 'Up to', 'Down to', 'Left to', 'Right to'])  # Create an empty DataFrame with columns
df2 = pd.DataFrame(columns=['Username', 'Password', 'Name', 'IP', 'Type_box', 'X1', 'Y1', 'X2', 'Y2', 'X3', 'Y3', 'X4', 'Y4', 'Up to', 'Down to', 'Left to', 'Right to'])  # Create an empty DataFrame with columns
df3 = pd.DataFrame(columns=['Username', 'Password', 'Name', 'IP', 'Type_box', 'X1', 'Y1', 'X2', 'Y2', 'X3', 'Y3', 'X4', 'Y4', 'Up to', 'Down to', 'Left to', 'Right to'])  # Create an empty DataFrame with columns
df4 = pd.DataFrame(columns=['Username', 'Password', 'Name', 'IP', 'Type_box', 'X1', 'Y1', 'X2', 'Y2', 'X3', 'Y3', 'X4', 'Y4', 'Up to', 'Down to', 'Left to', 'Right to'])  # Create an empty DataFrame with columns
df5 = pd.DataFrame(columns=['Username', 'Password', 'Name', 'IP', 'Type_box', 'X1', 'Y1', 'X2', 'Y2', 'X3', 'Y3', 'X4', 'Y4', 'Up to', 'Down to', 'Left to', 'Right to'])  # Create an empty DataFrame with columns
shape_data = {}

draw_status = False
process = None
vdo_name_mp4 = None

app.secret_key = 'tanph26554'

# Check if the file exists
if not os.path.isfile('static/data2.csv'):
    # Create an empty DataFrame with columns
    df = pd.DataFrame(columns=['Username', 'Password', 'Name', 'IP', 'Type_box', 'X1', 'Y1', 'X2', 'Y2', 'X3', 'Y3', 'X4', 'Y4'])

    # Save the DataFrame to 'data2.csv'
    df.to_csv('static/data2.csv', index=False)

# Check if the file exists
if not os.path.isfile('static/link.csv'):
    # Create an empty DataFrame with columns
    dflink = pd.DataFrame(columns=['Name', 'Link'])

    # Save the DataFrame to 'data2.csv'
    dflink.to_csv('static/link.csv', index=False)

# Check if the file exists
if not os.path.isfile('static/link_congun.csv'):
    # Create an empty DataFrame with columns
    dflink = pd.DataFrame(columns=['Name', 'Link'])

    # Save the DataFrame to 'data2.csv'
    dflink.to_csv('static/link_congun.csv', index=False)
    
# Check if the file exists
if not os.path.isfile('static/link_count_people.csv'):
    # Create an empty DataFrame with columns
    dflink = pd.DataFrame(columns=['Name', 'Link'])

    # Save the DataFrame to 'data2.csv'
    dflink.to_csv('static/link_count_people.csv', index=False)
    
# Check if the file exists
if not os.path.isfile('static/status_function.csv'):
    # Create an empty DataFrame with columns
    dflink = pd.DataFrame(columns=['IP', 'function_congun', 'function_count_people'])

    # Save the DataFrame to 'data2.csv'
    dflink.to_csv('static/status_function.csv', index=False)

# Check if the file exists
if not os.path.isfile('static/status_client_side.csv'):
    # Create an empty DataFrame with columns
    dflink = pd.DataFrame(columns=['cs', 'row_num'])

    # Save the DataFrame to 'data2.csv'
    dflink.to_csv('static/status_client_side.csv', index=False)    
        
if not os.path.isfile('static/Images_IP.csv'):
    # Create an empty DataFrame with columns
    images = ['/Image_c1', '/Image_c2', '/Image_c3', '/Image_c4', '/Image_c5','/']
    dflink = pd.DataFrame(columns=['IP', '/Images'])
    
    # Add the image paths to the Link column
    for i in range(len(images)):
        dflink.loc[i] = ['', images[i]]

    # Save the DataFrame to 'link.csv'
    dflink.to_csv('static/Images_IP.csv', index=False)
    
# Check if the file exists
if not os.path.isfile('static/Sheets.csv'):
    # Create an empty DataFrame with columns
    dfsheets = pd.DataFrame(columns=['Name', 'Link'])

    # Save the DataFrame to 'data2.csv'
    dfsheets.to_csv('static/Sheets.csv', index=False)

path_folder = [
    os.path.join('static', 'vdo', 'avi'),
    os.path.join('static', 'vdo', 'mp4')
]
for path in path_folder:
    if not os.path.exists(path):
        os.makedirs(path)
        
@app.route('/')
def index():
    global last_data1, last_data2, last_data3, last_data4, last_data5
    
    existing_data = pd.read_csv('static/data2.csv')
    last_data1 = existing_data.iloc[0] if not existing_data.empty else None
    last_data2 = existing_data.iloc[1] if len(existing_data) >= 2 else None
    last_data3 = existing_data.iloc[2] if len(existing_data) >= 3 else None
    last_data4 = existing_data.iloc[3] if len(existing_data) >= 4 else None
    last_data5 = existing_data.iloc[4] if len(existing_data) >= 5 else None
    
    last_data = [last_data1, last_data2, last_data3, last_data4, last_data5]
    draw_status = False
    for data in last_data:
        if data is not None:
            draw_status = True  # Update draw_status to True if any non-None element is present
            break  # Exit the loop after finding a non-None element
        
    dfsheets = pd.read_csv('static/Sheets.csv')
    if not dfsheets.empty:
        sheets_link = dfsheets.loc[0, 'Link']
    else:
        sheets_link = ""
    
    #sheets_link = sheets_link.rsplit('/',1)[0] + '/export?format=csv'
    
    df_status = pd.read_csv('static/status_function.csv')
    status_c1_congun = df_status.loc[0, 'function_congun'] if not df_status.empty else None
    status_c1_count_people = df_status.loc[0, 'function_count_people'] if not df_status.empty else None
    status_c2_congun = df_status.loc[1, 'function_congun'] if len(df_status) >= 2 else None
    status_c2_count_people = df_status.loc[1, 'function_count_people'] if len(df_status) >= 2 else None
    selected_functions_c1 = []
    selected_functions_c2 = []

    # Check status_c1_congun and add 'congun' to selected_functions_c1 if 'yes'
    if status_c1_congun == 'yes':
        selected_functions_c1.append('congun')

    # Check status_c1_count_people and add 'count-people' to selected_functions_c1 if 'yes'
    if status_c1_count_people == 'yes':
        selected_functions_c1.append('count-people')   
        
    # Check status_c1_congun and add 'congun' to selected_functions_c1 if 'yes'
    if status_c2_congun == 'yes':
        selected_functions_c2.append('congun')

    # Check status_c1_count_people and add 'count-people' to selected_functions_c1 if 'yes'
    if status_c2_count_people == 'yes':
        selected_functions_c2.append('count-people')    
        
        
    return render_template('index.html', last_data1=last_data1, last_data2=last_data2, 
                           last_data3=last_data3, last_data4=last_data4, last_data5=last_data5, 
                           draw_status=draw_status,
                           selected_functions_c1=selected_functions_c1,
                           selected_functions_c2=selected_functions_c2)

@app.route('/data2.csv')
def serve_data_file():
    return send_from_directory('static', 'data2.csv')

@app.route('/Images_IP.csv')
def src_images():
    return send_from_directory('static', 'Images_IP.csv')

@app.route('/Image_c1')
def src_images_c1():
    
    def fetch_rtsp_image(rtsp_url, save_path):
    # Create a VideoCapture object with the RTSP URL
        cap = cv2.VideoCapture(rtsp_url)

        # Check if the camera stream is opened successfully
        if not cap.isOpened():
            print("Failed to open RTSP stream")
            return

        # Read a frame from the RTSP stream
        ret, frame = cap.read()

        # Release the VideoCapture object
        cap.release()

        # Check if a frame is successfully read
        if not ret:
            print("Failed to fetch frame from RTSP stream")
            return

        # Create the save directory if it doesn't exist
        os.makedirs(save_path, exist_ok=True)

        # Save the frame as an image
        image_path = os.path.join(save_path, "image.jpg")
        cv2.imwrite(image_path, frame)
        print("Image saved successfully:", image_path)

    # Example usage
    dflink = pd.read_csv('static/link.csv')
    rtsp_url = dflink.loc[0, 'Link']
    save_path = "static/images/camera1"
    fetch_rtsp_image(rtsp_url, save_path)

    base_dir = 'static/images/camera1'

    # Get the list of image files within the latest folder
    image_files = os.listdir(base_dir)
    image_files.sort(key=lambda x: os.path.getmtime(os.path.join(base_dir, x)), reverse=True)
    latest_image_filename = image_files[0]

    latest_image_path = latest_image_filename.replace("\\", "/")
  
    return send_from_directory(base_dir, latest_image_path)

@app.route('/Image_c2')
def src_images_c2():
    
    def fetch_rtsp_image(rtsp_url, save_path):
    # Create a VideoCapture object with the RTSP URL
        cap = cv2.VideoCapture(rtsp_url)

        # Check if the camera stream is opened successfully
        if not cap.isOpened():
            print("Failed to open RTSP stream")
            return

        # Read a frame from the RTSP stream
        ret, frame = cap.read()

        # Release the VideoCapture object
        cap.release()

        # Check if a frame is successfully read
        if not ret:
            print("Failed to fetch frame from RTSP stream")
            return

        # Create the save directory if it doesn't exist
        os.makedirs(save_path, exist_ok=True)

        # Save the frame as an image
        image_path = os.path.join(save_path, "image.jpg")
        cv2.imwrite(image_path, frame)
        print("Image saved successfully:", image_path)

    # Example usage
    dflink = pd.read_csv('static/link.csv')
    rtsp_url = dflink.loc[1, 'Link']
    save_path = "static/images/camera2"
    fetch_rtsp_image(rtsp_url, save_path)
    
    base_dir = 'static/images/camera2'

    # Get the list of image files within the latest folder
    image_files = os.listdir(base_dir)
    image_files.sort(key=lambda x: os.path.getmtime(os.path.join(base_dir, x)), reverse=True)
    latest_image_filename = image_files[0]

    latest_image_path = latest_image_filename.replace("\\", "/")
  
    return send_from_directory(base_dir, latest_image_path)

@app.route('/Image_c3')
def src_images_c3():
    
    def fetch_rtsp_image(rtsp_url, save_path):
    # Create a VideoCapture object with the RTSP URL
        cap = cv2.VideoCapture(rtsp_url)

        # Check if the camera stream is opened successfully
        if not cap.isOpened():
            print("Failed to open RTSP stream")
            return

        # Read a frame from the RTSP stream
        ret, frame = cap.read()

        # Release the VideoCapture object
        cap.release()

        # Check if a frame is successfully read
        if not ret:
            print("Failed to fetch frame from RTSP stream")
            return

        # Create the save directory if it doesn't exist
        os.makedirs(save_path, exist_ok=True)

        # Save the frame as an image
        image_path = os.path.join(save_path, "image.jpg")
        cv2.imwrite(image_path, frame)
        print("Image saved successfully:", image_path)

    # Example usage
    dflink = pd.read_csv('static/link.csv')
    rtsp_url = dflink.loc[2, 'Link']
    save_path = "static/images/camera3"
    fetch_rtsp_image(rtsp_url, save_path)
    
    base_dir = 'static/images/camera3'

    # Get the list of image files within the latest folder
    image_files = os.listdir(base_dir)
    image_files.sort(key=lambda x: os.path.getmtime(os.path.join(base_dir, x)), reverse=True)
    latest_image_filename = image_files[0]

    latest_image_path = latest_image_filename.replace("\\", "/")
  
    return send_from_directory(base_dir, latest_image_path)

@app.route('/Image_c4')
def src_images_c4():
    
    def fetch_rtsp_image(rtsp_url, save_path):
    # Create a VideoCapture object with the RTSP URL
        cap = cv2.VideoCapture(rtsp_url)

        # Check if the camera stream is opened successfully
        if not cap.isOpened():
            print("Failed to open RTSP stream")
            return

        # Read a frame from the RTSP stream
        ret, frame = cap.read()

        # Release the VideoCapture object
        cap.release()

        # Check if a frame is successfully read
        if not ret:
            print("Failed to fetch frame from RTSP stream")
            return

        # Create the save directory if it doesn't exist
        os.makedirs(save_path, exist_ok=True)

        # Save the frame as an image
        image_path = os.path.join(save_path, "image.jpg")
        cv2.imwrite(image_path, frame)
        print("Image saved successfully:", image_path)

    # Example usage
    dflink = pd.read_csv('static/link.csv')
    rtsp_url = dflink.loc[3, 'Link']
    save_path = "static/images/camera4"
    fetch_rtsp_image(rtsp_url, save_path)
    
    base_dir = 'static/images/camera4'

    # Get the list of image files within the latest folder
    image_files = os.listdir(base_dir)
    image_files.sort(key=lambda x: os.path.getmtime(os.path.join(base_dir, x)), reverse=True)
    latest_image_filename = image_files[0]

    latest_image_path = latest_image_filename.replace("\\", "/")
  
    return send_from_directory(base_dir, latest_image_path)

@app.route('/Image_c5')
def src_images_c5():
    
    def fetch_rtsp_image(rtsp_url, save_path):
    # Create a VideoCapture object with the RTSP URL
        cap = cv2.VideoCapture(rtsp_url)

        # Check if the camera stream is opened successfully
        if not cap.isOpened():
            print("Failed to open RTSP stream")
            return

        # Read a frame from the RTSP stream
        ret, frame = cap.read()

        # Release the VideoCapture object
        cap.release()

        # Check if a frame is successfully read
        if not ret:
            print("Failed to fetch frame from RTSP stream")
            return

        # Create the save directory if it doesn't exist
        os.makedirs(save_path, exist_ok=True)

        # Save the frame as an image
        image_path = os.path.join(save_path, "image.jpg")
        cv2.imwrite(image_path, frame)
        print("Image saved successfully:", image_path)

    # Example usage
    dflink = pd.read_csv('static/link.csv')
    rtsp_url = dflink.loc[4, 'Link']
    save_path = "static/images/camera5"
    fetch_rtsp_image(rtsp_url, save_path)
    
    base_dir = 'static/images/camera5'

    # Get the list of image files within the latest folder
    image_files = os.listdir(base_dir)
    image_files.sort(key=lambda x: os.path.getmtime(os.path.join(base_dir, x)), reverse=True)
    latest_image_filename = image_files[0]

    latest_image_path = latest_image_filename.replace("\\", "/")
  
    return send_from_directory(base_dir, latest_image_path)

@app.route('/upload', methods=['POST'])
def upload():

    sheet_name = request.form.get('sheet_name')
    sheet_link = request.form.get('sheet_link')
    file = request.files.get('file')

    dfsheets = pd.read_csv('static/Sheets.csv')
    row_data = {
            'Name': sheet_name,
            'Link': sheet_link,
        }

    dfsheets.loc[0] = row_data
    # Save the DataFrame to a CSV file
    dfsheets.to_csv('static/Sheets.csv', mode='w', index=False)
    
    # Save file to static folder
    if file:
        filename = file.filename
        file.save(os.path.join('static', filename))

    return redirect('/')

@app.route('/upload_function_c1', methods=['POST', 'GET'])
def upload_function_c1():
    global last_data1, last_data2, last_data3, last_data4, last_data5
    
    existing_data = pd.read_csv('static/data2.csv')
    last_data1 = existing_data.iloc[0] if not existing_data.empty else None
    last_data2 = existing_data.iloc[1] if len(existing_data) >= 2 else None
    last_data3 = existing_data.iloc[2] if len(existing_data) >= 3 else None
    last_data4 = existing_data.iloc[3] if len(existing_data) >= 4 else None
    last_data5 = existing_data.iloc[4] if len(existing_data) >= 5 else None
    
    last_data = [last_data1, last_data2, last_data3, last_data4, last_data5]
    draw_status = False
    for data in last_data:
        if data is not None:
            draw_status = True  # Update draw_status to True if any non-None element is present
            break  # Exit the loop after finding a non-None element
    ip_c1 = existing_data.loc[0, 'IP'] if not existing_data.empty else None    
    dfsheets = pd.read_csv('static/Sheets.csv')
    if not dfsheets.empty:
        sheets_link = dfsheets.loc[0, 'Link']
    else:
        sheets_link = ""
    
    #sheets_link = sheets_link.rsplit('/',1)[0] + '/export?format=csv'
    
    if request.method == 'POST':
        selected_functions_c1 = request.form.getlist('function_c1')  # Get the selected functions as a list

        # Store the selected functions in the session
        session['selected_functions'] = selected_functions_c1

        # Initialize the status dictionary
        status_data = {
            'IP': ip_c1,
            'function_congun': 'no',
            'function_count_people': 'no'
        }

        # Update the status dictionary based on selected functions
        if 'congun' in selected_functions_c1:
            status_data['function_congun'] = 'yes'
        if 'count-people' in selected_functions_c1:
            status_data['function_count_people'] = 'yes'

        # Read the existing status DataFrame
        df_status = pd.read_csv('static/status_function.csv')

        # Update the first row with the new status data
        df_status.loc[0] = status_data

        # Save the DataFrame to a CSV file
        df_status.to_csv('static/status_function.csv', mode='w', index=False)

        print("camera1:", ", ".join(selected_functions_c1))

        # Add your code to run scripts based on selected functions here
    else:
        # Handle GET request to populate the selected_functions
        selected_functions_c1 = session.get('selected_functions_c1', [])
        
    df_status = pd.read_csv('static/status_function.csv')
    status_c2_congun = df_status.loc[1, 'function_congun'] if len(df_status) >= 2 else None
    status_c2_count_people = df_status.loc[1, 'function_count_people'] if len(df_status) >= 2 else None
    selected_functions_c2 = []

    # Check status_c1_congun and add 'congun' to selected_functions_c1 if 'yes'
    if status_c2_congun == 'yes':
        selected_functions_c2.append('congun')

    # Check status_c1_count_people and add 'count-people' to selected_functions_c1 if 'yes'
    if status_c2_count_people == 'yes':
        selected_functions_c2.append('count-people')    

    # Render the template with the selected function value
    return render_template('index.html', last_data1=last_data1, last_data2=last_data2, 
                           last_data3=last_data3, last_data4=last_data4, last_data5=last_data5, 
                           draw_status=draw_status, 
                           selected_functions_c1=selected_functions_c1,
                           selected_functions_c2=selected_functions_c2)

@app.route('/upload_function_c2', methods=['POST', 'GET'])
def upload_function_c2():
    global last_data1, last_data2, last_data3, last_data4, last_data5
    
    existing_data = pd.read_csv('static/data2.csv')
    last_data1 = existing_data.iloc[0] if not existing_data.empty else None
    last_data2 = existing_data.iloc[1] if len(existing_data) >= 2 else None
    last_data3 = existing_data.iloc[2] if len(existing_data) >= 3 else None
    last_data4 = existing_data.iloc[3] if len(existing_data) >= 4 else None
    last_data5 = existing_data.iloc[4] if len(existing_data) >= 5 else None
    
    last_data = [last_data1, last_data2, last_data3, last_data4, last_data5]
    draw_status = False
    for data in last_data:
        if data is not None:
            draw_status = True  # Update draw_status to True if any non-None element is present
            break  # Exit the loop after finding a non-None element
    ip_c2 = existing_data.loc[1, 'IP'] if len(existing_data) >= 2 else None   
    dfsheets = pd.read_csv('static/Sheets.csv')
    if not dfsheets.empty:
        sheets_link = dfsheets.loc[0, 'Link']
    else:
        sheets_link = ""
    
    #sheets_link = sheets_link.rsplit('/',1)[0] + '/export?format=csv'
    
    if request.method == 'POST':
        selected_functions_c2 = request.form.getlist('function_c2')  # Get the selected functions as a list

        # Store the selected functions in the session
        session['selected_functions'] = selected_functions_c2

        # Initialize the status dictionary
        status_data = {
            'IP': ip_c2,
            'function_congun': 'no',
            'function_count_people': 'no'
        }

        # Update the status dictionary based on selected functions
        if 'congun' in selected_functions_c2:
            status_data['function_congun'] = 'yes'
        if 'count-people' in selected_functions_c2:
            status_data['function_count_people'] = 'yes'

        # Read the existing status DataFrame
        df_status = pd.read_csv('static/status_function.csv')

        # Update the first row with the new status data
        df_status.loc[1] = status_data

        # Save the DataFrame to a CSV file
        df_status.to_csv('static/status_function.csv', mode='w', index=False)

        print("camera2:", ", ".join(selected_functions_c2))

        # Add your code to run scripts based on selected functions here
    else:
        # Handle GET request to populate the selected_functions
        selected_functions_c2 = session.get('selected_functions', [])

    df_status = pd.read_csv('static/status_function.csv')
    status_c1_congun = df_status.loc[0, 'function_congun'] if not df_status.empty else None
    status_c1_count_people = df_status.loc[0, 'function_count_people'] if not df_status.empty else None
    selected_functions_c1 = []

    # Check status_c1_congun and add 'congun' to selected_functions_c1 if 'yes'
    if status_c1_congun == 'yes':
        selected_functions_c1.append('congun')

    # Check status_c1_count_people and add 'count-people' to selected_functions_c1 if 'yes'
    if status_c1_count_people == 'yes':
        selected_functions_c1.append('count-people')
     
    # Render the template with the selected function value
    return render_template('index.html', last_data1=last_data1, last_data2=last_data2, last_data3=last_data3, 
                           last_data4=last_data4, last_data5=last_data5, 
                           draw_status=draw_status,
                           selected_functions_c1=selected_functions_c1, 
                           selected_functions_c2=selected_functions_c2)

@app.route('/upload_function_c3', methods=['POST', 'GET'])
def upload_function_c3():
    global last_data1, last_data2, last_data3, last_data4, last_data5
    
    existing_data = pd.read_csv('static/data2.csv')
    last_data1 = existing_data.iloc[0] if not existing_data.empty else None
    last_data2 = existing_data.iloc[1] if len(existing_data) >= 2 else None
    last_data3 = existing_data.iloc[2] if len(existing_data) >= 3 else None
    last_data4 = existing_data.iloc[3] if len(existing_data) >= 4 else None
    last_data5 = existing_data.iloc[4] if len(existing_data) >= 5 else None
    
    last_data = [last_data1, last_data2, last_data3, last_data4, last_data5]
    draw_status = False
    for data in last_data:
        if data is not None:
            draw_status = True  # Update draw_status to True if any non-None element is present
            break  # Exit the loop after finding a non-None element
    ip_c3 = existing_data.loc[2, 'IP'] if len(existing_data) >= 3 else None   
    dfsheets = pd.read_csv('static/Sheets.csv')
    if not dfsheets.empty:
        sheets_link = dfsheets.loc[0, 'Link']
    else:
        sheets_link = ""
    
    #sheets_link = sheets_link.rsplit('/',1)[0] + '/export?format=csv'
    
    if request.method == 'POST':
        selected_functions_c3 = request.form.getlist('function_c3')  # Get the selected functions as a list

        # Store the selected functions in the session
        session['selected_functions'] = selected_functions_c3

        # Initialize the status dictionary
        status_data = {
            'IP': ip_c3,
            'function_congun': 'no',
            'function_count_people': 'no'
        }

        # Update the status dictionary based on selected functions
        if 'congun' in selected_functions_c3:
            status_data['function_congun'] = 'yes'
        if 'count-people' in selected_functions_c3:
            status_data['function_count_people'] = 'yes'

        # Read the existing status DataFrame
        df_status = pd.read_csv('static/status_function.csv')

        # Update the first row with the new status data
        df_status.loc[2] = status_data

        # Save the DataFrame to a CSV file
        df_status.to_csv('static/status_function.csv', mode='w', index=False)

        print("camera3:", ", ".join(selected_functions_c3))

        # Add your code to run scripts based on selected functions here
    else:
        # Handle GET request to populate the selected_functions
        selected_functions_c3 = session.get('selected_functions', [])

    df_status = pd.read_csv('static/status_function.csv')
    status_c1_congun = df_status.loc[0, 'function_congun'] if not df_status.empty else None
    status_c1_count_people = df_status.loc[0, 'function_count_people'] if not df_status.empty else None
    selected_functions_c1 = []

    # Check status_c1_congun and add 'congun' to selected_functions_c1 if 'yes'
    if status_c1_congun == 'yes':
        selected_functions_c1.append('congun')

    # Check status_c1_count_people and add 'count-people' to selected_functions_c1 if 'yes'
    if status_c1_count_people == 'yes':
        selected_functions_c1.append('count-people')
     
    # Render the template with the selected function value
    return render_template('index.html', last_data1=last_data1, last_data2=last_data2, last_data3=last_data3, 
                           last_data4=last_data4, last_data5=last_data5, 
                           draw_status=draw_status,
                           selected_functions_c1=selected_functions_c1, 
                           selected_functions_c2=selected_functions_c3)
        
@app.route('/Sheets_old_video_results_list_c1')
def sheets_video_list_c1():
    existing_data = pd.read_csv('static/data2.csv')
    ip_data1 = existing_data.loc[0, 'IP'] if not existing_data.empty else None
    
    old_video_list = 'list_result.csv'
    csv_file_path = f'static/{old_video_list}'
    df = pd.read_csv(csv_file_path)
    
    # Check if ip_data1 is not None and filter df based on its value
    if ip_data1 is not None:
        filtered_df = df[df['IP'] == ip_data1]

        # Get the data from the filtered DataFrame
        date_values = filtered_df['Date'].tolist()
        IP_values = filtered_df['IP'].tolist()
        video_name_values = filtered_df['File_Name'].tolist()

        # Combine data into a list of tuples (index, date, video_name)
        data_to_display = [(index + 1, date, ip, video_name) for index, (date, ip, video_name) in enumerate(zip(date_values, IP_values, video_name_values))]

    else:
        # Handle the case when ip_data1 is None (no matching IP)
        data_to_display = []

    return render_template('sheet_old_videos_list_ui.html', data_to_display=data_to_display)

@app.route('/Sheets_old_video_results_list_c2')
def sheets_video_list_c2():
    existing_data = pd.read_csv('static/data2.csv')
    ip_data1 = existing_data.loc[1, 'IP'] if not existing_data.empty else None
    
    old_video_list = 'list_result.csv'
    csv_file_path = f'static/{old_video_list}'
    df = pd.read_csv(csv_file_path)
    
    # Check if ip_data1 is not None and filter df based on its value
    if ip_data1 is not None:
        filtered_df = df[df['IP'] == ip_data1]

        # Get the data from the filtered DataFrame
        date_values = filtered_df['Date'].tolist()
        IP_values = filtered_df['IP'].tolist()
        video_name_values = filtered_df['File_Name'].tolist()

        # Combine data into a list of tuples (index, date, video_name)
        data_to_display = [(index + 1, date, ip, video_name) for index, (date, ip, video_name) in enumerate(zip(date_values, IP_values, video_name_values))]

    else:
        # Handle the case when ip_data1 is None (no matching IP)
        data_to_display = []

    return render_template('sheet_old_videos_list_ui.html', data_to_display=data_to_display)


create_dash_application(app)

@app.route('/old_box_label')
def old_box_label():
    return render_template('old_box_label.html')

@app.route('/old_dash1', methods=['GET', 'POST'])
def old_dash1():
    
    existing_data = pd.read_csv('static/data2.csv')
    ip_data1 = existing_data.loc[0, 'IP'] if not existing_data.empty else None
    name_data1 = existing_data.loc[0, 'Name'] if not existing_data.empty else None
    row_num = existing_data.index[0] if not existing_data.empty else None
    print(row_num)
    dff = pd.DataFrame(columns=['cs'])
    client_side = request.args.get('cs') 
    csv_filename = f'./static/status_client_side.csv'
    dfclient_side = pd.read_csv(csv_filename)
    row_data = {
            'cs': client_side,
            'row_num': row_num,
        }
    dfclient_side.loc[0] = row_data
    dfclient_side.to_csv(csv_filename, mode='w', index=False)
    
    part = './static/result-csv'
    pattern = f'{ip_data1}{name_data1}*'
    full_pattern = os.path.join(part, pattern)
    matching_files = glob.glob(full_pattern)
    csvfiles = [os.path.join(file) for file in matching_files]
    num_files = len(csvfiles)
    print(f'The number of files in the list is: {num_files}')
    
    def get_duration_and_hour(month, day, hour):
        if month == 9 and day in range(27, 31) and hour in range(10, 22):
            return f'Sep {day} {"am" if hour < 12 else "pm"}', f'{hour}-{hour+1}.'
        elif month == 10 and day in range(0, 9) and hour in range(10, 22):
            return f'Oct {day} {"am" if hour < 12 else "pm"}', f'{hour}-{hour+1}.'
        else:
            return '', ''

    dff = pd.DataFrame(columns=['Unnamed: 0', 'round', 'idp', 'count', 'gender', 'category', 'distance', 'duration', 'hour', 'csv_name'])

    for i in csvfiles:
        data = pd.read_csv(i)
        
        # Extract the year, month, date, and hour from 'YYYYMMDDhh' format using regular expression
        match = re.search(r'2023(\d{2})(\d{2})(\d{2})', i)
        
        if match:
            month = int(match.group(1))
            day = int(match.group(2))
            hour = int(match.group(3))
            
            duration, hour_range = get_duration_and_hour(month, day, hour)
            
            data['duration'] = f'{duration}'
            data['hour'] = f'{hour_range}'
            data['csv_name'] = f'{i}'
            
        dff = dff.append(data)

    dff.sort_values(by='csv_name', inplace=True)
    tb = dff[['round', 'idp', 'duration', 'hour','count', 'gender', 'category', 'csv_name', 'distance', 'path']]
    print(tb)
    part_dash_csv = './static/final-result-csv/uploaded_video.csv'
    tb.to_csv(part_dash_csv, index=True)

    # ip = request.args.get('ip') 
    # file_name = request.args.get('file_name') 
    # final_result_csv_path = './static/final-result-csv/uploaded_video.csv'
    # path = './static/vid_storage/CCTV_Storage1/'
    # #csvfile = f'{path}{ip}/_final_result/{file_name}'
    # csvfile = f'{path}192.168.31.20/_final_result/192.168.31.20_20230928_181942.csv'
    
    # df = pd.read_csv(csvfile)
    # df.to_csv(final_result_csv_path, index=True)

    return redirect('/dash/')

@app.route('/old_dash2', methods=['GET', 'POST'])
def old_dash2():
    
    existing_data = pd.read_csv('static/data2.csv')
    ip_data2 = existing_data.loc[1, 'IP'] if not existing_data.empty else None
    name_data2 = existing_data.loc[1, 'Name'] if not existing_data.empty else None
    row_num = existing_data.index[1] if not existing_data.empty else None
    print(row_num)
    dff = pd.DataFrame(columns=['cs'])
    client_side = request.args.get('cs') 
    csv_filename = f'./static/status_client_side.csv'
    dfclient_side = pd.read_csv(csv_filename)
    row_data = {
            'cs': client_side,
            'row_num': row_num,
        }
    dfclient_side.loc[0] = row_data
    dfclient_side.to_csv(csv_filename, mode='w', index=False)
   
    part = './static/result-csv'
    pattern = f'{ip_data2}{name_data2}*'
    full_pattern = os.path.join(part, pattern)
    matching_files = glob.glob(full_pattern)
    csvfiles = [os.path.join(file) for file in matching_files]
    num_files = len(csvfiles)
    print(f'The number of files in the list is: {num_files}')
    def get_duration_and_hour(month, day, hour):
        if month == 9 and day in range(27, 31) and hour in range(10, 22):
            return f'Sep {day} {"am" if hour < 12 else "pm"}', f'{hour}-{hour+1}.'
        elif month == 10 and day in range(0, 9) and hour in range(10, 22):
            return f'Oct {day} {"am" if hour < 12 else "pm"}', f'{hour}-{hour+1}.'
        else:
            return '', ''

    dff = pd.DataFrame(columns=['Unnamed: 0', 'round', 'idp', 'count', 'gender', 'category', 'distance', 'duration', 'hour', 'csv_name'])

    for i in csvfiles:
        data = pd.read_csv(i)
        
        # Extract the year, month, date, and hour from 'YYYYMMDDhh' format using regular expression
        match = re.search(r'2023(\d{2})(\d{2})(\d{2})', i)
        
        if match:
            month = int(match.group(1))
            day = int(match.group(2))
            hour = int(match.group(3))
            
            duration, hour_range = get_duration_and_hour(month, day, hour)
            
            data['duration'] = f'{duration}'
            data['hour'] = f'{hour_range}'
            data['csv_name'] = f'{i}'
            
        dff = dff.append(data)

    dff.sort_values(by='csv_name', inplace=True)
    tb = dff[['round', 'idp', 'duration', 'hour','count', 'gender', 'category', 'csv_name', 'distance', 'path']]
    print(tb)
    part_dash_csv = './static/final-result-csv/uploaded_video.csv'
    tb.to_csv(part_dash_csv, index=True)

    # ip = request.args.get('ip') 
    # file_name = request.args.get('file_name') 
    # final_result_csv_path = './static/final-result-csv/uploaded_video.csv'
    # path = './static/vid_storage/CCTV_Storage1/'
    # #csvfile = f'{path}{ip}/_final_result/{file_name}'
    # csvfile = f'{path}192.168.31.20/_final_result/192.168.31.20_20230928_181942.csv'
    
    # df = pd.read_csv(csvfile)
    # df.to_csv(final_result_csv_path, index=True)

    return redirect('/dash/')

@app.route('/Sheets')
def sheets():
    dfsheets = pd.read_csv('static/Sheets.csv')
    sheets_link = ""  # Assign an initial value

    #if not dfsheets.empty:
        #sheets_link = dfsheets.loc[0, 'Link']
        #sheets_link = sheets_link.rsplit('/', 1)[0] + '/export?format=csv'

        #response = requests.get(sheets_link)
        #csv_data = response.content.decode('utf-8')

        #df = pd.read_csv(io.StringIO(csv_data))
        #header = df.columns.tolist()
        #values = df.values.tolist()
    #else:
        #header = []
        #values = []

    return render_template('test_sheets_ui.html')#, header=header, values=values)

@app.route('/vdo/<uuid>')
def vdo(uuid):
    global process
    global save_mp4
    
    link_name = uuid
    print(uuid)
    if process is not None:
        process.terminate()

    process = subprocess.Popen(['python', 'python_script_person_pc_old.py', '-uuid', link_name])
    
    process.wait()

    base_dir = "static/vdo/avi/"
    save_dir = "static/vdo/mp4/"
    
    vdo_files = glob.glob(base_dir + "*.avi")
    vdo_files = [file.replace("\\", "/") for file in vdo_files]
    vdo_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    latest_vdo_filename = vdo_files[0]

    avi_path = latest_vdo_filename
    # Create the output file path with a .mp4 extension
    mp4_path = avi_path.rsplit('.', 1)[0] + '.mp4'
    vdo_name_mp4 = mp4_path.split('/')[-1]
    save_mp4 = f'{save_dir}{vdo_name_mp4}'

    # Load the AVI video and convert it to MP4
    video = VideoFileClip(avi_path)
    video.write_videofile(save_mp4, codec='libx264')
    print(save_mp4)
    
    # Simulate processing time (5 seconds delay)
    sleep(5)

    return redirect('/play')

@app.route('/play', methods=['GET', 'POST'])
def play():
    global save_mp4
    return render_template('play.html', save_mp4=save_mp4)

@app.route('/goback', methods=['POST'])
def goback():
    return redirect('/Sheets')

@app.route('/label')
def label():
    existing_data = pd.read_csv('static/data2.csv')
    last_data1 = existing_data.iloc[0] if not existing_data.empty else None
    return render_template('label1.html', last_data1=last_data1)

@app.route('/label_edit')
def label_edit():
    return render_template('label_edit.html', last_data1=last_data1)

@app.route('/label2')
def label2():
    existing_data = pd.read_csv('static/data2.csv')
    last_data2 = existing_data.iloc[1] if len(existing_data) >= 2 else None
    return render_template('label2.html', last_data2=last_data2)

@app.route('/label_edit2')
def label_edit2():
    return render_template('label_edit2.html', last_data2=last_data2)

@app.route('/label3')
def label3():
    existing_data = pd.read_csv('static/data2.csv')
    last_data3 = existing_data.iloc[2] if len(existing_data) >= 3 else None
    return render_template('label3.html', last_data3=last_data3)

@app.route('/label_edit3')
def label_edit3():
    return render_template('label_edit3.html', last_data3=last_data3)

@app.route('/label4')
def label4():
    existing_data = pd.read_csv('static/data2.csv')
    last_data4 = existing_data.iloc[3] if len(existing_data) >= 4 else None
    return render_template('label4.html', last_data4=last_data4)

@app.route('/label_edit4')
def label_edit4():
    return render_template('label_edit4.html', last_data4=last_data4)

@app.route('/label5')
def label5():
    existing_data = pd.read_csv('static/data2.csv')
    last_data5 = existing_data.iloc[4] if len(existing_data) >= 5 else None
    return render_template('label5.html', last_data5=last_data5)

@app.route('/label_edit5')
def label_edit5():
    return render_template('label_edit5.html', last_data5=last_data5)

@app.route('/save_shapes', methods=['POST'])
def save_shapes():
    global shape_data  # Access the global shape_data dictionary

    ip = request.form.get('ip1')
    
    type = request.form.get('type')
    x1 = request.form.get('x1')
    y1 = request.form.get('y1')
    x2 = request.form.get('x2')
    y2 = request.form.get('y2')
    x3 = request.form.get('x3')
    y3 = request.form.get('y3')
    x4 = request.form.get('x4')
    y4 = request.form.get('y4')
    up = request.form.get('up')
    left = request.form.get('left')
    right = request.form.get('right')
    down = request.form.get('down')

    shape_data['Type_box'] = type
    shape_data['X1'] = x1
    shape_data['Y1'] = y1
    shape_data['X2'] = x2
    shape_data['Y2'] = y2
    shape_data['X3'] = x3
    shape_data['Y3'] = y3
    shape_data['X4'] = x4
    shape_data['Y4'] = y4
    shape_data['Up to'] = up
    shape_data['Down to'] = down
    shape_data['Left to'] = left
    shape_data['Right to'] = right
    
    csv_filename = f'{ip}.csv'
    csv_path = os.path.join('static/output', csv_filename)
    
    # Clear the existing CSV file
    if os.path.exists(csv_path):
        os.remove(csv_path)

    # Create an empty DataFrame
    df = pd.DataFrame(columns=['Type_box', 'X1', 'Y1', 'X2', 'Y2', 'X3', 'Y3', 'X4', 'Y4', 'Up to', 'Down to', 'Left to', 'Right to'])
    
    row_data = {
            'Type_box': shape_data.get('Type_box', ''),
            'X1': shape_data.get('X1', ''),
            'Y1': shape_data.get('Y1', ''),
            'X2': shape_data.get('X2', ''),
            'Y2': shape_data.get('Y2', ''),
            'X3': shape_data.get('X3', ''),
            'Y3': shape_data.get('Y3', ''),
            'X4': shape_data.get('X4', ''),
            'Y4': shape_data.get('Y4', ''),
            'Up to': shape_data.get('Up to', ''),
            'Down to': shape_data.get('Down to', ''),
            'Left to': shape_data.get('Left to', ''),
            'Right to': shape_data.get('Right to', '')
        }
    df_output_csv = df.append(row_data, ignore_index=True)
        
    df_output_csv.to_csv(csv_path, mode='w', index=False)  
     
    df = pd.read_csv('static/data2.csv')

    if ip in df['IP'].values:
        # Update the row with the matching IP
        matching_row = df[df['IP'] == ip].index[0]
        df.loc[matching_row, 'Type_box'] = shape_data.get('Type_box', '')
        df.loc[matching_row, 'X1'] = shape_data.get('X1', '')
        df.loc[matching_row, 'Y1'] = shape_data.get('Y1', '')
        df.loc[matching_row, 'X2'] = shape_data.get('X2', '')
        df.loc[matching_row, 'Y2'] = shape_data.get('Y2', '')
        df.loc[matching_row, 'X3'] = shape_data.get('X3', '')
        df.loc[matching_row, 'Y3'] = shape_data.get('Y3', '')
        df.loc[matching_row, 'X4'] = shape_data.get('X4', '')
        df.loc[matching_row, 'Y4'] = shape_data.get('Y4', '')
        df.loc[matching_row, 'Up to'] = shape_data.get('Up to', '')
        df.loc[matching_row, 'Down to'] = shape_data.get('Down to', '')
        df.loc[matching_row, 'Left to'] = shape_data.get('Left to', '')
        df.loc[matching_row, 'Right to'] = shape_data.get('Right to', '')
    else:
        row_data = {
            'Username': '',
            'Password': '',
            'Name': '',
            'IP': ip,
            'Type_box': shape_data.get('Type_box', ''),
            'X1': shape_data.get('X1', ''),
            'Y1': shape_data.get('Y1', ''),
            'X2': shape_data.get('X2', ''),
            'Y2': shape_data.get('Y2', ''),
            'X3': shape_data.get('X3', ''),
            'Y3': shape_data.get('Y3', ''),
            'X4': shape_data.get('X4', ''),
            'Y4': shape_data.get('Y4', ''),
            'Up to': shape_data.get('Up to', ''),
            'Down to': shape_data.get('Down to', ''),
            'Left to': shape_data.get('Left to', ''),
            'Right to': shape_data.get('Right to', '')
        }
        df = df.append(row_data, ignore_index=True)
        
    df.to_csv('static/data2.csv', index=False)    
    
    return 'Saved shape successfully.'

@app.route('/save_shapes_edit1', methods=['POST'])
def save_shapes_edit1():
    global shape_data  # Access the global shape_data dictionary

    ip = request.form.get('ip1e')  # Retrieve the IP value from the IP input field

    type_box = request.form.get('type')
    x1 = request.form.get('x1')
    y1 = request.form.get('y1')
    x2 = request.form.get('x2')
    y2 = request.form.get('y2')
    x3 = request.form.get('x3')
    y3 = request.form.get('y3')
    x4 = request.form.get('x4')
    y4 = request.form.get('y4')
    up = request.form.get('up')
    left = request.form.get('left')
    right = request.form.get('right')
    down = request.form.get('down')

    shape_data['Type_box'] = type_box
    shape_data['X1'] = x1
    shape_data['Y1'] = y1
    shape_data['X2'] = x2
    shape_data['Y2'] = y2
    shape_data['X3'] = x3
    shape_data['Y3'] = y3
    shape_data['X4'] = x4
    shape_data['Y4'] = y4
    shape_data['Up to'] = up
    shape_data['Down to'] = down
    shape_data['Left to'] = left
    shape_data['Right to'] = right
    
    csv_filename = f'{ip}.csv'
    csv_path = os.path.join('static/output', csv_filename)
    
    # Clear the existing CSV file
    if os.path.exists(csv_path):
        os.remove(csv_path)

    # Create an empty DataFrame
    df = pd.DataFrame(columns=['Type_box', 'X1', 'Y1', 'X2', 'Y2', 'X3', 'Y3', 'X4', 'Y4', 'Up to', 'Down to', 'Left to', 'Right to'])
    
    row_data = {
            'Type_box': shape_data.get('Type_box', ''),
            'X1': shape_data.get('X1', ''),
            'Y1': shape_data.get('Y1', ''),
            'X2': shape_data.get('X2', ''),
            'Y2': shape_data.get('Y2', ''),
            'X3': shape_data.get('X3', ''),
            'Y3': shape_data.get('Y3', ''),
            'X4': shape_data.get('X4', ''),
            'Y4': shape_data.get('Y4', ''),
            'Up to': shape_data.get('Up to', ''),
            'Down to': shape_data.get('Down to', ''),
            'Left to': shape_data.get('Left to', ''),
            'Right to': shape_data.get('Right to', '')
        }
    df_output_csv = df.append(row_data, ignore_index=True)
        
    df_output_csv.to_csv(csv_path, mode='w', index=False)  
     
    df = pd.read_csv('static/data2.csv')

    if ip in df['IP'].values:
        # Update the row with the matching IP
        matching_row = df[df['IP'] == ip].index[0]
        df.loc[matching_row, 'Type_box'] = shape_data.get('Type_box', '')
        df.loc[matching_row, 'X1'] = shape_data.get('X1', '')
        df.loc[matching_row, 'Y1'] = shape_data.get('Y1', '')
        df.loc[matching_row, 'X2'] = shape_data.get('X2', '')
        df.loc[matching_row, 'Y2'] = shape_data.get('Y2', '')
        df.loc[matching_row, 'X3'] = shape_data.get('X3', '')
        df.loc[matching_row, 'Y3'] = shape_data.get('Y3', '')
        df.loc[matching_row, 'X4'] = shape_data.get('X4', '')
        df.loc[matching_row, 'Y4'] = shape_data.get('Y4', '')
        df.loc[matching_row, 'Up to'] = shape_data.get('Up to', '')
        df.loc[matching_row, 'Down to'] = shape_data.get('Down to', '')
        df.loc[matching_row, 'Left to'] = shape_data.get('Left to', '')
        df.loc[matching_row, 'Right to'] = shape_data.get('Right to', '')
    else:
        row_data = {
            'Username': '',
            'Password': '',
            'Name': '',
            'IP': ip,
            'Type_box': shape_data.get('Type_box', ''),
            'X1': shape_data.get('X1', ''),
            'Y1': shape_data.get('Y1', ''),
            'X2': shape_data.get('X2', ''),
            'Y2': shape_data.get('Y2', ''),
            'X3': shape_data.get('X3', ''),
            'Y3': shape_data.get('Y3', ''),
            'X4': shape_data.get('X4', ''),
            'Y4': shape_data.get('Y4', ''),
            'Up to': shape_data.get('Up to', ''),
            'Down to': shape_data.get('Down to', ''),
            'Left to': shape_data.get('Left to', ''),
            'Right to': shape_data.get('Right to', '')
        }
        df = df.append(row_data, ignore_index=True)
        
    df.to_csv('static/data2.csv', index=False)
    
    return 'Data updated successfully.'

@app.route('/save_shapes2', methods=['POST'])
def save_shapes2():
    global shape_data  # Access the global shape_data dictionary

    ip = request.form.get('ip2')
    
    type = request.form.get('type')
    x1 = request.form.get('x1')
    y1 = request.form.get('y1')
    x2 = request.form.get('x2')
    y2 = request.form.get('y2')
    x3 = request.form.get('x3')
    y3 = request.form.get('y3')
    x4 = request.form.get('x4')
    y4 = request.form.get('y4')
    up = request.form.get('up')
    left = request.form.get('left')
    right = request.form.get('right')
    down = request.form.get('down')

    shape_data['Type_box'] = type
    shape_data['X1'] = x1
    shape_data['Y1'] = y1
    shape_data['X2'] = x2
    shape_data['Y2'] = y2
    shape_data['X3'] = x3
    shape_data['Y3'] = y3
    shape_data['X4'] = x4
    shape_data['Y4'] = y4
    shape_data['Up to'] = up
    shape_data['Down to'] = down
    shape_data['Left to'] = left
    shape_data['Right to'] = right
    
    csv_filename = f'{ip}.csv'
    csv_path = os.path.join('static/output', csv_filename)
    
    # Clear the existing CSV file
    if os.path.exists(csv_path):
        os.remove(csv_path)

    # Create an empty DataFrame
    df = pd.DataFrame(columns=['Type_box', 'X1', 'Y1', 'X2', 'Y2', 'X3', 'Y3', 'X4', 'Y4', 'Up to', 'Down to', 'Left to', 'Right to'])
    
    row_data = {
            'Type_box': shape_data.get('Type_box', ''),
            'X1': shape_data.get('X1', ''),
            'Y1': shape_data.get('Y1', ''),
            'X2': shape_data.get('X2', ''),
            'Y2': shape_data.get('Y2', ''),
            'X3': shape_data.get('X3', ''),
            'Y3': shape_data.get('Y3', ''),
            'X4': shape_data.get('X4', ''),
            'Y4': shape_data.get('Y4', ''),
            'Up to': shape_data.get('Up to', ''),
            'Down to': shape_data.get('Down to', ''),
            'Left to': shape_data.get('Left to', ''),
            'Right to': shape_data.get('Right to', '')
        }
    df_output_csv = df.append(row_data, ignore_index=True)
        
    df_output_csv.to_csv(csv_path, mode='w', index=False)  
     
    df = pd.read_csv('static/data2.csv')

    if ip in df['IP'].values:
        # Update the row with the matching IP
        matching_row = df[df['IP'] == ip].index[0]
        df.loc[matching_row, 'Type_box'] = shape_data.get('Type_box', '')
        df.loc[matching_row, 'X1'] = shape_data.get('X1', '')
        df.loc[matching_row, 'Y1'] = shape_data.get('Y1', '')
        df.loc[matching_row, 'X2'] = shape_data.get('X2', '')
        df.loc[matching_row, 'Y2'] = shape_data.get('Y2', '')
        df.loc[matching_row, 'X3'] = shape_data.get('X3', '')
        df.loc[matching_row, 'Y3'] = shape_data.get('Y3', '')
        df.loc[matching_row, 'X4'] = shape_data.get('X4', '')
        df.loc[matching_row, 'Y4'] = shape_data.get('Y4', '')
        df.loc[matching_row, 'Up to'] = shape_data.get('Up to', '')
        df.loc[matching_row, 'Down to'] = shape_data.get('Down to', '')
        df.loc[matching_row, 'Left to'] = shape_data.get('Left to', '')
        df.loc[matching_row, 'Right to'] = shape_data.get('Right to', '')
    else:
        row_data = {
            'Username': '',
            'Password': '',
            'Name': '',
            'IP': ip,
            'Type_box': shape_data.get('Type_box', ''),
            'X1': shape_data.get('X1', ''),
            'Y1': shape_data.get('Y1', ''),
            'X2': shape_data.get('X2', ''),
            'Y2': shape_data.get('Y2', ''),
            'X3': shape_data.get('X3', ''),
            'Y3': shape_data.get('Y3', ''),
            'X4': shape_data.get('X4', ''),
            'Y4': shape_data.get('Y4', ''),
            'Up to': shape_data.get('Up to', ''),
            'Down to': shape_data.get('Down to', ''),
            'Left to': shape_data.get('Left to', ''),
            'Right to': shape_data.get('Right to', '')
        }
        df = df.append(row_data, ignore_index=True)
        
    df.to_csv('static/data2.csv', index=False)
    
    return 'Saved shape successfully.'

@app.route('/save_shapes_edit2', methods=['POST'])
def save_shapes_edit2():
    global shape_data  # Access the global shape_data dictionary

    ip = request.form.get('ip2e')  # Retrieve the IP value from the IP input field

    type_box = request.form.get('type')
    x1 = request.form.get('x1')
    y1 = request.form.get('y1')
    x2 = request.form.get('x2')
    y2 = request.form.get('y2')
    x3 = request.form.get('x3')
    y3 = request.form.get('y3')
    x4 = request.form.get('x4')
    y4 = request.form.get('y4')
    up = request.form.get('up')
    left = request.form.get('left')
    right = request.form.get('right')
    down = request.form.get('down')

    shape_data['Type_box'] = type_box
    shape_data['X1'] = x1
    shape_data['Y1'] = y1
    shape_data['X2'] = x2
    shape_data['Y2'] = y2
    shape_data['X3'] = x3
    shape_data['Y3'] = y3
    shape_data['X4'] = x4
    shape_data['Y4'] = y4
    shape_data['Up to'] = up
    shape_data['Down to'] = down
    shape_data['Left to'] = left
    shape_data['Right to'] = right
    
    csv_filename = f'{ip}.csv'
    csv_path = os.path.join('static/output', csv_filename)
    
    # Clear the existing CSV file
    if os.path.exists(csv_path):
        os.remove(csv_path)

    # Create an empty DataFrame
    df = pd.DataFrame(columns=['Type_box', 'X1', 'Y1', 'X2', 'Y2', 'X3', 'Y3', 'X4', 'Y4', 'Up to', 'Down to', 'Left to', 'Right to'])
    
    row_data = {
            'Type_box': shape_data.get('Type_box', ''),
            'X1': shape_data.get('X1', ''),
            'Y1': shape_data.get('Y1', ''),
            'X2': shape_data.get('X2', ''),
            'Y2': shape_data.get('Y2', ''),
            'X3': shape_data.get('X3', ''),
            'Y3': shape_data.get('Y3', ''),
            'X4': shape_data.get('X4', ''),
            'Y4': shape_data.get('Y4', ''),
            'Up to': shape_data.get('Up to', ''),
            'Down to': shape_data.get('Down to', ''),
            'Left to': shape_data.get('Left to', ''),
            'Right to': shape_data.get('Right to', '')
        }
    df_output_csv = df.append(row_data, ignore_index=True)
        
    df_output_csv.to_csv(csv_path, mode='w', index=False)  
     
    df = pd.read_csv('static/data2.csv')

    if ip in df['IP'].values:
        # Update the row with the matching IP
        matching_row = df[df['IP'] == ip].index[0]
        df.loc[matching_row, 'Type_box'] = shape_data.get('Type_box', '')
        df.loc[matching_row, 'X1'] = shape_data.get('X1', '')
        df.loc[matching_row, 'Y1'] = shape_data.get('Y1', '')
        df.loc[matching_row, 'X2'] = shape_data.get('X2', '')
        df.loc[matching_row, 'Y2'] = shape_data.get('Y2', '')
        df.loc[matching_row, 'X3'] = shape_data.get('X3', '')
        df.loc[matching_row, 'Y3'] = shape_data.get('Y3', '')
        df.loc[matching_row, 'X4'] = shape_data.get('X4', '')
        df.loc[matching_row, 'Y4'] = shape_data.get('Y4', '')
        df.loc[matching_row, 'Up to'] = shape_data.get('Up to', '')
        df.loc[matching_row, 'Down to'] = shape_data.get('Down to', '')
        df.loc[matching_row, 'Left to'] = shape_data.get('Left to', '')
        df.loc[matching_row, 'Right to'] = shape_data.get('Right to', '')
    else:
        row_data = {
            'Username': '',
            'Password': '',
            'Name': '',
            'IP': ip,
            'Type_box': shape_data.get('Type_box', ''),
            'X1': shape_data.get('X1', ''),
            'Y1': shape_data.get('Y1', ''),
            'X2': shape_data.get('X2', ''),
            'Y2': shape_data.get('Y2', ''),
            'X3': shape_data.get('X3', ''),
            'Y3': shape_data.get('Y3', ''),
            'X4': shape_data.get('X4', ''),
            'Y4': shape_data.get('Y4', ''),
            'Up to': shape_data.get('Up to', ''),
            'Down to': shape_data.get('Down to', ''),
            'Left to': shape_data.get('Left to', ''),
            'Right to': shape_data.get('Right to', '')
        }
        df = df.append(row_data, ignore_index=True)
        
    df.to_csv('static/data2.csv', index=False)
    
    return 'Data updated successfully.'

@app.route('/save_shapes3', methods=['POST'])
def save_shapes3():
    global shape_data  # Access the global shape_data dictionary

    ip = request.form.get('ip3')
    
    type = request.form.get('type')
    x1 = request.form.get('x1')
    y1 = request.form.get('y1')
    x2 = request.form.get('x2')
    y2 = request.form.get('y2')
    x3 = request.form.get('x3')
    y3 = request.form.get('y3')
    x4 = request.form.get('x4')
    y4 = request.form.get('y4')
    up = request.form.get('up')
    left = request.form.get('left')
    right = request.form.get('right')
    down = request.form.get('down')

    shape_data['Type_box'] = type
    shape_data['X1'] = x1
    shape_data['Y1'] = y1
    shape_data['X2'] = x2
    shape_data['Y2'] = y2
    shape_data['X3'] = x3
    shape_data['Y3'] = y3
    shape_data['X4'] = x4
    shape_data['Y4'] = y4
    shape_data['Up to'] = up
    shape_data['Down to'] = down
    shape_data['Left to'] = left
    shape_data['Right to'] = right
    
    csv_filename = f'{ip}.csv'
    csv_path = os.path.join('static/output', csv_filename)
    
    # Clear the existing CSV file
    if os.path.exists(csv_path):
        os.remove(csv_path)

    # Create an empty DataFrame
    df = pd.DataFrame(columns=['Type_box', 'X1', 'Y1', 'X2', 'Y2', 'X3', 'Y3', 'X4', 'Y4', 'Up to', 'Down to', 'Left to', 'Right to'])
    
    row_data = {
            'Type_box': shape_data.get('Type_box', ''),
            'X1': shape_data.get('X1', ''),
            'Y1': shape_data.get('Y1', ''),
            'X2': shape_data.get('X2', ''),
            'Y2': shape_data.get('Y2', ''),
            'X3': shape_data.get('X3', ''),
            'Y3': shape_data.get('Y3', ''),
            'X4': shape_data.get('X4', ''),
            'Y4': shape_data.get('Y4', ''),
            'Up to': shape_data.get('Up to', ''),
            'Down to': shape_data.get('Down to', ''),
            'Left to': shape_data.get('Left to', ''),
            'Right to': shape_data.get('Right to', '')
        }
    df_output_csv = df.append(row_data, ignore_index=True)
        
    df_output_csv.to_csv(csv_path, mode='w', index=False)  
     
    df = pd.read_csv('static/data2.csv')

    if ip in df['IP'].values:
        # Update the row with the matching IP
        matching_row = df[df['IP'] == ip].index[0]
        df.loc[matching_row, 'Type_box'] = shape_data.get('Type_box', '')
        df.loc[matching_row, 'X1'] = shape_data.get('X1', '')
        df.loc[matching_row, 'Y1'] = shape_data.get('Y1', '')
        df.loc[matching_row, 'X2'] = shape_data.get('X2', '')
        df.loc[matching_row, 'Y2'] = shape_data.get('Y2', '')
        df.loc[matching_row, 'X3'] = shape_data.get('X3', '')
        df.loc[matching_row, 'Y3'] = shape_data.get('Y3', '')
        df.loc[matching_row, 'X4'] = shape_data.get('X4', '')
        df.loc[matching_row, 'Y4'] = shape_data.get('Y4', '')
        df.loc[matching_row, 'Up to'] = shape_data.get('Up to', '')
        df.loc[matching_row, 'Down to'] = shape_data.get('Down to', '')
        df.loc[matching_row, 'Left to'] = shape_data.get('Left to', '')
        df.loc[matching_row, 'Right to'] = shape_data.get('Right to', '')
    else:
        row_data = {
            'Username': '',
            'Password': '',
            'Name': '',
            'IP': ip,
            'Type_box': shape_data.get('Type_box', ''),
            'X1': shape_data.get('X1', ''),
            'Y1': shape_data.get('Y1', ''),
            'X2': shape_data.get('X2', ''),
            'Y2': shape_data.get('Y2', ''),
            'X3': shape_data.get('X3', ''),
            'Y3': shape_data.get('Y3', ''),
            'X4': shape_data.get('X4', ''),
            'Y4': shape_data.get('Y4', ''),
            'Up to': shape_data.get('Up to', ''),
            'Down to': shape_data.get('Down to', ''),
            'Left to': shape_data.get('Left to', ''),
            'Right to': shape_data.get('Right to', '')
        }
        df = df.append(row_data, ignore_index=True)
        
    df.to_csv('static/data2.csv', index=False)
    
    return 'Saved shape successfully.'

@app.route('/save_shapes_edit3', methods=['POST'])
def save_shapes_edit3():
    global shape_data  # Access the global shape_data dictionary

    ip = request.form.get('ip3e')  # Retrieve the IP value from the IP input field

    type_box = request.form.get('type')
    x1 = request.form.get('x1')
    y1 = request.form.get('y1')
    x2 = request.form.get('x2')
    y2 = request.form.get('y2')
    x3 = request.form.get('x3')
    y3 = request.form.get('y3')
    x4 = request.form.get('x4')
    y4 = request.form.get('y4')
    up = request.form.get('up')
    left = request.form.get('left')
    right = request.form.get('right')
    down = request.form.get('down')

    shape_data['Type_box'] = type_box
    shape_data['X1'] = x1
    shape_data['Y1'] = y1
    shape_data['X2'] = x2
    shape_data['Y2'] = y2
    shape_data['X3'] = x3
    shape_data['Y3'] = y3
    shape_data['X4'] = x4
    shape_data['Y4'] = y4
    shape_data['Up to'] = up
    shape_data['Down to'] = down
    shape_data['Left to'] = left
    shape_data['Right to'] = right
    
    csv_filename = f'{ip}.csv'
    csv_path = os.path.join('static/output', csv_filename)
    
    # Clear the existing CSV file
    if os.path.exists(csv_path):
        os.remove(csv_path)

    # Create an empty DataFrame
    df = pd.DataFrame(columns=['Type_box', 'X1', 'Y1', 'X2', 'Y2', 'X3', 'Y3', 'X4', 'Y4', 'Up to', 'Down to', 'Left to', 'Right to'])
    
    row_data = {
            'Type_box': shape_data.get('Type_box', ''),
            'X1': shape_data.get('X1', ''),
            'Y1': shape_data.get('Y1', ''),
            'X2': shape_data.get('X2', ''),
            'Y2': shape_data.get('Y2', ''),
            'X3': shape_data.get('X3', ''),
            'Y3': shape_data.get('Y3', ''),
            'X4': shape_data.get('X4', ''),
            'Y4': shape_data.get('Y4', ''),
            'Up to': shape_data.get('Up to', ''),
            'Down to': shape_data.get('Down to', ''),
            'Left to': shape_data.get('Left to', ''),
            'Right to': shape_data.get('Right to', '')
        }
    df_output_csv = df.append(row_data, ignore_index=True)
        
    df_output_csv.to_csv(csv_path, mode='w', index=False)  
     
    df = pd.read_csv('static/data2.csv')

    if ip in df['IP'].values:
        # Update the row with the matching IP
        matching_row = df[df['IP'] == ip].index[0]
        df.loc[matching_row, 'Type_box'] = shape_data.get('Type_box', '')
        df.loc[matching_row, 'X1'] = shape_data.get('X1', '')
        df.loc[matching_row, 'Y1'] = shape_data.get('Y1', '')
        df.loc[matching_row, 'X2'] = shape_data.get('X2', '')
        df.loc[matching_row, 'Y2'] = shape_data.get('Y2', '')
        df.loc[matching_row, 'X3'] = shape_data.get('X3', '')
        df.loc[matching_row, 'Y3'] = shape_data.get('Y3', '')
        df.loc[matching_row, 'X4'] = shape_data.get('X4', '')
        df.loc[matching_row, 'Y4'] = shape_data.get('Y4', '')
        df.loc[matching_row, 'Up to'] = shape_data.get('Up to', '')
        df.loc[matching_row, 'Down to'] = shape_data.get('Down to', '')
        df.loc[matching_row, 'Left to'] = shape_data.get('Left to', '')
        df.loc[matching_row, 'Right to'] = shape_data.get('Right to', '')
    else:
        row_data = {
            'Username': '',
            'Password': '',
            'Name': '',
            'IP': ip,
            'Type_box': shape_data.get('Type_box', ''),
            'X1': shape_data.get('X1', ''),
            'Y1': shape_data.get('Y1', ''),
            'X2': shape_data.get('X2', ''),
            'Y2': shape_data.get('Y2', ''),
            'X3': shape_data.get('X3', ''),
            'Y3': shape_data.get('Y3', ''),
            'X4': shape_data.get('X4', ''),
            'Y4': shape_data.get('Y4', ''),
            'Up to': shape_data.get('Up to', ''),
            'Down to': shape_data.get('Down to', ''),
            'Left to': shape_data.get('Left to', ''),
            'Right to': shape_data.get('Right to', '')
        }
        df = df.append(row_data, ignore_index=True)
        
    df.to_csv('static/data2.csv', index=False)
    
    return 'Data updated successfully.'

@app.route('/save_shapes4', methods=['POST'])
def save_shapes4():
    global shape_data  # Access the global shape_data dictionary

    ip = request.form.get('ip4')
    
    type = request.form.get('type')
    x1 = request.form.get('x1')
    y1 = request.form.get('y1')
    x2 = request.form.get('x2')
    y2 = request.form.get('y2')
    x3 = request.form.get('x3')
    y3 = request.form.get('y3')
    x4 = request.form.get('x4')
    y4 = request.form.get('y4')
    up = request.form.get('up')
    left = request.form.get('left')
    right = request.form.get('right')
    down = request.form.get('down')

    shape_data['Type_box'] = type
    shape_data['X1'] = x1
    shape_data['Y1'] = y1
    shape_data['X2'] = x2
    shape_data['Y2'] = y2
    shape_data['X3'] = x3
    shape_data['Y3'] = y3
    shape_data['X4'] = x4
    shape_data['Y4'] = y4
    shape_data['Up to'] = up
    shape_data['Down to'] = down
    shape_data['Left to'] = left
    shape_data['Right to'] = right
    
    csv_filename = f'{ip}.csv'
    csv_path = os.path.join('static/output', csv_filename)
    
    # Clear the existing CSV file
    if os.path.exists(csv_path):
        os.remove(csv_path)

    # Create an empty DataFrame
    df = pd.DataFrame(columns=['Type_box', 'X1', 'Y1', 'X2', 'Y2', 'X3', 'Y3', 'X4', 'Y4', 'Up to', 'Down to', 'Left to', 'Right to'])
    
    row_data = {
            'Type_box': shape_data.get('Type_box', ''),
            'X1': shape_data.get('X1', ''),
            'Y1': shape_data.get('Y1', ''),
            'X2': shape_data.get('X2', ''),
            'Y2': shape_data.get('Y2', ''),
            'X3': shape_data.get('X3', ''),
            'Y3': shape_data.get('Y3', ''),
            'X4': shape_data.get('X4', ''),
            'Y4': shape_data.get('Y4', ''),
            'Up to': shape_data.get('Up to', ''),
            'Down to': shape_data.get('Down to', ''),
            'Left to': shape_data.get('Left to', ''),
            'Right to': shape_data.get('Right to', '')
        }
    df_output_csv = df.append(row_data, ignore_index=True)
        
    df_output_csv.to_csv(csv_path, mode='w', index=False)  
     
    df = pd.read_csv('static/data2.csv')

    if ip in df['IP'].values:
        # Update the row with the matching IP
        matching_row = df[df['IP'] == ip].index[0]
        df.loc[matching_row, 'Type_box'] = shape_data.get('Type_box', '')
        df.loc[matching_row, 'X1'] = shape_data.get('X1', '')
        df.loc[matching_row, 'Y1'] = shape_data.get('Y1', '')
        df.loc[matching_row, 'X2'] = shape_data.get('X2', '')
        df.loc[matching_row, 'Y2'] = shape_data.get('Y2', '')
        df.loc[matching_row, 'X3'] = shape_data.get('X3', '')
        df.loc[matching_row, 'Y3'] = shape_data.get('Y3', '')
        df.loc[matching_row, 'X4'] = shape_data.get('X4', '')
        df.loc[matching_row, 'Y4'] = shape_data.get('Y4', '')
        df.loc[matching_row, 'Up to'] = shape_data.get('Up to', '')
        df.loc[matching_row, 'Down to'] = shape_data.get('Down to', '')
        df.loc[matching_row, 'Left to'] = shape_data.get('Left to', '')
        df.loc[matching_row, 'Right to'] = shape_data.get('Right to', '')
    else:
        row_data = {
            'Username': '',
            'Password': '',
            'Name': '',
            'IP': ip,
            'Type_box': shape_data.get('Type_box', ''),
            'X1': shape_data.get('X1', ''),
            'Y1': shape_data.get('Y1', ''),
            'X2': shape_data.get('X2', ''),
            'Y2': shape_data.get('Y2', ''),
            'X3': shape_data.get('X3', ''),
            'Y3': shape_data.get('Y3', ''),
            'X4': shape_data.get('X4', ''),
            'Y4': shape_data.get('Y4', ''),
            'Up to': shape_data.get('Up to', ''),
            'Down to': shape_data.get('Down to', ''),
            'Left to': shape_data.get('Left to', ''),
            'Right to': shape_data.get('Right to', '')
        }
        df = df.append(row_data, ignore_index=True)
        
    df.to_csv('static/data2.csv', index=False)
    
    return 'Saved shape successfully.'

@app.route('/save_shapes_edit4', methods=['POST'])
def save_shapes_edit4():
    global shape_data  # Access the global shape_data dictionary

    ip = request.form.get('ip4e')  # Retrieve the IP value from the IP input field

    type_box = request.form.get('type')
    x1 = request.form.get('x1')
    y1 = request.form.get('y1')
    x2 = request.form.get('x2')
    y2 = request.form.get('y2')
    x3 = request.form.get('x3')
    y3 = request.form.get('y3')
    x4 = request.form.get('x4')
    y4 = request.form.get('y4')
    up = request.form.get('up')
    left = request.form.get('left')
    right = request.form.get('right')
    down = request.form.get('down')

    shape_data['Type_box'] = type_box
    shape_data['X1'] = x1
    shape_data['Y1'] = y1
    shape_data['X2'] = x2
    shape_data['Y2'] = y2
    shape_data['X3'] = x3
    shape_data['Y3'] = y3
    shape_data['X4'] = x4
    shape_data['Y4'] = y4
    shape_data['Up to'] = up
    shape_data['Down to'] = down
    shape_data['Left to'] = left
    shape_data['Right to'] = right
    
    csv_filename = f'{ip}.csv'
    csv_path = os.path.join('static/output', csv_filename)
    
    # Clear the existing CSV file
    if os.path.exists(csv_path):
        os.remove(csv_path)

    # Create an empty DataFrame
    df = pd.DataFrame(columns=['Type_box', 'X1', 'Y1', 'X2', 'Y2', 'X3', 'Y3', 'X4', 'Y4', 'Up to', 'Down to', 'Left to', 'Right to'])
    
    row_data = {
            'Type_box': shape_data.get('Type_box', ''),
            'X1': shape_data.get('X1', ''),
            'Y1': shape_data.get('Y1', ''),
            'X2': shape_data.get('X2', ''),
            'Y2': shape_data.get('Y2', ''),
            'X3': shape_data.get('X3', ''),
            'Y3': shape_data.get('Y3', ''),
            'X4': shape_data.get('X4', ''),
            'Y4': shape_data.get('Y4', ''),
            'Up to': shape_data.get('Up to', ''),
            'Down to': shape_data.get('Down to', ''),
            'Left to': shape_data.get('Left to', ''),
            'Right to': shape_data.get('Right to', '')
        }
    df_output_csv = df.append(row_data, ignore_index=True)
        
    df_output_csv.to_csv(csv_path, mode='w', index=False)  
     
    df = pd.read_csv('static/data2.csv')

    if ip in df['IP'].values:
        # Update the row with the matching IP
        matching_row = df[df['IP'] == ip].index[0]
        df.loc[matching_row, 'Type_box'] = shape_data.get('Type_box', '')
        df.loc[matching_row, 'X1'] = shape_data.get('X1', '')
        df.loc[matching_row, 'Y1'] = shape_data.get('Y1', '')
        df.loc[matching_row, 'X2'] = shape_data.get('X2', '')
        df.loc[matching_row, 'Y2'] = shape_data.get('Y2', '')
        df.loc[matching_row, 'X3'] = shape_data.get('X3', '')
        df.loc[matching_row, 'Y3'] = shape_data.get('Y3', '')
        df.loc[matching_row, 'X4'] = shape_data.get('X4', '')
        df.loc[matching_row, 'Y4'] = shape_data.get('Y4', '')
        df.loc[matching_row, 'Up to'] = shape_data.get('Up to', '')
        df.loc[matching_row, 'Down to'] = shape_data.get('Down to', '')
        df.loc[matching_row, 'Left to'] = shape_data.get('Left to', '')
        df.loc[matching_row, 'Right to'] = shape_data.get('Right to', '')
    else:
        row_data = {
            'Username': '',
            'Password': '',
            'Name': '',
            'IP': ip,
            'Type_box': shape_data.get('Type_box', ''),
            'X1': shape_data.get('X1', ''),
            'Y1': shape_data.get('Y1', ''),
            'X2': shape_data.get('X2', ''),
            'Y2': shape_data.get('Y2', ''),
            'X3': shape_data.get('X3', ''),
            'Y3': shape_data.get('Y3', ''),
            'X4': shape_data.get('X4', ''),
            'Y4': shape_data.get('Y4', ''),
            'Up to': shape_data.get('Up to', ''),
            'Down to': shape_data.get('Down to', ''),
            'Left to': shape_data.get('Left to', ''),
            'Right to': shape_data.get('Right to', '')
        }
        df = df.append(row_data, ignore_index=True)
        
    df.to_csv('static/data2.csv', index=False)
    
    return 'Data updated successfully.'

@app.route('/save_shapes5', methods=['POST'])
def save_shapes5():
    global shape_data  # Access the global shape_data dictionary

    ip = request.form.get('ip5')
    
    type = request.form.get('type')
    x1 = request.form.get('x1')
    y1 = request.form.get('y1')
    x2 = request.form.get('x2')
    y2 = request.form.get('y2')
    x3 = request.form.get('x3')
    y3 = request.form.get('y3')
    x4 = request.form.get('x4')
    y4 = request.form.get('y4')
    up = request.form.get('up')
    left = request.form.get('left')
    right = request.form.get('right')
    down = request.form.get('down')

    shape_data['Type_box'] = type
    shape_data['X1'] = x1
    shape_data['Y1'] = y1
    shape_data['X2'] = x2
    shape_data['Y2'] = y2
    shape_data['X3'] = x3
    shape_data['Y3'] = y3
    shape_data['X4'] = x4
    shape_data['Y4'] = y4
    shape_data['Up to'] = up
    shape_data['Down to'] = down
    shape_data['Left to'] = left
    shape_data['Right to'] = right
    
    csv_filename = f'{ip}.csv'
    csv_path = os.path.join('static/output', csv_filename)
    
    # Clear the existing CSV file
    if os.path.exists(csv_path):
        os.remove(csv_path)

    # Create an empty DataFrame
    df = pd.DataFrame(columns=['Type_box', 'X1', 'Y1', 'X2', 'Y2', 'X3', 'Y3', 'X4', 'Y4', 'Up to', 'Down to', 'Left to', 'Right to'])
    
    row_data = {
            'Type_box': shape_data.get('Type_box', ''),
            'X1': shape_data.get('X1', ''),
            'Y1': shape_data.get('Y1', ''),
            'X2': shape_data.get('X2', ''),
            'Y2': shape_data.get('Y2', ''),
            'X3': shape_data.get('X3', ''),
            'Y3': shape_data.get('Y3', ''),
            'X4': shape_data.get('X4', ''),
            'Y4': shape_data.get('Y4', ''),
            'Up to': shape_data.get('Up to', ''),
            'Down to': shape_data.get('Down to', ''),
            'Left to': shape_data.get('Left to', ''),
            'Right to': shape_data.get('Right to', '')
        }
    df_output_csv = df.append(row_data, ignore_index=True)
        
    df_output_csv.to_csv(csv_path, mode='w', index=False)  
     
    df = pd.read_csv('static/data2.csv')

    if ip in df['IP'].values:
        # Update the row with the matching IP
        matching_row = df[df['IP'] == ip].index[0]
        df.loc[matching_row, 'Type_box'] = shape_data.get('Type_box', '')
        df.loc[matching_row, 'X1'] = shape_data.get('X1', '')
        df.loc[matching_row, 'Y1'] = shape_data.get('Y1', '')
        df.loc[matching_row, 'X2'] = shape_data.get('X2', '')
        df.loc[matching_row, 'Y2'] = shape_data.get('Y2', '')
        df.loc[matching_row, 'X3'] = shape_data.get('X3', '')
        df.loc[matching_row, 'Y3'] = shape_data.get('Y3', '')
        df.loc[matching_row, 'X4'] = shape_data.get('X4', '')
        df.loc[matching_row, 'Y4'] = shape_data.get('Y4', '')
        df.loc[matching_row, 'Up to'] = shape_data.get('Up to', '')
        df.loc[matching_row, 'Down to'] = shape_data.get('Down to', '')
        df.loc[matching_row, 'Left to'] = shape_data.get('Left to', '')
        df.loc[matching_row, 'Right to'] = shape_data.get('Right to', '')
    else:
        row_data = {
            'Username': '',
            'Password': '',
            'Name': '',
            'IP': ip,
            'Type_box': shape_data.get('Type_box', ''),
            'X1': shape_data.get('X1', ''),
            'Y1': shape_data.get('Y1', ''),
            'X2': shape_data.get('X2', ''),
            'Y2': shape_data.get('Y2', ''),
            'X3': shape_data.get('X3', ''),
            'Y3': shape_data.get('Y3', ''),
            'X4': shape_data.get('X4', ''),
            'Y4': shape_data.get('Y4', ''),
            'Up to': shape_data.get('Up to', ''),
            'Down to': shape_data.get('Down to', ''),
            'Left to': shape_data.get('Left to', ''),
            'Right to': shape_data.get('Right to', '')
        }
        df = df.append(row_data, ignore_index=True)
        
    df.to_csv('static/data2.csv', index=False)
    
    return 'Saved shape successfully.'

@app.route('/save_shapes_edit5', methods=['POST'])
def save_shapes_edit5():
    global shape_data  # Access the global shape_data dictionary

    ip = request.form.get('ip5e')  # Retrieve the IP value from the IP input field

    type_box = request.form.get('type')
    x1 = request.form.get('x1')
    y1 = request.form.get('y1')
    x2 = request.form.get('x2')
    y2 = request.form.get('y2')
    x3 = request.form.get('x3')
    y3 = request.form.get('y3')
    x4 = request.form.get('x4')
    y4 = request.form.get('y4')
    up = request.form.get('up')
    left = request.form.get('left')
    right = request.form.get('right')
    down = request.form.get('down')

    shape_data['Type_box'] = type_box
    shape_data['X1'] = x1
    shape_data['Y1'] = y1
    shape_data['X2'] = x2
    shape_data['Y2'] = y2
    shape_data['X3'] = x3
    shape_data['Y3'] = y3
    shape_data['X4'] = x4
    shape_data['Y4'] = y4
    shape_data['Up to'] = up
    shape_data['Down to'] = down
    shape_data['Left to'] = left
    shape_data['Right to'] = right
    
    csv_filename = f'{ip}.csv'
    csv_path = os.path.join('static/output', csv_filename)
    
    # Clear the existing CSV file
    if os.path.exists(csv_path):
        os.remove(csv_path)

    # Create an empty DataFrame
    df = pd.DataFrame(columns=['Type_box', 'X1', 'Y1', 'X2', 'Y2', 'X3', 'Y3', 'X4', 'Y4', 'Up to', 'Down to', 'Left to', 'Right to'])
    
    row_data = {
            'Type_box': shape_data.get('Type_box', ''),
            'X1': shape_data.get('X1', ''),
            'Y1': shape_data.get('Y1', ''),
            'X2': shape_data.get('X2', ''),
            'Y2': shape_data.get('Y2', ''),
            'X3': shape_data.get('X3', ''),
            'Y3': shape_data.get('Y3', ''),
            'X4': shape_data.get('X4', ''),
            'Y4': shape_data.get('Y4', ''),
            'Up to': shape_data.get('Up to', ''),
            'Down to': shape_data.get('Down to', ''),
            'Left to': shape_data.get('Left to', ''),
            'Right to': shape_data.get('Right to', '')
        }
    df_output_csv = df.append(row_data, ignore_index=True)
        
    df_output_csv.to_csv(csv_path, mode='w', index=False)  
     
    df = pd.read_csv('static/data2.csv')

    if ip in df['IP'].values:
        # Update the row with the matching IP
        matching_row = df[df['IP'] == ip].index[0]
        df.loc[matching_row, 'Type_box'] = shape_data.get('Type_box', '')
        df.loc[matching_row, 'X1'] = shape_data.get('X1', '')
        df.loc[matching_row, 'Y1'] = shape_data.get('Y1', '')
        df.loc[matching_row, 'X2'] = shape_data.get('X2', '')
        df.loc[matching_row, 'Y2'] = shape_data.get('Y2', '')
        df.loc[matching_row, 'X3'] = shape_data.get('X3', '')
        df.loc[matching_row, 'Y3'] = shape_data.get('Y3', '')
        df.loc[matching_row, 'X4'] = shape_data.get('X4', '')
        df.loc[matching_row, 'Y4'] = shape_data.get('Y4', '')
        df.loc[matching_row, 'Up to'] = shape_data.get('Up to', '')
        df.loc[matching_row, 'Down to'] = shape_data.get('Down to', '')
        df.loc[matching_row, 'Left to'] = shape_data.get('Left to', '')
        df.loc[matching_row, 'Right to'] = shape_data.get('Right to', '')
    else:
        row_data = {
            'Username': '',
            'Password': '',
            'Name': '',
            'IP': ip,
            'Type_box': shape_data.get('Type_box', ''),
            'X1': shape_data.get('X1', ''),
            'Y1': shape_data.get('Y1', ''),
            'X2': shape_data.get('X2', ''),
            'Y2': shape_data.get('Y2', ''),
            'X3': shape_data.get('X3', ''),
            'Y3': shape_data.get('Y3', ''),
            'X4': shape_data.get('X4', ''),
            'Y4': shape_data.get('Y4', ''),
            'Up to': shape_data.get('Up to', ''),
            'Down to': shape_data.get('Down to', ''),
            'Left to': shape_data.get('Left to', ''),
            'Right to': shape_data.get('Right to', '')
        }
        df = df.append(row_data, ignore_index=True)
        
    df.to_csv('static/data2.csv', index=False)
    
    return 'Data updated successfully.'

@app.route('/submit1', methods=['POST'])
def submit():
    global df1, shape_data, process  # Access the global DataFrame and shape_data dictionary

    df1 = pd.read_csv('static/data2.csv')
    df1link = pd.read_csv('static/link.csv')
    df1_ipimage = pd.read_csv('static/Images_IP.csv')
    
    # Retrieve the data from the form
    username = request.form['username1']
    password = request.form['password1']
    name = request.form['name1']
    ip = request.form['ip1']

    if 'draw' in request.form:
        
        row_data = {
            'Username': username,
            'Password': password,
            'Name': name,
            'IP': ip,
            'Type_box': shape_data.get('Type_box', ''),
            'X1': shape_data.get('X1', ''),
            'Y1': shape_data.get('Y1', ''),
            'X2': shape_data.get('X2', ''),
            'Y2': shape_data.get('Y2', ''),
            'X3': shape_data.get('X3', ''),
            'Y3': shape_data.get('Y3', ''),
            'X4': shape_data.get('X4', ''),
            'Y4': shape_data.get('Y4', '')
        }

        # Append the combined data to the DataFrame
        df1 = df1.append(row_data, ignore_index=True)

        # Clear the shape_data dictionary for the next submission
        shape_data = {}
    
        # Save the DataFrame to a CSV file
        df1.to_csv('static/data2.csv', mode='w', index=False)
        
        image = "/Image_c1"
        if image in df1_ipimage['/Images'].values:
            matching_row = df1_ipimage[df1_ipimage['/Images'] == image].index[0]
            df1_ipimage.loc[matching_row, 'IP'] = ip
        else:
            
            row_data_ipimage = {
                'IP' : ip,
                '/Images' : "/Image_c1"
            }
            df1_ipimage = df1_ipimage.append(row_data_ipimage, ignore_index=True)
        shape_data = {}
        df1_ipimage.to_csv('static/Images_IP.csv', index=False)
        
        df_status = pd.read_csv('static/status_function.csv')
        status_c1_congun = df_status.loc[0, 'function_congun'] if not df_status.empty else None
        status_c1_count_people = df_status.loc[0, 'function_count_people'] if not df_status.empty else None

        # Check status_c1_congun and add 'congun' to selected_functions_c1 if 'yes'
        if status_c1_congun == 'yes':
            csv_filename = f'./static/link_congun.csv'
            df1link_congun = pd.read_csv(csv_filename)
            row_data_link = {
                'Name' : name,
                'Link' : f"rtsp://{username}:{password}@{ip}/Streaming/Channels/101/"
            }
            df1link_congun = df1link_congun.append(row_data_link, ignore_index=True)
            shape_data = {}
            df1link_congun.to_csv(csv_filename, mode='w', index=False)
        # Check status_c1_count_people and add 'count-people' to selected_functions_c1 if 'yes'
        if status_c1_count_people == 'yes':
            csv_filename = f'./static/link_count_people.csv'
            df1link_count_people = pd.read_csv(csv_filename)
            row_data_link = {
                'Name' : name,
                'Link' : f"rtsp://{username}:{password}@{ip}/Streaming/Channels/101/"
            }
            df1link_count_people = df1link_count_people.append(row_data_link, ignore_index=True)
            shape_data = {}
            df1link_count_people.to_csv(csv_filename, mode='w', index=False)

        link = f"rtsp://{username}:{password}@{ip}/Streaming/Channels/101/"
        row_data_link = {
            'Name': name,
            'Link': link
        }
        if link in df1link['Link'].values:
            matching_row = df1link[df1link['Link'] == link].index[0]
            df1link.loc[matching_row, 'Name'] = name
        else:
            df1link = df1link.append(row_data_link, ignore_index=True)
        
        shape_data = {}
        df1link.to_csv('static/link.csv', mode='w', index=False)
        
        return redirect('/label')
    
    # Check if the IP already exists in the DataFrame
    if ip in df1['IP'].values:
        # Update the row with the matching IP
        matching_row = df1[df1['IP'] == ip].index[0]
        df1.loc[matching_row, 'Username'] = username
        df1.loc[matching_row, 'Password'] = password
        df1.loc[matching_row, 'Name'] = name
        df1.loc[matching_row, 'Type_box'] = shape_data.get('Type_box', '')
        df1.loc[matching_row, 'X1'] = shape_data.get('X1', '')
        df1.loc[matching_row, 'Y1'] = shape_data.get('Y1', '')
        df1.loc[matching_row, 'X2'] = shape_data.get('X2', '')
        df1.loc[matching_row, 'Y2'] = shape_data.get('Y2', '')
        df1.loc[matching_row, 'X3'] = shape_data.get('X3', '')
        df1.loc[matching_row, 'Y3'] = shape_data.get('Y3', '')
        df1.loc[matching_row, 'X4'] = shape_data.get('X4', '')
        df1.loc[matching_row, 'Y4'] = shape_data.get('Y4', '')
    else:
        # Combine the form submission data and shape data into a single dictionary
        row_data = {
            'Username': username,
            'Password': password,
            'Name': name,
            'IP': ip,
            'Type_box': shape_data.get('Type_box', ''),
            'X1': shape_data.get('X1', ''),
            'Y1': shape_data.get('Y1', ''),
            'X2': shape_data.get('X2', ''),
            'Y2': shape_data.get('Y2', ''),
            'X3': shape_data.get('X3', ''),
            'Y3': shape_data.get('Y3', ''),
            'X4': shape_data.get('X4', ''),
            'Y4': shape_data.get('Y4', '')
        }

        # Append the combined data to the DataFrame
        df1 = df1.append(row_data, ignore_index=True)

    # Clear the shape_data dictionary for the next submission
    shape_data = {}

    # Save the DataFrame to a CSV file
    df1.to_csv('static/data2.csv', mode='w', index=False)
    
    
    df_status = pd.read_csv('static/status_function.csv')
    status_c1_congun = df_status.loc[0, 'function_congun'] if not df_status.empty else None
    status_c1_count_people = df_status.loc[0, 'function_count_people'] if not df_status.empty else None

    # Check status_c1_congun and add 'congun' to selected_functions_c1 if 'yes'
    if status_c1_congun == 'yes':
        csv_filename = f'./static/link_congun.csv'
        df1link_congun = pd.read_csv(csv_filename)
        link = f"rtsp://{username}:{password}@{ip}/Streaming/Channels/101/"
        row_data_link = {
                'Name' : name,
                'Link' : link
            }
        if link in df1link_congun['Link'].values:
            matching_row = df1link_congun[df1link_congun['Link'] == link].index[0]
            df1link_congun.loc[matching_row, 'Name'] = name
        else:
            df1link_congun = df1link_congun.append(row_data_link, ignore_index=True)
        shape_data = {}
        df1link_congun.to_csv(csv_filename, mode='w', index=False)
        
    # Check status_c1_count_people and add 'count-people' to selected_functions_c1 if 'yes'
    if status_c1_count_people == 'yes':
        csv_filename = f'./static/link_count_people.csv'
        df1link_count_people = pd.read_csv(csv_filename)
        link = f"rtsp://{username}:{password}@{ip}/Streaming/Channels/101/"
        row_data_link = {
                'Name' : name,
                'Link' : link
            }
        if link in df1link_count_people['Link'].values:
            matching_row = df1link_count_people[df1link_count_people['Link'] == link].index[0]
            df1link_count_people.loc[matching_row, 'Name'] = name
        else:
            df1link_count_people = df1link_count_people.append(row_data_link, ignore_index=True)
        shape_data = {}
        df1link_count_people.to_csv(csv_filename, mode='w', index=False)
              
    link = f"rtsp://{username}:{password}@{ip}/Streaming/Channels/101/"
    row_data_link = {
        'Name': name,
        'Link': link
    }
    if link in df1link['Link'].values:
        matching_row = df1link[df1link['Link'] == link].index[0]
        df1link.loc[matching_row, 'Name'] = name
    else:
        df1link = df1link.append(row_data_link, ignore_index=True)
        
    shape_data = {}
    df1link.to_csv('static/link.csv', mode='w', index=False)

    if status_c1_congun == 'yes':
        if process is not None:
            process.terminate()
        conda_env = "openmmposep3.8"
        #'conda', 'run', '-n', f'{conda_env}', 
        command = ['python', 'Multi-RecordingCCTV-CV.py']
        print(command)
        process_congun = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out_coungun, err_congun = process_congun.communicate()
        
        print("Process congun Output:")
        print(out_coungun.decode('utf-8'))  
        print("Process congun Error:")
        print(err_congun.decode('utf-8'))  
        
    if status_c1_count_people == 'yes':
        if process is not None:
            process.terminate()
        conda_env = "yolop3.9"
        #'conda', 'run', '-n', f'{conda_env}', 
        command = ['python', 'python_script_runcount_EffNet_Jetson_Demo_26Dec23.py', '-second', '2', '-f', str(20), '-img_save', 'not_all']
        print(command)
        process_count = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out_count, err_count = process_count.communicate()

        print("Process count Output:")
        print(out_count.decode('utf-8'))  
        print("Process count Error:")
        print(err_count.decode('utf-8'))  

    return redirect('/')

@app.route('/submit2', methods=['POST'])
def submit2():
    global df2, shape_data, process  

    df2 = pd.read_csv('static/data2.csv')
    df2link = pd.read_csv('static/link.csv')
    df2_ipimage = pd.read_csv('static/Images_IP.csv')
 
    username = request.form['username2']
    password = request.form['password2']
    name = request.form['name2']
    ip = request.form['ip2']
    
    if 'draw' in request.form:
        
        row_data = {
            'Username': username,
            'Password': password,
            'Name': name,
            'IP': ip,
            'Type_box': shape_data.get('Type_box', ''),
            'X1': shape_data.get('X1', ''),
            'Y1': shape_data.get('Y1', ''),
            'X2': shape_data.get('X2', ''),
            'Y2': shape_data.get('Y2', ''),
            'X3': shape_data.get('X3', ''),
            'Y3': shape_data.get('Y3', ''),
            'X4': shape_data.get('X4', ''),
            'Y4': shape_data.get('Y4', '')
        }

        df2 = df2.append(row_data, ignore_index=True)

        shape_data = {}

        df2.to_csv('static/data2.csv', mode='w', index=False)
        
        image = "/Image_c2"
        if image in df2_ipimage['/Images'].values:
            matching_row = df2_ipimage[df2_ipimage['/Images'] == image].index[0]
            df2_ipimage.loc[matching_row, 'IP'] = ip
        else:
            
            row_data_ipimage = {
                'IP' : ip,
                '/Images' : "/Image_c2"
            }
            df2_ipimage = df2_ipimage.append(row_data_ipimage, ignore_index=True)
        shape_data = {}
        df2_ipimage.to_csv('static/Images_IP.csv', index=False)
        
        df_status = pd.read_csv('static/status_function.csv')
        status_c2_congun = df_status.loc[1, 'function_congun'] if not df_status.empty else None
        status_c2_count_people = df_status.loc[1, 'function_count_people'] if not df_status.empty else None

        # Check status_c1_congun and add 'congun' to selected_functions_c1 if 'yes'
        if status_c2_congun == 'yes':
            csv_filename = f'./static/link_congun.csv'
            df2link_congun = pd.read_csv(csv_filename)
            row_data_link = {
                'Name' : name,
                'Link' : f"rtsp://{username}:{password}@{ip}/Streaming/Channels/101/"
            }
            df2link_congun = df2link_congun.append(row_data_link, ignore_index=True)
            shape_data = {}
            df2link_congun.to_csv(csv_filename, mode='w', index=False)
        # Check status_c1_count_people and add 'count-people' to selected_functions_c1 if 'yes'
        if status_c2_count_people == 'yes':
            csv_filename = f'./static/link_count_people.csv'
            df2link_count_people = pd.read_csv(csv_filename)
            row_data_link = {
                'Name' : name,
                'Link' : f"rtsp://{username}:{password}@{ip}/Streaming/Channels/101/"
            }
            df2link_count_people = df2link_count_people.append(row_data_link, ignore_index=True)
            shape_data = {}
            df2link_count_people.to_csv(csv_filename, mode='w', index=False)

        link = f"rtsp://{username}:{password}@{ip}/Streaming/Channels/101/"
        row_data_link = {
            'Name': name,
            'Link': link
        }
        if link in df2link['Link'].values:
            matching_row = df2link[df2link['Link'] == link].index[0]
            df2link.loc[matching_row, 'Name'] = name
        else:
            df2link = df2link.append(row_data_link, ignore_index=True)
        
        shape_data = {}
        df2link.to_csv('static/link.csv', mode='w', index=False)
        
        return redirect('/label2')
        
    
    if ip in df2['IP'].values:
        
        matching_row = df2[df2['IP'] == ip].index[0]
        df2.loc[matching_row, 'Username'] = username
        df2.loc[matching_row, 'Password'] = password
        df2.loc[matching_row, 'Name'] = name
        df2.loc[matching_row, 'Type_box'] = shape_data.get('Type_box', '')
        df2.loc[matching_row, 'X1'] = shape_data.get('X1', '')
        df2.loc[matching_row, 'Y1'] = shape_data.get('Y1', '')
        df2.loc[matching_row, 'X2'] = shape_data.get('X2', '')
        df2.loc[matching_row, 'Y2'] = shape_data.get('Y2', '')
        df2.loc[matching_row, 'X3'] = shape_data.get('X3', '')
        df2.loc[matching_row, 'Y3'] = shape_data.get('Y3', '')
        df2.loc[matching_row, 'X4'] = shape_data.get('X4', '')
        df2.loc[matching_row, 'Y4'] = shape_data.get('Y4', '')
    else:
        
        row_data = {
            'Username': username,
            'Password': password,
            'Name': name,
            'IP': ip,
            'Type_box': shape_data.get('Type_box', ''),
            'X1': shape_data.get('X1', ''),
            'Y1': shape_data.get('Y1', ''),
            'X2': shape_data.get('X2', ''),
            'Y2': shape_data.get('Y2', ''),
            'X3': shape_data.get('X3', ''),
            'Y3': shape_data.get('Y3', ''),
            'X4': shape_data.get('X4', ''),
            'Y4': shape_data.get('Y4', '')
        }
    
        df2 = df2.append(row_data, ignore_index=True)

    shape_data = {}

    df2.to_csv('static/data2.csv', mode='w', index=False) 
    
    df_status = pd.read_csv('static/status_function.csv')
    status_c2_congun = df_status.loc[1, 'function_congun'] if not df_status.empty else None
    status_c2_count_people = df_status.loc[1, 'function_count_people'] if not df_status.empty else None

    # Check status_c1_congun and add 'congun' to selected_functions_c1 if 'yes'
    if status_c2_congun == 'yes':
        csv_filename = f'./static/link_congun.csv'
        df2link_congun = pd.read_csv(csv_filename)
        link = f"rtsp://{username}:{password}@{ip}/Streaming/Channels/101/"
        row_data_link = {
                'Name' : name,
                'Link' : link
            }
        if link in df2link_congun['Link'].values:
            matching_row = df2link_congun[df2link_congun['Link'] == link].index[0]
            df2link_congun.loc[matching_row, 'Name'] = name
        else:
            df2link_congun = df2link_congun.append(row_data_link, ignore_index=True)
        shape_data = {}
        df2link_congun.to_csv(csv_filename, mode='w', index=False)
        
    # Check status_c1_count_people and add 'count-people' to selected_functions_c1 if 'yes'
    if status_c2_count_people == 'yes':
        csv_filename = f'./static/link_count_people.csv'
        df2link_count_people = pd.read_csv(csv_filename)
        link = f"rtsp://{username}:{password}@{ip}/Streaming/Channels/101/"
        row_data_link = {
                'Name' : name,
                'Link' : link
            }
        if link in df2link_count_people['Link'].values:
            matching_row = df2link_count_people[df2link_count_people['Link'] == link].index[0]
            df2link_count_people.loc[matching_row, 'Name'] = name
        else:
            df2link_count_people = df2link_count_people.append(row_data_link, ignore_index=True)
        shape_data = {}
        df2link_count_people.to_csv(csv_filename, mode='w', index=False)
              
    link = f"rtsp://{username}:{password}@{ip}/Streaming/Channels/101/"
    row_data_link = {
        'Name': name,
        'Link': link
    }
    if link in df2link['Link'].values:
        matching_row = df2link[df2link['Link'] == link].index[0]
        df2link.loc[matching_row, 'Name'] = name
    else:
        df2link = df2link.append(row_data_link, ignore_index=True)
        
    shape_data = {}
    df2link.to_csv('static/link.csv', mode='w', index=False)

    if status_c2_congun == 'yes':
        if process is not None:
            process.terminate()
        conda_env = "openmmposep3.8"
        #'conda', 'run', '-n', f'{conda_env}', 
        command = ['python', 'Multi-RecordingCCTV-CV.py']
        print(command)
        process_congun = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out_coungun, err_congun = process_congun.communicate()
        
        print("Process congun Output:")
        print(out_coungun.decode('utf-8'))  
        print("Process congun Error:")
        print(err_congun.decode('utf-8'))  
        
    if status_c2_count_people == 'yes':
        if process is not None:
            process.terminate()
        conda_env = "yolop3.9"
        #'conda', 'run', '-n', f'{conda_env}', 
        command = ['python', 'python_script_runcount_EffNet_Jetson_Demo_26Dec23.py', '-second', '2', '-f', str(20), '-img_save', 'not_all']
        print(command)
        process_count = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out_count, err_count = process_count.communicate()

        print("Process count Output:")
        print(out_count.decode('utf-8'))  
        print("Process count Error:")
        print(err_count.decode('utf-8'))  
    
    return redirect('/')

@app.route('/submit3', methods=['POST'])
def submit3():
    global df3, shape_data, process

    df3 = pd.read_csv('static/data2.csv')
    df3link = pd.read_csv('static/link.csv')
    df3_ipimage = pd.read_csv('static/Images_IP.csv')

    username = request.form['username3']
    password = request.form['password3']
    name = request.form['name3']
    ip = request.form['ip3']
    
    if 'draw' in request.form:
        
        row_data = {
            'Username': username,
            'Password': password,
            'Name': name,
            'IP': ip,
            'Type_box': shape_data.get('Type_box', ''),
            'X1': shape_data.get('X1', ''),
            'Y1': shape_data.get('Y1', ''),
            'X2': shape_data.get('X2', ''),
            'Y2': shape_data.get('Y2', ''),
            'X3': shape_data.get('X3', ''),
            'Y3': shape_data.get('Y3', ''),
            'X4': shape_data.get('X4', ''),
            'Y4': shape_data.get('Y4', '')
        }

        df3 = df3.append(row_data, ignore_index=True)

        shape_data = {}

        df3.to_csv('static/data2.csv', mode='w', index=False)
        
        image = "/Image_c3"
        if image in df3_ipimage['/Images'].values:
            matching_row = df3_ipimage[df3_ipimage['/Images'] == image].index[0]
            df3_ipimage.loc[matching_row, 'IP'] = ip
        else:
            
            row_data_ipimage = {
                'IP' : ip,
                '/Images' : "/Image_c3"
            }
            df3_ipimage = df3_ipimage.append(row_data_ipimage, ignore_index=True)
        shape_data = {}
        df3_ipimage.to_csv('static/Images_IP.csv', index=False)
        
        df_status = pd.read_csv('static/status_function.csv')
        status_c3_congun = df_status.loc[2, 'function_congun'] if not df_status.empty else None
        status_c3_count_people = df_status.loc[2, 'function_count_people'] if not df_status.empty else None

        # Check status_c1_congun and add 'congun' to selected_functions_c1 if 'yes'
        if status_c3_congun == 'yes':
            csv_filename = f'./static/link_congun.csv'
            df3link_congun = pd.read_csv(csv_filename)
            row_data_link = {
                'Name' : name,
                'Link' : f"rtsp://{username}:{password}@{ip}/Streaming/Channels/101/"
            }
            df3link_congun = df3link_congun.append(row_data_link, ignore_index=True)
            shape_data = {}
            df3link_congun.to_csv(csv_filename, mode='w', index=False)
        # Check status_c1_count_people and add 'count-people' to selected_functions_c1 if 'yes'
        if status_c3_count_people == 'yes':
            csv_filename = f'./static/link_count_people.csv'
            df3link_count_people = pd.read_csv(csv_filename)
            row_data_link = {
                'Name' : name,
                'Link' : f"rtsp://{username}:{password}@{ip}/Streaming/Channels/101/"
            }
            df3link_count_people = df3link_count_people.append(row_data_link, ignore_index=True)
            shape_data = {}
            df3link_count_people.to_csv(csv_filename, mode='w', index=False)

        link = f"rtsp://{username}:{password}@{ip}/Streaming/Channels/101/"
        row_data_link = {
            'Name': name,
            'Link': link
        }
        if link in df3link['Link'].values:
            matching_row = df3link[df3link['Link'] == link].index[0]
            df3link.loc[matching_row, 'Name'] = name
        else:
            df3link = df3link.append(row_data_link, ignore_index=True)
        
        shape_data = {}
        df3link.to_csv('static/link.csv', mode='w', index=False)
        
        return redirect('/label3')
    
    if ip in df3['IP'].values:
        matching_row = df3[df3['IP'] == ip].index[0]
        df3.loc[matching_row, 'Username'] = username
        df3.loc[matching_row, 'Password'] = password
        df3.loc[matching_row, 'Name'] = name
        df3.loc[matching_row, 'Type_box'] = shape_data.get('Type_box', '')
        df3.loc[matching_row, 'X1'] = shape_data.get('X1', '')
        df3.loc[matching_row, 'Y1'] = shape_data.get('Y1', '')
        df3.loc[matching_row, 'X2'] = shape_data.get('X2', '')
        df3.loc[matching_row, 'Y2'] = shape_data.get('Y2', '')
        df3.loc[matching_row, 'X3'] = shape_data.get('X3', '')
        df3.loc[matching_row, 'Y3'] = shape_data.get('Y3', '')
        df3.loc[matching_row, 'X4'] = shape_data.get('X4', '')
        df3.loc[matching_row, 'Y4'] = shape_data.get('Y4', '')
    else:
        row_data = {
            'Username': username,
            'Password': password,
            'Name': name,
            'IP': ip,
            'Type_box': shape_data.get('Type_box', ''),
            'X1': shape_data.get('X1', ''),
            'Y1': shape_data.get('Y1', ''),
            'X2': shape_data.get('X2', ''),
            'Y2': shape_data.get('Y2', ''),
            'X3': shape_data.get('X3', ''),
            'Y3': shape_data.get('Y3', ''),
            'X4': shape_data.get('X4', ''),
            'Y4': shape_data.get('Y4', '')
        }
    
        df3 = df3.append(row_data, ignore_index=True)
        
    shape_data = {}

    df3.to_csv('static/data2.csv', mode='w', index=False) 
    
    df_status = pd.read_csv('static/status_function.csv')
    status_c3_congun = df_status.loc[2, 'function_congun'] if not df_status.empty else None
    status_c3_count_people = df_status.loc[2, 'function_count_people'] if not df_status.empty else None

    # Check status_c1_congun and add 'congun' to selected_functions_c1 if 'yes'
    if status_c3_congun == 'yes':
        csv_filename = f'./static/link_congun.csv'
        df3link_congun = pd.read_csv(csv_filename)
        link = f"rtsp://{username}:{password}@{ip}/Streaming/Channels/101/"
        row_data_link = {
                'Name' : name,
                'Link' : link
            }
        if link in df3link_congun['Link'].values:
            matching_row = df3link_congun[df3link_congun['Link'] == link].index[0]
            df3link_congun.loc[matching_row, 'Name'] = name
        else:
            df3link_congun = df3link_congun.append(row_data_link, ignore_index=True)
        shape_data = {}
        df3link_congun.to_csv(csv_filename, mode='w', index=False)
        
    # Check status_c1_count_people and add 'count-people' to selected_functions_c1 if 'yes'
    if status_c3_count_people == 'yes':
        csv_filename = f'./static/link_count_people.csv'
        df3link_count_people = pd.read_csv(csv_filename)
        link = f"rtsp://{username}:{password}@{ip}/Streaming/Channels/101/"
        row_data_link = {
                'Name' : name,
                'Link' : link
            }
        if link in df3link_count_people['Link'].values:
            matching_row = df3link_count_people[df3link_count_people['Link'] == link].index[1]
            df3link_count_people.loc[matching_row, 'Name'] = name
        else:
            df3link_count_people = df3link_count_people.append(row_data_link, ignore_index=True)
        shape_data = {}
        df3link_count_people.to_csv(csv_filename, mode='w', index=False)
              
    link = f"rtsp://{username}:{password}@{ip}/Streaming/Channels/101/"
    row_data_link = {
        'Name': name,
        'Link': link
    }
    if link in df3link['Link'].values:
        matching_row = df3link[df3link['Link'] == link].index[2]
        df3link.loc[matching_row, 'Name'] = name
    else:
        df2link = df2link.append(row_data_link, ignore_index=True)
        
    shape_data = {}
    df3link.to_csv('static/link.csv', mode='w', index=False)

    if status_c3_congun == 'yes':
        if process is not None:
            process.terminate()
        conda_env = "openmmposep3.8"
        command = ['python', 'Multi-RecordingCCTV-CV.py']
        print(command)
        process_congun = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out_coungun, err_congun = process_congun.communicate()
        
        print("Process congun Output:")
        print(out_coungun.decode('utf-8'))  
        print("Process congun Error:")
        print(err_congun.decode('utf-8'))  
        
    if status_c3_count_people == 'yes':
        if process is not None:
            process.terminate()
        conda_env = "yolop3.9"
        command = ['python', 'python_script_runcount_EffNet_Jetson_Demo_26Dec23.py', '-second', '2', '-f', str(20), '-img_save', 'all']
        print(command)
        process_count = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out_count, err_count = process_count.communicate()

        print("Process count Output:")
        print(out_count.decode('utf-8'))  
        print("Process count Error:")
        print(err_count.decode('utf-8'))
    
    return redirect('/')

@app.route('/submit4', methods=['POST'])
def submit4():
    global df4, shape_data, process

    df4 = pd.read_csv('static/data2.csv')
    df4link = pd.read_csv('static/link.csv')
    df4_ipimage = pd.read_csv('static/Images_IP.csv')

    username = request.form['username4']
    password = request.form['password4']
    name = request.form['name4']
    ip = request.form['ip4']

    if 'draw' in request.form:

        row_data = {
            'Username': username,
            'Password': password,
            'Name': name,
            'IP': ip,
            'Type_box': shape_data.get('Type_box', ''),
            'X1': shape_data.get('X1', ''),
            'Y1': shape_data.get('Y1', ''),
            'X2': shape_data.get('X2', ''),
            'Y2': shape_data.get('Y2', ''),
            'X3': shape_data.get('X3', ''),
            'Y3': shape_data.get('Y3', ''),
            'X4': shape_data.get('X4', ''),
            'Y4': shape_data.get('Y4', '')
        }

        df4 = df4.append(row_data, ignore_index=True)

        shape_data = {}
        
        df4.to_csv('static/data2.csv', mode='w', index=False) 
                
        image = "/Image_c4"
        if image in df4_ipimage['/Images'].values:
            matching_row = df4_ipimage[df4_ipimage['/Images'] == image].index[0]
            df4_ipimage.loc[matching_row, 'IP'] = ip
        else:
            
            row_data_ipimage = {
                'IP' : ip,
                '/Images' : "/Image_c4"
            }
            df4_ipimage = df4_ipimage.append(row_data_ipimage, ignore_index=True)
        shape_data = {}
        df4_ipimage.to_csv('static/Images_IP.csv', index=False)
        
        df_status = pd.read_csv('static/status_function.csv')
        status_c4_congun = df_status.loc[3, 'function_congun'] if not df_status.empty else None
        status_c4_count_people = df_status.loc[3, 'function_count_people'] if not df_status.empty else None

        # Check status_c1_congun and add 'congun' to selected_functions_c1 if 'yes'
        if status_c4_congun == 'yes':
            csv_filename = f'./static/link_congun.csv'
            df4link_congun = pd.read_csv(csv_filename)
            row_data_link = {
                'Name' : name,
                'Link' : f"rtsp://{username}:{password}@{ip}/Streaming/Channels/101/"
            }
            df4link_congun = df4link_congun.append(row_data_link, ignore_index=True)
            shape_data = {}
            df4link_congun.to_csv(csv_filename, mode='w', index=False)
        # Check status_c1_count_people and add 'count-people' to selected_functions_c1 if 'yes'
        if status_c4_count_people == 'yes':
            csv_filename = f'./static/link_count_people.csv'
            df4link_count_people = pd.read_csv(csv_filename)
            row_data_link = {
                'Name' : name,
                'Link' : f"rtsp://{username}:{password}@{ip}/Streaming/Channels/101/"
            }
            df4link_count_people = df4link_count_people.append(row_data_link, ignore_index=True)
            shape_data = {}
            df4link_count_people.to_csv(csv_filename, mode='w', index=False)

        link = f"rtsp://{username}:{password}@{ip}/Streaming/Channels/101/"
        row_data_link = {
            'Name': name,
            'Link': link
        }
        if link in df4link['Link'].values:
            matching_row = df4link[df4link['Link'] == link].index[0]
            df4link.loc[matching_row, 'Name'] = name
        else:
            df4link = df4link.append(row_data_link, ignore_index=True)
        
        shape_data = {}
        df4link.to_csv('static/link.csv', mode='w', index=False)
        
        return redirect('/label4')
    
    if ip in df4['IP'].values:
        matching_row = df4[df4['IP'] == ip].index[0]
        df4.loc[matching_row, 'Username'] = username
        df4.loc[matching_row, 'Password'] = password
        df4.loc[matching_row, 'Name'] = name
        df4.loc[matching_row, 'Type_box'] = shape_data.get('Type_box', '')
        df4.loc[matching_row, 'X1'] = shape_data.get('X1', '')
        df4.loc[matching_row, 'Y1'] = shape_data.get('Y1', '')
        df4.loc[matching_row, 'X2'] = shape_data.get('X2', '')
        df4.loc[matching_row, 'Y2'] = shape_data.get('Y2', '')
        df4.loc[matching_row, 'X3'] = shape_data.get('X3', '')
        df4.loc[matching_row, 'Y3'] = shape_data.get('Y3', '')
        df4.loc[matching_row, 'X4'] = shape_data.get('X4', '')
        df4.loc[matching_row, 'Y4'] = shape_data.get('Y4', '')
    else:
        row_data = {
            'Username': username,
            'Password': password,
            'Name': name,
            'IP': ip,
            'Type_box': shape_data.get('Type_box', ''),
            'X1': shape_data.get('X1', ''),
            'Y1': shape_data.get('Y1', ''),
            'X2': shape_data.get('X2', ''),
            'Y2': shape_data.get('Y2', ''),
            'X3': shape_data.get('X3', ''),
            'Y3': shape_data.get('Y3', ''),
            'X4': shape_data.get('X4', ''),
            'Y4': shape_data.get('Y4', '')
        }
    
        df4 = df4.append(row_data, ignore_index=True)

    shape_data = {}

    df4.to_csv('static/data2.csv', mode='w', index=False)  
    
    df_status = pd.read_csv('static/status_function.csv')
    status_c4_congun = df_status.loc[3, 'function_congun'] if not df_status.empty else None
    status_c4_count_people = df_status.loc[3, 'function_count_people'] if not df_status.empty else None

    # Check status_c1_congun and add 'congun' to selected_functions_c1 if 'yes'
    if status_c4_congun == 'yes':
        csv_filename = f'./static/link_congun.csv'
        df4link_congun = pd.read_csv(csv_filename)
        link = f"rtsp://{username}:{password}@{ip}/Streaming/Channels/101/"
        row_data_link = {
                'Name' : name,
                'Link' : link
            }
        if link in df4link_congun['Link'].values:
            matching_row = df4link_congun[df4link_congun['Link'] == link].index[0]
            df4link_congun.loc[matching_row, 'Name'] = name
        else:
            df4link_congun = df4link_congun.append(row_data_link, ignore_index=True)
        shape_data = {}
        df4link_congun.to_csv(csv_filename, mode='w', index=False)
        
    # Check status_c1_count_people and add 'count-people' to selected_functions_c1 if 'yes'
    if status_c4_count_people == 'yes':
        csv_filename = f'./static/link_count_people.csv'
        df4link_count_people = pd.read_csv(csv_filename)
        link = f"rtsp://{username}:{password}@{ip}/Streaming/Channels/101/"
        row_data_link = {
                'Name' : name,
                'Link' : link
            }
        if link in df4link_count_people['Link'].values:
            matching_row = df4link_count_people[df4link_count_people['Link'] == link].index[0]
            df4link_count_people.loc[matching_row, 'Name'] = name
        else:
            df4link_count_people = df4link_count_people.append(row_data_link, ignore_index=True)
        shape_data = {}
        df4link_count_people.to_csv(csv_filename, mode='w', index=False)
              
    link = f"rtsp://{username}:{password}@{ip}/Streaming/Channels/101/"
    row_data_link = {
        'Name': name,
        'Link': link
    }
    if link in df4link['Link'].values:
        matching_row = df4link[df4link['Link'] == link].index[1]
        df4link.loc[matching_row, 'Name'] = name
    else:
        df4link = df4link.append(row_data_link, ignore_index=True)
        
    shape_data = {}
    df4link.to_csv('static/link.csv', mode='w', index=False)

    if status_c4_congun == 'yes':
        if process is not None:
            process.terminate()
        conda_env = "openmmposep3.8"
        command = ['conda', 'run', '-n', f'{conda_env}', 'python', 'Multi-RecordingCCTV-CV.py']
        print(command)
        process_congun = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out_coungun, err_congun = process_congun.communicate()
        
        print("Process congun Output:")
        print(out_coungun.decode('utf-8'))  
        print("Process congun Error:")
        print(err_congun.decode('utf-8'))  
        
    if status_c4_count_people == 'yes':
        if process is not None:
            process.terminate()
        conda_env = "yolop3.9"
        command = ['python', 'python_script_runcount_EffNet_Jetson_Demo_26Dec23.py', '-second', '2', '-f', str(20), '-img_save', 'all']
        print(command)
        process_count = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out_count, err_count = process_count.communicate()

        print("Process count Output:")
        print(out_count.decode('utf-8'))  
        print("Process count Error:")
        print(err_count.decode('utf-8'))
    
    return redirect('/')

@app.route('/submit5', methods=['POST'])
def submit5():
    global df5, shape_data, process

    df5 = pd.read_csv('static/data2.csv')
    df5link = pd.read_csv('static/link.csv')
    df5_ipimage = pd.read_csv('static/Images_IP.csv')
    
    username = request.form['username5']
    password = request.form['password5']
    name = request.form['name5']
    ip = request.form['ip5']

    if 'draw' in request.form:

        row_data = {
            'Username': username,
            'Password': password,
            'Name': name,
            'IP': ip,
            'Type_box': shape_data.get('Type_box', ''),
            'X1': shape_data.get('X1', ''),
            'Y1': shape_data.get('Y1', ''),
            'X2': shape_data.get('X2', ''),
            'Y2': shape_data.get('Y2', ''),
            'X3': shape_data.get('X3', ''),
            'Y3': shape_data.get('Y3', ''),
            'X4': shape_data.get('X4', ''),
            'Y4': shape_data.get('Y4', '')
        }

        df5 = df5.append(row_data, ignore_index=True)

        shape_data = {}
        
        df5.to_csv('static/data2.csv', mode='w', index=False) 
                        
        image = "/Image_c5"
        if image in df5_ipimage['/Images'].values:
            matching_row = df5_ipimage[df5_ipimage['/Images'] == image].index[0]
            df5_ipimage.loc[matching_row, 'IP'] = ip
        else:
            
            row_data_ipimage = {
                'IP' : ip,
                '/Images' : "/Image_c5"
            }
            df5_ipimage = df5_ipimage.append(row_data_ipimage, ignore_index=True)
        shape_data = {}
        df5_ipimage.to_csv('static/Images_IP.csv', index=False)
        
        df_status = pd.read_csv('static/status_function.csv')
        status_c5_congun = df_status.loc[4, 'function_congun'] if not df_status.empty else None
        status_c5_count_people = df_status.loc[4, 'function_count_people'] if not df_status.empty else None

        # Check status_c1_congun and add 'congun' to selected_functions_c1 if 'yes'
        if status_c5_congun == 'yes':
            csv_filename = f'./static/link_congun.csv'
            df5link_congun = pd.read_csv(csv_filename)
            row_data_link = {
                'Name' : name,
                'Link' : f"rtsp://{username}:{password}@{ip}/Streaming/Channels/101/"
            }
            df5link_congun = df5link_congun.append(row_data_link, ignore_index=True)
            shape_data = {}
            df5link_congun.to_csv(csv_filename, mode='w', index=False)
        # Check status_c1_count_people and add 'count-people' to selected_functions_c1 if 'yes'
        if status_c5_count_people == 'yes':
            csv_filename = f'./static/link_count_people.csv'
            df5link_count_people = pd.read_csv(csv_filename)
            row_data_link = {
                'Name' : name,
                'Link' : f"rtsp://{username}:{password}@{ip}/Streaming/Channels/101/"
            }
            df5link_count_people = df5link_count_people.append(row_data_link, ignore_index=True)
            shape_data = {}
            df5link_count_people.to_csv(csv_filename, mode='w', index=False)

        link = f"rtsp://{username}:{password}@{ip}/Streaming/Channels/101/"
        row_data_link = {
            'Name': name,
            'Link': link
        }
        if link in df5link['Link'].values:
            matching_row = df5link[df5link['Link'] == link].index[0]
            df5link.loc[matching_row, 'Name'] = name
        else:
            df5link = df5link.append(row_data_link, ignore_index=True)
        
        shape_data = {}
        df5link.to_csv('static/link.csv', mode='w', index=False)
        
        return redirect('/label5')
    
    if ip in df5['IP'].values:
        matching_row = df5[df5['IP'] == ip].index[0]
        df5.loc[matching_row, 'Username'] = username
        df5.loc[matching_row, 'Password'] = password
        df5.loc[matching_row, 'Name'] = name
        df5.loc[matching_row, 'Type_box'] = shape_data.get('Type_box', '')
        df5.loc[matching_row, 'X1'] = shape_data.get('X1', '')
        df5.loc[matching_row, 'Y1'] = shape_data.get('Y1', '')
        df5.loc[matching_row, 'X2'] = shape_data.get('X2', '')
        df5.loc[matching_row, 'Y2'] = shape_data.get('Y2', '')
        df5.loc[matching_row, 'X3'] = shape_data.get('X3', '')
        df5.loc[matching_row, 'Y3'] = shape_data.get('Y3', '')
        df5.loc[matching_row, 'X4'] = shape_data.get('X4', '')
        df5.loc[matching_row, 'Y4'] = shape_data.get('Y4', '')
    else:
        row_data = {
            'Username': username,
            'Password': password,
            'Name': name,
            'IP': ip,
            'Type_box': shape_data.get('Type_box', ''),
            'X1': shape_data.get('X1', ''),
            'Y1': shape_data.get('Y1', ''),
            'X2': shape_data.get('X2', ''),
            'Y2': shape_data.get('Y2', ''),
            'X3': shape_data.get('X3', ''),
            'Y3': shape_data.get('Y3', ''),
            'X4': shape_data.get('X4', ''),
            'Y4': shape_data.get('Y4', '')
        }
    
        df5 = df5.append(row_data, ignore_index=True)

    shape_data = {}
   
    df5.to_csv('static/data2.csv', mode='w', index=False)  
    
    df_status = pd.read_csv('static/status_function.csv')
    status_c5_congun = df_status.loc[4, 'function_congun'] if not df_status.empty else None
    status_c5_count_people = df_status.loc[4, 'function_count_people'] if not df_status.empty else None

    # Check status_c1_congun and add 'congun' to selected_functions_c1 if 'yes'
    if status_c5_congun == 'yes':
        csv_filename = f'./static/link_congun.csv'
        df5link_congun = pd.read_csv(csv_filename)
        link = f"rtsp://{username}:{password}@{ip}/Streaming/Channels/101/"
        row_data_link = {
                'Name' : name,
                'Link' : link
            }
        if link in df5link_congun['Link'].values:
            matching_row = df5link_congun[df5link_congun['Link'] == link].index[0]
            df5link_congun.loc[matching_row, 'Name'] = name
        else:
            df5link_congun = df5link_congun.append(row_data_link, ignore_index=True)
        shape_data = {}
        df5link_congun.to_csv(csv_filename, mode='w', index=False)
        
    # Check status_c1_count_people and add 'count-people' to selected_functions_c1 if 'yes'
    if status_c5_count_people == 'yes':
        csv_filename = f'./static/link_count_people.csv'
        df5link_count_people = pd.read_csv(csv_filename)
        link = f"rtsp://{username}:{password}@{ip}/Streaming/Channels/101/"
        row_data_link = {
                'Name' : name,
                'Link' : link
            }
        if link in df5link_count_people['Link'].values:
            matching_row = df5link_count_people[df5link_count_people['Link'] == link].index[0]
            df5link_count_people.loc[matching_row, 'Name'] = name
        else:
            df5link_count_people = df5link_count_people.append(row_data_link, ignore_index=True)
        shape_data = {}
        df5link_count_people.to_csv(csv_filename, mode='w', index=False)
              
    link = f"rtsp://{username}:{password}@{ip}/Streaming/Channels/101/"
    row_data_link = {
        'Name': name,
        'Link': link
    }
    if link in df5link['Link'].values:
        matching_row = df5link[df5link['Link'] == link].index[0]
        df5link.loc[matching_row, 'Name'] = name
    else:
        df5link = df5link.append(row_data_link, ignore_index=True)
        
    shape_data = {}
    df5link.to_csv('static/link.csv', mode='w', index=False)

    if status_c5_congun == 'yes':
        if process is not None:
            process.terminate()
        conda_env = "openmmposep3.8"
        command = ['conda', 'run', '-n', f'{conda_env}', 'python', 'Multi-RecordingCCTV-CV.py']
        print(command)
        process_congun = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out_coungun, err_congun = process_congun.communicate()
        
        print("Process congun Output:")
        print(out_coungun.decode('utf-8'))  
        print("Process congun Error:")
        print(err_congun.decode('utf-8'))  
        
    if status_c5_count_people == 'yes':
        if process is not None:
            process.terminate()
        conda_env = "yolop3.9"
        command = ['python', 'python_script_runcount_EffNet_Jetson_Demo_26Dec23.py', '-second', '2', '-f', str(20), '-img_save', 'all']
        print(command)
        process_count = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out_count, err_count = process_count.communicate()

        print("Process count Output:")
        print(out_count.decode('utf-8'))  
        print("Process count Error:")
        print(err_count.decode('utf-8'))
    
    return redirect('/')

@app.route('/delete_row', methods=['POST'])
def delete_row():
    df = pd.read_csv('static/data2.csv')
    dflink = pd.read_csv('static/link.csv') 
    df_ipimage = pd.read_csv('static/Images_IP.csv')
    df_status = pd.read_csv('static/status_function.csv')
    row_number = int(request.form['row_number'])
    
    if row_number >= 0 and row_number < len(df_ipimage):
        df_ipimage.iloc[row_number, 0] = ''  # Set the IP column value to an empty string
        
        # Shift the subsequent rows up by copying the value from the next row
        for i in range(row_number, len(df_ipimage)-1):
            df_ipimage.iloc[i, 0] = df_ipimage.iloc[i+1, 0]
        
        df_ipimage.reset_index(drop=True, inplace=True)  # Reset the row indices
        df_ipimage.to_csv('static/Images_IP.csv', index=False)  # Save the modified DataFrame back to the CSV file
        
    if row_number >= 0 and row_number < len(dflink):
        dflink.drop(dflink.index[row_number], inplace=True)
        dflink.to_csv('static/link.csv', index=False)  # Save the modified DataFrame back to the CSV file
        
    if row_number >= 0 and row_number < len(df):
        df.drop(df.index[row_number], inplace=True)
        df.to_csv('static/data2.csv', index=False)  # Save the modified DataFrame back to the CSV file
    
    if row_number >= 0 and row_number < len(df_status):
        df_status.drop(df_status.index[row_number], inplace=True)
        df_status.to_csv('static/status_function.csv', index=False)  # Save the modified DataFrame back to the CSV file    
            
    return redirect('/')

@app.route('/save-label', methods=['POST'])
def save_label():
    global draw_status
    draw_status = True  
    return redirect(url_for('index'))

@app.route('/save-label-edit', methods=['POST'])
def save_label_edit():
    global draw_status
    draw_status = True  
    return redirect(url_for('index'))

@app.route('/save-label2', methods=['POST'])
def save_label2():
    global draw_status
    draw_status = True  
    return redirect(url_for('index'))

@app.route('/save-label-edit2', methods=['POST'])
def save_label_edit2():
    global draw_status
    draw_status = True  
    return redirect(url_for('index'))

@app.route('/save-label3', methods=['POST'])
def save_label3():
    global draw_status
    draw_status = True
    return redirect(url_for('index'))

@app.route('/save-label-edit3', methods=['POST'])
def save_label_edit3():
    global draw_status
    draw_status = True  
    return redirect(url_for('index'))

@app.route('/save-label4', methods=['POST'])
def save_label4():
    global draw_status
    draw_status = True
    return redirect(url_for('index'))

@app.route('/save-label-edit4', methods=['POST'])
def save_label_edit4():
    global draw_status
    draw_status = True  
    return redirect(url_for('index'))

@app.route('/save-label5', methods=['POST'])
def save_label5():
    global draw_status
    draw_status = True
    return redirect(url_for('index'))

@app.route('/save-label-edit5', methods=['POST'])
def save_label_edit5():
    global draw_status
    draw_status = True  
    return redirect(url_for('index'))

if __name__ == '__main__':
    #if process is not None:
        #process.terminate()

    #process = subprocess.Popen(['python', 'Multi-RecordingCCTV-CV.py'])
    app.debug=True
    app.run(host='0.0.0.0', port=8003)
