#!/usr/bin/env python
from tkinter import Tk, filedialog, Label, Button, Text, Scrollbar
from PIL import Image, ImageTk
from pillow_heif import register_heif_opener
import os

class ConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HEIC to JPEG Converter")

        self.label = Label(root, text="Click the button below to convert HEIC images to JPEG and rename them.")
        self.label.pack(pady=10)

        self.convert_button = Button(root, text="Browse for folder", command=self.process_folder)
        self.convert_button.pack()

        self.status_text = Text(root, wrap="word", height=10)
        self.status_text.pack(fill="both", expand=True)

        self.scrollbar = Scrollbar(root, command=self.status_text.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.status_text.config(yscrollcommand=self.scrollbar.set)

        self.images = []  # Store PhotoImage instances
        self.root.mainloop()

    def convert_and_rename(self, folder_path):
        input_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.heic') or f.lower().endswith('.png') or f.lower().endswith('.jpg')]

        for index, input_file in enumerate(input_files, start=1):
            input_path = os.path.join(folder_path, input_file)
            folder_name = os.path.basename(folder_path)
            output_filename = f"{folder_name} {index}.jpg"
            output_path = os.path.join(folder_path, output_filename)

            img = Image.open(input_path)
            img = img.convert("RGB")
            img.save(output_path, format="JPEG")

            os.remove(input_path)  # Remove the original HEIC file

            self.status_text.insert("end", f"Converting: {input_file} to {output_filename}\n")
            self.status_text.see("end")
            self.root.update()

            img=img.resize((450, 350))
            img_tk = ImageTk.PhotoImage(img)
            self.images.append(img_tk)
            self.display_image(img_tk)

            self.status_text.see("end")
            self.root.update()

    def display_image(self, img_tk):
        if hasattr(self, "img_label"):
            self.img_label.destroy()

        self.img_label = Label(self.root, image=img_tk)
        self.img_label.image = img_tk  # Keep a reference to prevent garbage collection
        self.img_label.pack()

    def process_folder(self):
        selected_folder = filedialog.askdirectory(title="Select the folder containing HEIC images")

        for root, dirs, files in os.walk(selected_folder):
            self.convert_and_rename(root)

register_heif_opener()

root = Tk()
app = ConverterApp(root)
