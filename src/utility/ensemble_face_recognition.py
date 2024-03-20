import cv2
import face_recognition
from file_operations import read_json_from_file, write_json_to_file
from face_recognition_operations import fr_load_encodings, fr_recognize
# from deep_face_operations import vgg_recognition
import subprocess

# globals
FR_DETECTION_METHOD = 'hog'
VGG_ACCEPTANCE_PARAMETER = 0.15
STRICT_ACCEPTANCE_PARAMETER = 0.20
COURTESY_ACCEPTANCE_PARAMETER = 0.05
FR_ACCEPTANCE_PARAMETER = 0.15
TRAIN_COUNT_MAP_PATH = '../../internal/json/train_count_map.json'
RETINA_FACE_TEMP_PATH = '../../internal/json/retina_face_temp.json'
DEEP_FACE_TEMP_PATH = '../../internal/json/deep_face_temp.json'

def image_face_recognition(input_image):
  '''
    INPUT: image path
    OUTPUT: recognized match names
    Enemble algorithm for face recognition
  '''
  # find the number of faces in the image using retinaFace and face_locations
  # Note: it is noticed that face_locations is not very accurate in detecting faces
  # if no. of faces detected by face_locations and retinaFace is different - use VGG
  # if no. of faces detected by face_locations and retinaFace is same, then use formulated strategy
  image = cv2.imread(input_image)
  rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
  boxes = face_recognition.face_locations(rgb_image, model=FR_DETECTION_METHOD)
  fr_num_faces = len(boxes)
  print("$$$$$$FR FACE NUM$$$$$$$$$ is ", fr_num_faces)

  # run subprocess to get number of faces from retina face
  write_json_to_file(RETINA_FACE_TEMP_PATH, {"face_count": 0})
  subprocess.run(["bash", "-c", f"../scripts/trigger_retina_face.sh {input_image}"], capture_output=True, text=True)
  retina_num_faces = read_json_from_file(RETINA_FACE_TEMP_PATH)["face_count"]
  TRAIN_COUNT_MAP = read_json_from_file(TRAIN_COUNT_MAP_PATH)['TRAIN_COUNT_MAP']
  print("RETINAAAAA DONE ", retina_num_faces, "number ONLY!!")

  if fr_num_faces != retina_num_faces:
    # use vgg... use face_recognition if confidence in outcome is low
    vgg_flagged_people = {}

    # vgg recognition call
    vgg_temp_json = {
      "vgg_matches_op": [],
      "vgg_matches_count_op": []
    }
    print("HOOOOHAHAHA")
    write_json_to_file(DEEP_FACE_TEMP_PATH, vgg_temp_json)
    kk = subprocess.run(["bash", "-c", f"../scripts/trigger_deep_face.sh {input_image}"], capture_output=True, text=True)
    print(kk)
    # vgg_matches, vgg_match_counts = vgg_recognition(input_image)
    vgg_temp_json = read_json_from_file(DEEP_FACE_TEMP_PATH)
    vgg_matches, vgg_match_counts = vgg_temp_json['vgg_matches_op'], vgg_temp_json['vgg_matches_count_op']

    vgg_matches_copy = vgg_matches.copy()
    for i, count in enumerate(vgg_match_counts):
      person = vgg_matches[i]
      if person != "Unknown" and count < (VGG_ACCEPTANCE_PARAMETER * TRAIN_COUNT_MAP[person]):
        vgg_flagged_people[person] = count
        vgg_matches_copy.remove(person)

    # return result if counts agree with the acceptance criteria
    if not vgg_flagged_people:
      # print("VGGVGVGVGGVGVGVVGVGVGVGVGVGVGVGVG")
      return vgg_matches

    # if vgg is not perfect here, then combine with high acceptance results from face recognition
    fr_encoding_data = fr_load_encodings()
    fr_matches, fr_match_counts = fr_recognize(fr_encoding_data, input_image)
    for i, count in enumerate(fr_match_counts):
      person = fr_matches[i]
      if person != "Unknown" and count >= (STRICT_ACCEPTANCE_PARAMETER * TRAIN_COUNT_MAP[person]) and person not in vgg_matches_copy:
        vgg_matches_copy.append(person)
    return vgg_matches_copy

  else:
    # same no. of faces
    # use face_recognition and then vgg if required
    fr_encoding_data = fr_load_encodings()
    fr_matches, fr_match_counts = fr_recognize(fr_encoding_data, input_image)
    fr_flagged_people = {}
    for i, count in enumerate(fr_match_counts):
      person = fr_matches[i]
      if person != "Unknown" and count < (FR_ACCEPTANCE_PARAMETER * TRAIN_COUNT_MAP[person]):
        fr_flagged_people[person] = count

    # return result if counts agree with the acceptance criteria
    if not fr_flagged_people:
      # print("FRFRFRFRFRFRFRFRFRFRFFRFRFRF")
      return fr_matches

    # if people are flagged, combine info from vgg
    vgg_flagged_people = {}
    
    # vgg recognition call
    vgg_temp_json = {
      "vgg_matches_op": [],
      "vgg_matches_count_op": []
    }
    write_json_to_file(DEEP_FACE_TEMP_PATH, vgg_temp_json)
    kk = subprocess.run(["bash", "-c", f"../scripts/trigger_deep_face.sh {input_image}"], capture_output=True, text=True)
    print(kk)
    # vgg_matches, vgg_match_counts = vgg_recognition(input_image)
    vgg_temp_json = read_json_from_file(DEEP_FACE_TEMP_PATH)
    vgg_matches, vgg_match_counts = vgg_temp_json['vgg_matches_op'], vgg_temp_json['vgg_matches_count_op']


    vgg_matches_copy = vgg_matches.copy()
    for i, count in enumerate(vgg_match_counts):
      person = vgg_matches[i]
      if person != "Unknown" and count < (VGG_ACCEPTANCE_PARAMETER * TRAIN_COUNT_MAP[person]):
        vgg_flagged_people[person] = count
        vgg_matches_copy.remove(person)

    # return result if counts agree with the acceptance criteria
    if not vgg_flagged_people:
      # print("VGGVGVGVGGVGVGVVGVGVGVGVGVGVGVGVG")
      return vgg_matches

    # at this point, both algos are uncertain about atleast 1 person in the image
    for vgg_key, vgg_value in vgg_flagged_people.items():
      # if same people flagged by both algo, check if they can be shown courtesy
      if vgg_key in fr_flagged_people and \
             max(vgg_value, fr_flagged_people[vgg_key] if vgg_key in fr_flagged_people else 0) >= COURTESY_ACCEPTANCE_PARAMETER * TRAIN_COUNT_MAP[vgg_key]:
        vgg_matches_copy.append(vgg_key)

    # do strict acceptance from fr_matches
    final_matches = set(vgg_matches_copy)
    for i, count in enumerate(fr_match_counts):
      person = fr_matches[i]
      if person != "Unknown" and count >= STRICT_ACCEPTANCE_PARAMETER * TRAIN_COUNT_MAP[person]:
        final_matches.add(person)

    # print("finalFinalFinalFinalFinal")
    return final_matches
