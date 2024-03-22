import cv2 
import json 
import os 
import shutil
import subprocess
from ensemble_face_recognition import image_face_recognition
from file_operations import delete_folder, read_json_from_file, write_json_to_file

# global vars
SHOT_LOCATION = '../../internal/json/temp.json'
FRAME_CONTROL = 2
TEMP_FRAME_DATA_PATH = '../../internal/temp_frame_data'
RECOGNIZED_PEOPLE_PATH = '../../internal/json/recognized_people.json'
RETINA_FACE_TEMP_PATH = '../../internal/json/retina_face_temp.json'

## CREATE FRAMES FROM A GIVEN SHOT
def create_frame_from_shot(shot_path):
  '''
    Helper function to create frames given a shot (video)
  '''
  # Read the video from specified path
  cam = cv2.VideoCapture(shot_path)
  fps = int(cam.get(cv2.CAP_PROP_FPS))
  print("fps ", fps)
  # Calculate the interval between frames to capture 24 frames per second
  frame_interval = fps // FRAME_CONTROL

  frame_paths = []

  try:
    # creating a folder named data
    if not os.path.exists(TEMP_FRAME_DATA_PATH):
      os.makedirs(TEMP_FRAME_DATA_PATH)

  # if not created then raise error
  except OSError:
    print ('Error: Creating directory of data')

  # frame
  currentframe = 0

  while(True):

    # reading from frame
    ret,frame = cam.read()

    if ret:
      # if video is still left continue creating images
      if currentframe % frame_interval == 0:
        name = TEMP_FRAME_DATA_PATH + '/frame-' + str(currentframe) + '.jpg'
        # print ('Creating...' + name)
        frame_paths.append(name)

        # writing the extracted images
        cv2.imwrite(name, frame)

      # increasing counter so that it will
      # show how many frames are created
      currentframe += 1
    else:
      break

  # Release all space and windows once done
  cam.release()
  cv2.destroyAllWindows()
  print("no of frames: ", len(frame_paths))
  return frame_paths


## RECOGNIZE ACTORS USING THAT SHOT AND RETURN
def shot_face_recognition():
  '''
    Face recognition, given a shot return the names of the people in the shot
  '''

  # create frames from the shot
  shot_path = read_json_from_file(SHOT_LOCATION)['selected_video']
  frame_paths = create_frame_from_shot(shot_path)

  # Optimization- call retina face and store img path -> count map in retina_face_temp
  retina_temp = {}
  for frame in frame_paths:
    retina_temp[frame] = 0
  write_json_to_file(RETINA_FACE_TEMP_PATH, retina_temp)
  subprocess.run(["bash", "-c", f"../scripts/trigger_retina_face.sh ignore_parameter"], capture_output=True, text=True)

  recognized_people = set()
  # go through frames and perform recognition
  for frame_path in frame_paths:
    people = image_face_recognition(frame_path)
    for person in people:
      if person != "Unknown":
        recognized_people.add(person)

  # clean-up
  # print('deleting folder....')
  delete_folder(TEMP_FRAME_DATA_PATH)

  recognized_people_json = {
    "recognized_people": list(recognized_people)
  }
  write_json_to_file(RECOGNIZED_PEOPLE_PATH, recognized_people_json)

#   return list(recognized_people)
  
if __name__ == '__main__':
  shot_face_recognition()