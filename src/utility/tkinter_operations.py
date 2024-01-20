def clear_widgets(frame):
    for widget in frame.winfo_children():
        widget.destroy()


def display_selected_video(file_path, info_label):
    info_label.pack(pady=10)
    info_label.config(text=f"Selected Video: {file_path}")


    