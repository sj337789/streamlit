import streamlit as st
from PIL import Image
import os
import subprocess
import shutil

def process_uploaded_file(uploaded_file, weights_path, output_path):
    try:
        upload_path = os.path.join(output_path, 'modeldetected_FPC', uploaded_file.name)
        os.makedirs(os.path.dirname(upload_path), exist_ok=True)

        with open(upload_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        command = f"python detect.py --weights \"{weights_path}\" --source \"{upload_path}\" --conf 0.6 --save-txt --project \"{output_path}\" --name result_images"
        subprocess.run(command, shell=True, check=True, cwd=os.path.join(os.getcwd(), "yolov5"))
        
        detected_file_path = os.path.join(output_path, 'modeldetected_FPC', 'result_images', uploaded_file.name)
        if os.path.exists(detected_file_path):
            return detected_file_path
    except Exception as e:
        st.write("Error in processing uploaded file: ", str(e))
    return None

st.title('Four-panel-cartoon Detection App')

uploaded_file = st.file_uploader("Choose an image file")

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)
    st.write("")

    weights_path = st.text_input('Enter the path to your weights file:')
    output_path = st.text_input('Enter the directory where you want to save the results:')
    text_file_path = st.text_input('Enter the path to the text file with image filenames:')
    destination_folder = st.text_input('Enter the destination folder to copy the images:')

    if st.button("Detect"):
        if weights_path and output_path and text_file_path and destination_folder:
            st.write("Detecting...")
            detected_file_path = process_uploaded_file(uploaded_file, weights_path, output_path)
            if detected_file_path is
