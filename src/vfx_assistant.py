import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
import json
from imutils import paths
import argparse
import pickle
import cv2
import os
import face_recognition
import time
from deepface import DeepFace
from retinaface import RetinaFace
from imutils.video import VideoStream
import imutils
# os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import sys
sys.path.append('utility')
sys.path.append('constants')

from utility.file_operations import read_json_from_file, write_json_to_file, count_files_in_directory, clear_temp_selected_video, extract_first_frame
from utility.tkinter_operations import clear_widgets
from constants.ui_operation import TEMP_JSON_FILE_PATH, SETTINGS_JSON_FILE_PATH, bg_color
from constants.internal_config import FR_DATASET_PATH
from utility.face_recognition_operations import fr_encoding_gen, fr_dump_encodings, fr_load_encodings

# functions
def import_settings():
    return read_json_from_file(SETTINGS_JSON_FILE_PATH)


def export_settings(silent_mode):
    data = {
        "SILENT_MODE": silent_mode
    }
    write_json_to_file(SETTINGS_JSON_FILE_PATH, data)


def reset_temp_file():
    data = {
            "selected_video": ""
    }
    write_json_to_file(TEMP_JSON_FILE_PATH, data)


def open_video(info_label, logowidget, cancel_button, process_shot_button, frame_2_label, upload_button):
    file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi;*.mkv")])
    if file_path:
        display_selected_video(file_path, info_label, logowidget, cancel_button, process_shot_button, frame_2_label, upload_button)
        data = {
            "selected_video": file_path
        }
        write_json_to_file(TEMP_JSON_FILE_PATH, data)


def display_selected_video(file_path, info_label, logowidget, cancel_button, process_shot_button, frame_2_label, upload_button):
    info_label.pack(pady=10)
    info_label.config(text=f"Selected Video: {file_path}")

    if file_path:
        logowidget.pack_forget()
        cancel_button.pack_forget()
        process_shot_button.pack_forget()
        frame_2_label.pack_forget()
        upload_button.pack_forget()

        logoimg = ImageTk.PhotoImage(image=extract_first_frame(file_path))
        logowidget = tk.Label(
            frame2, 
            image = logoimg,
            bg=bg_color
        )
        logowidget.image = logoimg
        logowidget.pack()

        # Process shot button display
        tk.Button(
            frame2,
            text="Process Shot",
            font=("TkHeadingFont", 25),
            bg="#28393a",
            fg="white",
            cursor="hand2",
            activebackground="#badee2",
            activeforeground="grey",
            command=lambda:load_frame3()
        ).pack(pady=10)

        # Cancel Button display
        tk.Button(
            frame2,
            text="Cancel",
            font=("TkHeadingFont", 10),
            bg="#28393a",
            fg="white",
            cursor="hand2",
            activebackground="#badee2",
            activeforeground="grey",
            command=lambda:load_frame1()
        ).pack(pady=20)
        

def count_files_in_directory_helper(directory_path):
    # Filter the items to include only subdirectories
    items = os.listdir(FR_DATASET_PATH)
    actor_folders = [item for item in items if os.path.isdir(os.path.join(FR_DATASET_PATH, item))]

    for actor in actor_folders:
        if actor not in [".ipynb_checkpoints"]:
            num_files = count_files_in_directory(f"{FR_DATASET_PATH}/{actor}")
            TRAIN_COUNT_MAP[actor] = num_files


def generate_face_recognition_encodings():
    # call the generate encoding function for face recognition algorithm
    knownNames, knownEncodings = fr_encoding_gen()

    # save encodings to the file system
    fr_dump_encodings(knownEncodings, knownNames)


def load_frame1():
    clear_widgets(settings_frame)
    clear_widgets(frame2)
    clear_widgets(frame3)

    frame1.tkraise()
    frame1.pack_propagate(False)

    reset_temp_file()
    
    # HEADING
    tk.Label(
        frame1, 
        text = "AI VFX ASSISTANT",
        bg = bg_color,
        fg = "white",
        font = ('TkHeadingFont', 40)
    ).pack(pady=20)

    # DISPLAY LOGO
    logoimg = ImageTk.PhotoImage(file='internal/local_assets/images/logo4_1.jpg')
    logowidget = tk.Label(
        frame1, 
        image = logoimg,
        bg=bg_color
    )
    logowidget.image = logoimg
    logowidget.pack()

    # OPTIONS
    tk.Button(
        frame1,
        text="Settings",
        font=("TkHeadingFont", 20),
        bg="#28393a",
        fg="white",
        cursor="hand2",
        activebackground="#badee2",
        activeforeground="grey",
        command=lambda:load_settings_frame()
    ).pack(pady=40)

    tk.Button(
        frame1,
        text="Get Started",
        font=("TkHeadingFont", 30),
        bg="#28393a",
        fg="white",
        cursor="hand2",
        activebackground="#badee2",
        activeforeground="grey",
        command=lambda:load_frame2()
    ).pack(pady=0)



def load_frame2():

    clear_widgets(frame1)
    clear_widgets(settings_frame)
    clear_widgets(frame3)
    clear_temp_selected_video(TEMP_JSON_FILE_PATH)

    frame2.tkraise()
    frame2.pack_propagate(False)
    frame2.grid(row=0, column=0)


    # HEADING
    frame_2_heading = tk.Label(
        frame2, 
        text = "AI VFX ASSISTANT UPLOAD",
        bg = bg_color,
        fg = "white",
        font = ('TkHeadingFont', 40)
    )
    frame_2_heading.pack(pady=20)


    frame_2_label = tk.Label(
        frame2,
        text="Please select a shot for processing and click the Process Shot button!",
        font=('Leelawadee', 14),
        bg = bg_color,
        fg = "white"
    )
    frame_2_label.pack(pady=5)

    # Image init
    logoimg = ImageTk.PhotoImage(file='internal/local_assets/images/logo2_1.jpg')
    logowidget = tk.Label(
        frame2, 
        image = logoimg,
        bg=bg_color
    )
    logowidget.image = logoimg

    # Cancel Button init
    cancel_button = tk.Button(
        frame2,
        text="Cancel",
        font=("TkHeadingFont", 10),
        bg="#28393a",
        fg="white",
        cursor="hand2",
        activebackground="#badee2",
        activeforeground="grey",
        command=lambda:load_frame1()
    )

    # Process shot button
    process_shot_button = tk.Button(
        frame2,
        text="Process Shot",
        font=("TkHeadingFont", 25),
        bg="#28393a",
        fg="white",
        cursor="hand2",
        activebackground="#badee2",
        activeforeground="grey",
        command=lambda:load_frame3()
    )

    # SHOT SELECTION
    info_label = tk.Label(frame2, text="Selected Video: None")
    upload_button = tk.Button(
        frame2, 
        text="Upload Shot", 
        font=("TkHeadingFont", 20),
        bg="#28393a",
        fg="white",
        cursor="hand2",
        activebackground="#badee2",
        activeforeground="grey",
        command=lambda:open_video(info_label, logowidget, cancel_button, process_shot_button, frame_2_label, upload_button)
    )
    upload_button.pack(pady=20)

    # Display Image
    logowidget.pack()

    # Display Process shot button
    process_shot_button.pack(pady=10)

    # Display Cancel button
    cancel_button.pack(pady=10)


def load_frame3():
    clear_widgets(frame1)
    clear_widgets(frame2)
    clear_widgets(settings_frame)

    frame3.tkraise()
    frame3.pack_propagate(False)
    frame3.grid(row=0, column=0)

    # Heading
    tk.Label(
        frame3, 
        text = "AI VFX ASSISTANT PROCESSING",
        bg = bg_color,
        fg = "white",
        font = ('TkHeadingFont', 40)
    ).pack(pady=20)

    # extract video to process
    temp_data = read_json_from_file(TEMP_JSON_FILE_PATH)
    if temp_data['selected_video'] == "":
        load_frame1()




def load_settings_frame():
    clear_widgets(frame1)
    clear_widgets(frame2)
    clear_widgets(frame3)

    settings_frame.tkraise()
    settings_frame.pack_propagate(False)
    settings_frame.grid(row=0, column=0)

    # Heading
    tk.Label(
        settings_frame, 
        text = "AI VFX ASSISTANT SETTINGS",
        bg = bg_color,
        fg = "white",
        font = ('TkHeadingFont', 40)
    ).pack(pady=20)

    # Silent mode setting
    settings = import_settings()
    choice = tk.StringVar()
    choice.set(settings['SILENT_MODE'])
    selected_option = tk.StringVar()
    selected_option.set(settings['SILENT_MODE'])

    # tk.Label(
    #     settings_frame, 
    #     textvariable=selected_option, 
    #     font=('Arial', 12)
    # ).pack(pady=10)

    # SILENT MODE SETTING
    tk.Label(
        settings_frame,
        text="Do you want to enable silent mode?\n Note: When silent mode is enabled, no prompts will be displayed for unidentified actors.",
        font=('Leelawadee', 14),
        bg = bg_color,
        fg = "white"
    ).pack(pady=10)

    tk.Radiobutton(
        settings_frame,
        text="Yes", 
        variable=choice, 
        value="True", 
        bg="#c1d7d9",
        cursor="hand2",
        command=lambda:selected_option.set(choice.get())
    ).pack()
    
    tk.Radiobutton(
        settings_frame,
        text="No", 
        variable=choice, 
        value="False", 
        bg="#c1d7d9",
        cursor="hand2",
        command=lambda:selected_option.set(choice.get())
    ).pack(pady=10)

    # Back button
    tk.Button(
        settings_frame,
        text="Save & Back",
        font=("TkHeadingFont", 20),
        bg="#28393a",
        fg="white",
        cursor="hand2",
        activebackground="#badee2",
        activeforeground="grey",
        command=lambda:(export_settings(selected_option.get()), load_frame1())
    ).pack(pady=20)

    tk.Button(
        settings_frame,
        text="Generate Encodings",
        font=("TkHeadingFont", 20),
        bg="#28393a",
        fg="white",
        cursor="hand2",
        activebackground="#badee2",
        activeforeground="grey",
        command=lambda:generate_face_recognition_encodings()
    ).pack(pady=20)



# GLOBAL VARS
settings = import_settings()
TRAIN_COUNT_MAP = {}

# initialize app
root = tk.Tk()
root.title("AI VFX Assistant")

# create a frame widget
frame1 = tk.Frame(root, width=1000, height=600, bg=bg_color)
frame2 = tk.Frame(root, width=1000, height=600, bg=bg_color)
frame3 = tk.Frame(root, width=1000, height=600, bg=bg_color)
settings_frame = tk.Frame(root, width=1000, height=600, bg=bg_color)

frame1.grid(row=0, column=0)

load_frame1()

# run app
root.mainloop()