from imutils import paths
# import sys
# insertPath = ""
# for path in sys.path:
#   if path.endswith('\\src\\utility'):
#     insertPath = '\\src\\constants'.join(path.rsplit('\\src\\utility', 1))
# sys.path.append(insertPath)


# from constants.internal_config import FR_DETECTION_METHOD, FR_DATASET_PATH, FR_ENCODINGS_DUMP_PATH, \
#                                       VERY_HIGH_MATCH_COUNT
# from utility.file_operations import read_json_from_file
# from constants.ui_operation import SETTINGS_JSON_FILE_PATH

import os
import face_recognition
import cv2
import pickle
import json 

# CONSTANTS - TODO: Fix imports for constants and utility
FR_DETECTION_METHOD = 'hog'
FR_DATASET_PATH = '../../dataset' #this is diff compared to the constants file
FR_ENCODINGS_DUMP_PATH = '../../fr_encodings.pickle' # this is changed compared to the constants file
VERY_HIGH_MATCH_COUNT = 1000000
SETTINGS_JSON_FILE_PATH = 'internal/json/settings.json'
def read_json_from_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)
    

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


# def fr_recognize(data, testImage):
#   '''
#     Input: Encoding data, image
#     Output: Match name, Match count
#     Function to do face recognition using the face recognition model
#   '''
#   DETECTION_METHOD = FR_DETECTION_METHOD
#   SILENT_MODE = read_json_from_file(SETTINGS_JSON_FILE_PATH)['SILENT_MODE']
#   VERY_HIGH_MATCH_COUNT = VERY_HIGH_MATCH_COUNT

#   # load the input image and convert it from BGR to RGB
#   image = cv2.imread(testImage)
#   rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

#   # detect the (x,y)-coordinates of the bounding boxes cooresponding to each
#   # face in the input image, then compute the facial embeddings for each face
#   boxes = face_recognition.face_locations(rgb_image, model=DETECTION_METHOD)
#   encodings = face_recognition.face_encodings(rgb_image, boxes)

#   # initialize the list of names for each face detected
#   names = []
#   match_counts = []

#   # loop over the facial embeddings
#   for e_i, encoding in enumerate(encodings):
#       # attempt to match each face in the input to our known encodings
#       # This function returns a list of True / False  values, one for each image in our dataset.
#       matches = face_recognition.compare_faces(data["encodings"], encoding)
#       # print(face_recognition.face_distance(data["encodings"], encoding))
#       name = "Unknown"
#       name_count = 0

#       # check to see if we have found any matches
#       if True in matches:
#           # find the indexes of all matched faces then initialize a dictionary to count
#           # the total number of times each face was matched
#           matchedIdxs = [i for (i, b) in enumerate(matches) if b]
#           counts = {}

#           # loop over the matched indexes and maintain a count for each recognized face face
#           for i in matchedIdxs:
#               name = data['names'][i]
#               counts[name] = counts.get(name, 0) + 1

#           # determine the recognized face with the largest number of votes: (notes: in the event of an unlikely
#           # tie, Python will select first entry in the dictionary)
#           # name = max(counts, key=counts.get)
#           name, name_count = max(counts.items(), key=lambda x: x[1])
#       else:
#         if not SILENT_MODE:
#           top, right, bottom, left = boxes[e_i]  # Extract face coordinates
#           top -= 110
#           right += 110
#           bottom += 110
#           left -= 110

#           # ensure within bounds
#           top = max(top, 0)
#           left = max(left, 0)

#           if not os.path.exists(TEMP_IMG_STORAGE_PATH):
#             # If it doesn't exist, create the directory
#             os.makedirs(TEMP_IMG_STORAGE_PATH)

#           # Create a PIL Image from the face region
#           face_image = Image.fromarray(rgb_image[top:bottom, left:right])
#           # Save the face image as a separate file
#           temp_img_save_path = f"{TEMP_IMG_STORAGE_PATH}/face_{e_i}.jpg"
#           face_image.save(temp_img_save_path)

#       names.append(name)
#       match_counts.append(name_count)

#   # end_time = time.time()
#   # print("Image recognition took ", end_time - start_time , " sec!")
#   # print(testImage, names)
#   # print(testImage, match_counts)
#   # print("#########################################################")

#   # # loop over the recognized faces
#   # for ((top, right, bottom, left), name) in zip(boxes, names):
#   #     # draw the predicted face name on the image
#   #     cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
#   #     y = top - 15 if top - 15 > 15 else top + 15
#   #     cv2.putText(image, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
#   #                 0.75, (0, 255, 0), 2)

#   if not SILENT_MODE and os.path.exists(TEMP_IMG_STORAGE_PATH):
#     # GIVES errors on google colab
#     # unknown_people_identification_message()
#     print("The following people weren't identified. Please help me by identifying them.")
#     print("The image file names are displayed below. The files are located in ", TEMP_IMG_STORAGE_PATH)
#     print(f"If you don't know their name or do not wish to identify them, type \"{DECLINE_TO_IDENTIFY}\"")
#     file_list = os.listdir(TEMP_IMG_STORAGE_PATH)
#     encoded_data = fr_load_encodings()
#     for file_name in file_list:
#       if file_name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
#         identity_input = input(f"Please identify {file_name} in the image above: ")
#         if identity_input != DECLINE_TO_IDENTIFY:
#           if identity_input.lower() not in os.listdir(FR_DATASET_PATH):
#             # create a new directory and insert the image
#             if not os.path.exists(f"{FR_DATASET_PATH}/{identity_input.lower()}"):
#               os.makedirs(f"{FR_DATASET_PATH}/{identity_input.lower()}")
#           shutil.copy(f"{TEMP_IMG_STORAGE_PATH}/{file_name}", f"{FR_DATASET_PATH}/{identity_input.lower()}/{file_name[:-4]}-{time.time()}.jpg")
#           TRAIN_COUNT_MAP[identity_input.lower()] = 1 + TRAIN_COUNT_MAP.get(identity_input.lower(), 0)

#           # add to the fr encodings
#           unknown_person_image = cv2.imread(f"{TEMP_IMG_STORAGE_PATH}/{file_name}")
#           rgb_unknown_person_image = cv2.cvtColor(unknown_person_image, cv2.COLOR_BGR2RGB)
#           req_encoding = face_recognition.face_encodings(rgb_unknown_person_image, face_recognition.face_locations(rgb_unknown_person_image, model=DETECTION_METHOD))
#           encoded_data["encodings"].append(req_encoding[0])
#           encoded_data["names"].append(identity_input.lower())
#           # add this to "names" and "match_counts"
#           names.append(identity_input.lower())
#           match_counts.append(VERY_HIGH_MATCH_COUNT)

#     # replace existing encoding
#     fr_dump_data(encoded_data)

#     # clean up of the stored images
#     delete_folder(TEMP_IMG_STORAGE_PATH)


#   # # show the tested image
#   # cv2_imshow(image)
#   # cv2.waitKey(0)

#   return names, match_counts


# def unknown_people_identification_message():
#   print("The following people weren't identified. Please help us by identifying them.")
#   print("The images and their id's are displayed below. After that you will see a prompt to type their name.")
#   print(f"If you don't know their name or do not wish to identify them, type \"{DECLINE_TO_IDENTIFY}\"")
#   # List all files in the directory
#   file_list = os.listdir(TEMP_IMG_STORAGE_PATH)

#   # Initialize a counter for image numbering
#   image_number = 1

#   # Loop through all files in the directory
#   for file_name in file_list:
#       # Construct the full file path
#       image_path = os.path.join(TEMP_IMG_STORAGE_PATH, file_name)

#       # Check if the file is an image (you can add more image extensions if needed)
#       if file_name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
#           # Read and display the image using OpenCV
#           print(file_name, ": ")
#           image = cv2.imread(image_path)
#           cv2_imshow(image)
#           image_number += 1
#           print(" ")
#           print(" ")

#   # Wait for a key press and close all image windows
#   cv2.waitKey(0)
#   cv2.destroyAllWindows()