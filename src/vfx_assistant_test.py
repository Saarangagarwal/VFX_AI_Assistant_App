import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk

bg_color = "#3d6466"

def open_video(info_label):
    file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi;*.mkv")])
    if file_path:
        display_selected_video(file_path, info_label)


def display_selected_video(file_path, info_label):
    info_label.pack(pady=10)
    info_label.config(text=f"Selected Video: {file_path}")


def load_frame1():
    frame1.pack_propagate(False)

    # frame1 widgets
    # TODO: resizing images...
    # logoimg = ImageTk.PhotoImage(file='local_assets/images/test_img.jpg')
    # logowidget = tk.Label(frame1, 
    #                     image = logoimg,
    #                     bg=bg_color)
    # logowidget.image = logoimg
    # logowidget.pack()

    tk.Label(frame1, 
            text="ready for the game???",
            bg=bg_color,
            fg="black",
            font=('TkMenuFont', 14)
            ).pack()

    # button widget
    # tk.Button(
    #     frame1,
    #     text="Button next",
    #     font=("TkHeadingFont", 20),
    #     bg="#28393a",
    #     fg="white",
    #     cursor="hand2",
    #     activebackground="#badee2",
    #     activeforeground="black",
    #     command=lambda:load_frame2()
    # ).pack(pady=20)

    # Create a button to open the file dialog
    info_label = tk.Label(frame1, text="Selected Video: None")
    upload_button = tk.Button(frame1, text="Upload Video", command=lambda:open_video(info_label))
    upload_button.pack(pady=10)


def load_frame2():
    print("HELLO!")

# initialize app
root = tk.Tk()
root.title("AI VFX Assistant")
# root.geometry('800x600+150+10')
# root.eval("tk::PlaceWindow . center")

# create a frame widget
frame1 = tk.Frame(root, width=800, height=600, bg=bg_color)
frame2 = tk.Frame(root, bg=bg_color)
frame1.grid(row=0, column=0)
frame2.grid(row=0, column=0)

load_frame1()

# run app
root.mainloop()
