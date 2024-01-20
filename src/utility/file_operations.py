import json
import os
import shutil


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