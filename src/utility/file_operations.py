import json
import os
import shutil
import cv2
from PIL import Image


def read_json_from_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)
    

def write_json_to_file(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)
        

def count_files_in_directory(directory_path):
  '''
    Helper function to count the number of files in a given directory
    Note that the directory name will be used as the name of the actor
  '''
  try:
    with os.scandir(directory_path) as entries:
      return sum(1 for entry in entries if entry.is_file())
  except FileNotFoundError:
    return -1  # Directory not found
  except PermissionError:
    return -2  # Permission denied
  except Exception as e:
    return -3  # Other error


def delete_folder(path):
  '''
    Used to delete a folder and its contents, given the directory path
  '''
  try:
    shutil.rmtree(path)
    print(f"Deleted folder and contents: {path}")
  except Exception as e:
    print(f"Error deleting folder: {e}")


def clear_temp_selected_video(path):
   data = read_json_from_file(path)
   data['selected_video'] = ""
   write_json_to_file(path, data)


def extract_first_frame(video_path):
  # Open the video file
  cap = cv2.VideoCapture(video_path)
  
  # Check if the video file is opened successfully
  if not cap.isOpened():
      print("Error: Unable to open video file.")
      return None
  
  # Read the first frame
  ret, frame = cap.read()
  
  # Check if the frame is read successfully
  if not ret:
      print("Error: Unable to read the first frame.")
      return None
  
  # Convert the frame from BGR to RGB (OpenCV uses BGR by default)
  frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
  
  # Convert the frame to PIL Image format
  pil_image = Image.fromarray(frame_rgb)
  pil_image_resized = pil_image.resize((400, 300))
    
  
  # Close the video file
  cap.release()
  
  return pil_image_resized


def clone_dataset_internal(from_path, to_path):
  # Walk through the directory tree
  for root, dirs, _ in os.walk(from_path):
    for dir in dirs:
      # Path to source images folder
      source_path = os.path.join(root, dir, 'refimgs')  

      if os.path.exists(source_path):
        # Path to destination images folder
        destination_path = os.path.join(to_path, dir) 

        # Create the corresponding directory if not exists
        if not os.path.exists(destination_path):
          os.makedirs(destination_path)  

        # Copy images from source to destination
        for file in os.listdir(source_path):
          shutil.copy(os.path.join(source_path, file), destination_path)