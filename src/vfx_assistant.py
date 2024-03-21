import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
import json
import imutils
from imutils import paths
import argparse
import pickle
import cv2
import os
import time
# from deepface import DeepFace
# from retinaface import RetinaFace
from imutils.video import VideoStream
import subprocess
import threading
from tkinter import ttk

import sys
sys.path.append('constants')
sys.path.append('scripts')

from utility.file_operations import read_json_from_file, write_json_to_file, count_files_in_directory, clear_temp_selected_video, extract_first_frame
from utility.tkinter_operations import clear_widgets
from constants.ui_operation import TEMP_JSON_FILE_PATH, SETTINGS_JSON_FILE_PATH, bg_color
from constants.internal_config import FR_DATASET_PATH

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


def generate_face_recognition_encodings():

    def run_subprocess(progressbar):
        kk = subprocess.run(["bash", "-c", "src/scripts/generate_fr_encodings.sh arguments"], capture_output=True, text=True)
        print(kk)
        progressbar.stop()
        progressbar.place_forget()

        # Success pop-up display and dismiss
        def dismiss_popup(popup):
            popup.destroy()

        popup = tk.Toplevel()
        popup.title("Success!")

        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()
        x = (screen_width - 200) // 2  # 200 is the width of the pop-up window
        y = (screen_height - 100) // 2  # 100 is the height of the pop-up window
        popup.geometry(f"300x200+{x}+{y}")  # Set the geometry of the pop-up window
        
        label = tk.Label(popup, text="Encodings generated successfully!")
        label.pack(pady=10)
        dismiss_button = tk.Button(popup, text="Dismiss", command=lambda: dismiss_popup(popup))
        dismiss_button.pack()

    progressbar = ttk.Progressbar(settings_frame, mode="determinate")
    progressbar.place(relx=0.35, rely=0.75, width=300)

    progress_thread = threading.Thread(target=run_subprocess, args=(progressbar,))
    progress_thread.start()
    # Start the progress bar animation with 2000 ms interval
    progressbar.start(2000)


def load_frame1():
    clear_widgets(settings_frame)
    clear_widgets(frame2)
    clear_widgets(frame3)
    clear_widgets(frame4)
    clear_widgets(about_frame)

    frame1.tkraise()
    frame1.pack_propagate(False)

    reset_temp_file()
    global initial_file_scan

    if not initial_file_scan:
        initial_file_scan = True
        write_json_to_file(TRAIN_COUNT_MAP_FILE_PATH, {})
        subprocess.run(["bash", "-c", "src/scripts/trigger_file_counter.sh arguments"], capture_output=True, text=True)
    
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
        text="About",
        font=("TkHeadingFont", 19),
        bg="#28393a",
        fg="white",
        cursor="hand2",
        activebackground="#badee2",
        activeforeground="grey",
        command=lambda:load_about_frame()
    ).pack(pady=10)

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
    ).pack(pady=10)

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
    clear_widgets(frame4)
    clear_widgets(frame3)
    clear_widgets(about_frame)
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
    clear_widgets(frame4)
    clear_widgets(about_frame)

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

    def run_recognition_subprocess(progressbar):
        kk = subprocess.run(["bash", "-c", "src/scripts/trigger_frame_recognizer.sh arguments"], capture_output=True, text=True)
        print(kk)
        # import time;time.sleep(5)
        progressbar.stop()
        progressbar.place_forget()
        load_frame4()

    # extract video to process
    temp_data = read_json_from_file(TEMP_JSON_FILE_PATH)
    write_json_to_file(RECOGNIZED_PEOPLE_PATH, {"recognized_people": []})
    if temp_data['selected_video'] == "":
        load_frame1()
    else:
        # display the selected video
        logoimg = ImageTk.PhotoImage(image=extract_first_frame(temp_data['selected_video']))
        logowidget = tk.Label(
            frame3, 
            image = logoimg,
            bg=bg_color
        )
        logowidget.image = logoimg
        logowidget.pack()

        # display progress bar
        progressbar = ttk.Progressbar(frame3, mode="determinate")
        progressbar.place(relx=0.35, rely=0.75, width=300)

        progress_thread = threading.Thread(target=run_recognition_subprocess, args=(progressbar,))
        progress_thread.start()
        # Start the progress bar animation with 2000 ms interval
        progressbar.start(2000)

        # display text below label
        progress_label = tk.Label(frame3, text="Face recognition in progress using the magic of AI", anchor="w", font=('Leelawadee', 10))
        progress_label.place(relx=0.35, rely=0.8)
        progress_label = tk.Label(frame3, text="Note: You may see pop-ups if silent mode is disabled", anchor="w", font=('Leelawadee', 10))
        progress_label.place(relx=0.34, rely=0.83)


def load_frame4():
    clear_widgets(frame1)
    clear_widgets(frame2)
    clear_widgets(frame3)
    clear_widgets(settings_frame)
    clear_widgets(about_frame)

    frame4.tkraise()
    frame4.pack_propagate(False)
    frame4.grid(row=0, column=0)

    # Heading
    tk.Label(
        frame4, 
        text = "AI VFX ASSISTANT RESULTS",
        bg = bg_color,
        fg = "white",
        font = ('TkHeadingFont', 40)
    ).pack(pady=20)

    tk.Button(
        frame4,
        text="Back to Home",
        font=("TkHeadingFont", 10),
        bg="#28393a",
        fg="white",
        cursor="hand2",
        activebackground="#badee2",
        activeforeground="grey",
        command=lambda:load_frame1()
    ).pack()

    recognized_people = read_json_from_file(RECOGNIZED_PEOPLE_PATH)["recognized_people"]
    print(recognized_people)


def load_settings_frame():
    clear_widgets(frame1)
    clear_widgets(frame2)
    clear_widgets(frame3)
    clear_widgets(frame4)
    clear_widgets(about_frame)

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


def load_about_frame():
    clear_widgets(frame1)
    clear_widgets(frame2)
    clear_widgets(frame3)
    clear_widgets(frame4)
    clear_widgets(settings_frame)

    about_frame.tkraise()
    about_frame.pack_propagate(False)
    about_frame.grid(row=0, column=0)

    # Heading
    tk.Label(
        about_frame, 
        text = "ABOUT AI VFX ASSISTANT",
        bg = bg_color,
        fg = "white",
        font = ('TkHeadingFont', 40)
    ).pack(pady=20)

    # Create a paragraph of text
    text = """Welcome to the AI (Artificial Intelligence) Visual Effects (VFX) Assistant. This tool is 
designed to assist VFX editors in speeding up asset..... face recognition.... What makes this tool special
is its ability to add new faces and learn on the go as you use it. Don't want to get prompted to help the 
tool get better? No worries, enabling silent mode in the settings menu allows for uninterrupted use of the 
tool. ....talk about embeddings...out of the box... can be generated.... talk about how to select shot and 
how the workflow goes along. At the end, also mention the developer/professor.............................
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer nec odio. Praesent libero. 
Sed cursus ante dapibus diam. Sed nisi. Nulla quis sem at nibh elementum imperdiet. 
Duis sagittis ipsum. Praesent mauris. Fusce nec tellus sed augue semper porta. Mauris massa. 
Vestibulum lacinia arcu eget nulla. Class aptent taciti sociosqu ad litora torquent per conubia nostra, 
per inceptos himenaeos. Curabitur sodales ligula in libero. Sed dignissim lacinia nunc."""

    # Create a Label to display the paragraph of text
    text_label = tk.Label(about_frame, text=text, justify="left", font=("Leelawadee", 12))
    text_label.pack()

    # Back button
    tk.Button(
        about_frame,
        text="Back",
        font=("TkHeadingFont", 18),
        bg="#28393a",
        fg="white",
        cursor="hand2",
        activebackground="#badee2",
        activeforeground="grey",
        command=lambda:load_frame1()
    ).pack(pady=20)

# GLOBAL VARS
settings = import_settings()
TRAIN_COUNT_MAP_FILE_PATH = 'internal/json/train_count_map.json'
RECOGNIZED_PEOPLE_PATH = 'internal/json/recognized_people.json'
initial_file_scan = False

# initialize app
root = tk.Tk()
root.title("AI VFX Assistant")

# create a frame widget
frame1 = tk.Frame(root, width=1000, height=600, bg=bg_color)
frame2 = tk.Frame(root, width=1000, height=600, bg=bg_color)
frame3 = tk.Frame(root, width=1000, height=600, bg=bg_color)
frame4 = tk.Frame(root, width=1000, height=600, bg=bg_color)
settings_frame = tk.Frame(root, width=1000, height=600, bg=bg_color)
about_frame = tk.Frame(root, width=1000, height=600, bg=bg_color)


frame1.grid(row=0, column=0)

load_frame1()

# run app
root.mainloop()