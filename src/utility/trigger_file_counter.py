import os
import json

def read_json_from_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)
    

TRAIN_COUNT_MAP_FILE_PATH = '../../internal/json/train_count_map.json'
FR_DATASET_PATH = '../../internal/internal_dataset'

def count_files_in_directory_helper():
    # Filter the items to include only subdirectories
    TRAIN_COUNT_MAP = {}
    global FR_DATASET_PATH
    items = os.listdir(FR_DATASET_PATH)
    actor_folders = [item for item in items if os.path.isdir(os.path.join(FR_DATASET_PATH, item))]

    for actor in actor_folders:
        if actor not in [".ipynb_checkpoints"]:
            num_files = count_files_in_directory(f"{FR_DATASET_PATH}/{actor}")
            TRAIN_COUNT_MAP[actor] = num_files
    
    write_json_to_file(TRAIN_COUNT_MAP_FILE_PATH, {"TRAIN_COUNT_MAP": TRAIN_COUNT_MAP})


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
  

def write_json_to_file(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)


if __name__ == '__main__':
    count_files_in_directory_helper()

