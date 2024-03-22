from retinaface import RetinaFace
import sys
from file_operations import write_json_to_file, read_json_from_file

RETINA_FACE_TEMP_PATH = '../../internal/json/retina_face_temp.json'

def count_faces(input_image):
    return len(RetinaFace.extract_faces(input_image))
    
def main():
    retina_temp_frames = read_json_from_file(RETINA_FACE_TEMP_PATH)
    retina_updated = {}
    for frame in retina_temp_frames:
        retina_updated[frame] = count_faces(frame)
    write_json_to_file(RETINA_FACE_TEMP_PATH, retina_updated)

if __name__ == '__main__':
    main()