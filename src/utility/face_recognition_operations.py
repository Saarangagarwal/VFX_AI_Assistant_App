from imutils import paths
from constants.internal_config import FR_DETECTION_METHOD, FR_DATASET_PATH, FR_ENCODINGS_DUMP_PATH
import os
import face_recognition
import cv2
import pickle


def fr_encoding_gen():
  '''
    Create encodings using the dataset for the face recognition algorithm.
    Note that folder names are used to identify the (actor) images within them.
  '''
  imagePaths = list(paths.list_images(FR_DATASET_PATH))

  # initialize the list of known encodings and known names
  knownEncodings = []
  knownNames = []
  DETECTION_METHOD = FR_DETECTION_METHOD

  # loop over the image paths
  for (i, imagePath) in enumerate(imagePaths):
    # extract the person name from the image path
    print("[DEBUG] Processing image {}/{}".format(i + 1, len(imagePaths)))
    name = imagePath.split(os.path.sep)[-2]

    # load the input image and convert it from BGR (OpenCV ordering) to dlib ordering (RGB)
    image = cv2.imread(imagePath)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # detect the (x, y)-coordinates of the bounding boxes
    # corresponding to each face in the input image
    boxes = face_recognition.face_locations(rgb, model=DETECTION_METHOD)

    # compute the facial embedding for the face
    encodings = face_recognition.face_encodings(rgb, boxes)

    # loop over the encodings
    for encoding in encodings:
      # add each encoding + name to our set of known names and encodings
      knownEncodings.append(encoding)
      knownNames.append(name)

  return knownNames, knownEncodings


def fr_dump_encodings(knownEncodings, knownNames):
  '''
    Function to store the encodings as pickle files in the file system.
    The path of the created file is determined by the encodings dump global variable
  '''
  print("[DEBUG] serializing and dumping encodings...")
  data = {"encodings": knownEncodings, "names": knownNames}
  f = open(FR_ENCODINGS_DUMP_PATH, "wb")
  f.write(pickle.dumps(data))
  f.close()


def fr_dump_data(data):
  '''
    Function to replace the existing encoding with the provided data.
    The path of the pickle file is determined by the encodings dump global variable
  '''
  if os.path.exists(FR_ENCODINGS_DUMP_PATH):
    os.remove(FR_ENCODINGS_DUMP_PATH)
    f = open(FR_ENCODINGS_DUMP_PATH, "wb")
    f.write(pickle.dumps(data))
    f.close()


def fr_load_encodings():
  '''
    Encodings stored in the pickle file are read and returned as json
  '''
  print("[DEBUG] loading encodings...")
  data = pickle.loads(open(FR_ENCODINGS_DUMP_PATH, "rb").read())
  return data


