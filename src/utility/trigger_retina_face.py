from retinaface import RetinaFace
import sys
from file_operations import write_json_to_file

RETINA_FACE_TEMP_PATH = '../../internal/json/retina_face_temp.json'

def count_faces(input_image):
    # print("###############################")
    # print("input image is ", input_image)
    # print("#############################")
    retina_num_faces = len(RetinaFace.extract_faces(input_image))
    write_json_to_file(RETINA_FACE_TEMP_PATH, {"face_count": retina_num_faces})
    

if __name__ == '__main__':
    count_faces(sys.argv[1])