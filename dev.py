import os
import subprocess
import streamlit as st
import gdown
import zipfile
import shutil
import argparse

# Download weights file from Google Drive
weights_url = 'https://drive.google.com/uc?id=12HYfiGvOFYj3cbCj-iHxvCmAi-AgV0xs'
weights_path = os.path.join(os.getcwd(), 'FPC-weight.pt')
gdown.download(weights_url, weights_path, quiet=False)


def run_detection(weights_path, source_path, output_path):
    # Create the output directory if it doesn't exist
    os.makedirs(output_path, exist_ok=True)

    command = f"python detect.py --weights \"{weights_path}\" --source \"{source_path}\" --conf 0.6 --save-txt --project \"{output_path}\" --name result_images"

    subprocess.run(command, shell=True, check=True, cwd=os.path.join(os.getcwd(), "yolov5"))


# Streamlit app
def main():
    st.title("Four Panel Cartoon Detection")
    st.write("Upload your zip file containing images")

    # Create the 'uploads' directory if it doesn't exist
    os.makedirs('uploads', exist_ok=True)

    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        with open(os.path.join("uploads", uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success("File uploaded.")
        st.write("Detecting...")

        # Unzip the uploaded file
        zip_path = os.path.join('uploads', uploaded_file.name)
        extract_path = os.path.join('uploads', os.path.splitext(uploaded_file.name)[0])
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)

        # Run detection script
        source_path = extract_path
        output_path = os.path.normpath(os.path.join(os.path.expanduser('~'), 'Desktop', 'modeldetected_FPC'))
        os.makedirs(output_path, exist_ok=True)

        # Modify the weights_path, source_path, and output_path here
        weights_path = os.path.join(os.getcwd(), 'FPC-weight.pt')

        run_detection(weights_path, source_path, output_path)

        st.write("Detection finished. Check the output directory.")

        # Read the list of file names from the text file
        file_names_path = os.path.join(extract_path, "fpc_true.txt")
        with open(file_names_path, "r") as f:
            file_names = [line.strip() for line in f.readlines() if line.strip()]

        # Define the source and destination folders
        source_folder = os.path.join(output_path, "result_images")
        destination_folder = os.path.join(output_path, "detected_true_images")

        # Create the destination folder if it doesn't exist
        os.makedirs(destination_folder, exist_ok=True)

        # Iterate through the file names, and if the file exists in the source folder, copy it to the destination folder
        for file_name in file_names:
            # Append the .jpg extension if it's missing
            if not file_name.lower().endswith('.jpg'):
                file_name = f"{file_name}.jpg"

            source_file = os.path.join(source_folder, file_name)
            destination_file = os.path.join(destination_folder, file_name)

            if os.path.exists(source_file):
                shutil.copy(source_file, destination_file)
                st.write(f"Copied {file_name} to {destination_folder}")
            else:
                st.write(f"File {file_name} not found in {source_folder}")


if __name__ == '__main__':
    main()
