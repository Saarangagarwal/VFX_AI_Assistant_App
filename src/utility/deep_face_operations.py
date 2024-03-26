from retinaface import RetinaFace
from deepface import DeepFace
from file_operations import write_json_to_file, read_json_from_file
import sys
import re
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS2 # or only MEIPASS
    except Exception:
        print("UGHH in exception")
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# globals
ALGO_MODELS = [ "VGG-Face", "Facenet", "Facenet512", "OpenFace", "DeepFace", "DeepID", "ArcFace", "Dlib", "SFace" ]
VGG_FACE_MODEL = ALGO_MODELS[0]
# VGG_DATASET_PATH = resource_path('dataset')
# VGG_DATASET_PATH = VGG_DATASET_PATH.replace('\\', '/')
VGG_DATASET_PATH = 'C:/Users/agarw/Desktop/1Uwaterloo/4A/URA with Lesley Istead/VFX Assistant App/internal/internal_dataset'
# VGG_DATASET_PATH = resource_path('dataset').replace('\\n', '/').replace('\n', '/').replace('\\', '/')
# VGG_DATASET_PATH = 'dataset'
# print("RURU ", resource_path('dataset').replace('\\n', '/').replace('\n', '/').replace('\\', '/'))
DEEP_FACE_TEMP_PATH = '../../internal/json/deep_face_temp.json'


def vgg_recognition(testImage):
  '''
    INPUT: image path
    OUTPUT: match name, match count
    Function to do face recognition using the VGG face model
  '''
  MODEL = VGG_FACE_MODEL
  faces = RetinaFace.extract_faces(testImage)
  # faces1 = RetinaFace.detect_faces(testImage)
  # print(faces1)
  # # Loop through the detected faces

  # x, y, width, height = faces1["face_1"]['facial_area']

  # # # Ensure the coordinates and dimensions are integers
  # x, y, width, height = int(x), int(y), int(width), int(height)
  # testImage = cv2.imread(testImage)
  # # Create an image of the detected face using OpenCV
  # face_image = testImage[y:y+height, x:x+width]

  # # Save or display the face image
  # cv2.imwrite(f'face_k.jpg', face_image)
  # # You can also display the image using cv2.imshow() or any other method



  matches = []
  match_counts = []

  for face in faces:
    kk = DeepFace.find(face, db_path = VGG_DATASET_PATH, model_name = MODEL, enforce_detection = False)[0]
    print("$$$&&&  DEEP FACE SUCCESS &&&$$$ ")
    actor_hash = {}
    for _, row in kk.iterrows():
      identity = row['identity']
      actor = re.split(r'[\/\\\\]+', identity)
      # print(identity, actor, "$$$$#\n")
      actor_hash[actor[len(actor) - 2]] = 1 + actor_hash.get(actor[len(actor) - 2], 0)

    if actor_hash:
      identified_actor = max(actor_hash, key=lambda k: actor_hash[k])
      matches.append(identified_actor)
      match_counts.append(actor_hash[identified_actor])
      # print(testImage.split("/")[-1], "OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO", identified_actor)
      # print(testImage.split("/")[-1], "OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO", actor_hash[identified_actor])
    else:
      # print(testImage.split("/")[-1], "OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO", "Unknown")
      matches.append("Unknown")
      match_counts.append(-1)
  # print("###END OF IMAGE###")
      
  # write output to file
  deep_face_temp_json = read_json_from_file(DEEP_FACE_TEMP_PATH)
  deep_face_temp_json['vgg_matches_op'] = matches
  deep_face_temp_json['vgg_matches_count_op'] = match_counts
  write_json_to_file(DEEP_FACE_TEMP_PATH, deep_face_temp_json)
  # return matches, match_counts

if __name__ == '__main__':
  vgg_recognition(sys.argv[1]) #works
  # vgg_recognition("C:/Users/agarw/testimgg.jpg")
  # vgg_recognition('../../internal/temp_frame_data/frame-0.jpg')
  # vgg_recognition('C:/Users/agarw/Desktop/1Uwaterloo/4A/URA with Lesley Istead/VFX Assistant App/internal/temp_frame_data/frame-0.jpg')