import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk
import json

# functions
def read_json_from_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


def write_json_to_file(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)
    settings = import_settings()


def import_settings():
    return read_json_from_file(SETTINGS_JSON_FILE_PATH)


def export_settings(silent_mode):
    data = {
        "SILENT_MODE": silent_mode
    }
    write_json_to_file(SETTINGS_JSON_FILE_PATH, data)


def clear_widgets(frame):
    for widget in frame.winfo_children():
        widget.destroy()


def reset_temp_file():
    data = {
            "selected_video": ""
    }
    write_json_to_file(TEMP_JSON_FILE_PATH, data)

def open_video(info_label):
    file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi;*.mkv")])
    if file_path:
        display_selected_video(file_path, info_label)
        data = {
            "selected_video": file_path
        }
        write_json_to_file(TEMP_JSON_FILE_PATH, data)


def display_selected_video(file_path, info_label):
    info_label.pack(pady=10)
    info_label.config(text=f"Selected Video: {file_path}")


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

    frame2.tkraise()
    frame2.pack_propagate(False)
    frame2.grid(row=0, column=0)


    # HEADING
    tk.Label(
        frame2, 
        text = "AI VFX ASSISTANT UPLOAD",
        bg = bg_color,
        fg = "white",
        font = ('TkHeadingFont', 40)
    ).pack(pady=20)


    tk.Label(
        frame2,
        text="Please select a shot for processing and click the Process Shot button!",
        font=('Leelawadee', 14),
        bg = bg_color,
        fg = "white"
    ).pack(pady=5)

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
        command=lambda:open_video(info_label)
    )
    upload_button.pack(pady=20)

    # Display Image
    logoimg = ImageTk.PhotoImage(file='internal/local_assets/images/logo2_1.jpg')
    logowidget = tk.Label(
        frame2, 
        image = logoimg,
        bg=bg_color
    )
    logowidget.image = logoimg
    logowidget.pack()

    # Buttons
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
    ).pack(pady=10)

    print(info_label)

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
    ).pack(pady=5)


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
        text="Save and Back",
        font=("TkHeadingFont", 20),
        bg="#28393a",
        fg="white",
        cursor="hand2",
        activebackground="#badee2",
        activeforeground="grey",
        command=lambda:(export_settings(selected_option.get()), load_frame1())
    ).pack(pady=20)



    




    

# GLOBAL VARS
bg_color = "#2b2e2e"
SETTINGS_JSON_FILE_PATH = 'internal/json/settings.json'
TEMP_JSON_FILE_PATH = 'internal/json/temp.json'
settings = import_settings()

# initialize app
root = tk.Tk()
root.title("AI VFX Assistant")
# root.geometry('800x600+150+10')
# root.eval("tk::PlaceWindow . center")

# create a frame widget
frame1 = tk.Frame(root, width=1000, height=600, bg=bg_color)
frame2 = tk.Frame(root, width=1000, height=600, bg=bg_color)
frame3 = tk.Frame(root, width=1000, height=600, bg=bg_color)
settings_frame = tk.Frame(root, width=1000, height=600, bg=bg_color)

frame1.grid(row=0, column=0)

load_frame1()

# run app
root.mainloop()