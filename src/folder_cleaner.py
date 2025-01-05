import os
import shutil
from tkinter import filedialog
from tkinter import ttk
import tkinter as tk

FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".heic"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx", ".csv"],
    "Videos": [".mp4", ".mov", ".avi", ".mkv"],
    "Music": [".mp3", ".wav", ".aac"],
    "Archives": [".zip", ".rar", ".tar", ".gz"],
    "Programs": [".exe", ".msi", ".apk"],
    "Others": []
}

class FolderCleaner:
    def __init__(self, content_frame):
        """
        Initializes the FolderCleaner with a reference to the Content frame.
        :param content_frame: The frame in which to display the output.
        """
        self.content_frame = content_frame

    def organize_files(self):
        """Prompts the user to select a directory and organizes files by type."""
        folder = filedialog.askdirectory(title="Select Folder to Clean")
        if not folder:
            return

        # Dictionary to store files for each category
        file_summary = {category: [] for category in FILE_CATEGORIES.keys()}
        # Move files into the appropriate category folders
        for file_name in os.listdir(folder):
            file_path = os.path.join(folder, file_name)

            if os.path.isfile(file_path):
                moved = False
                for category, extensions in FILE_CATEGORIES.items():
                    if any(file_name.lower().endswith(ext) for ext in extensions):
                        category_path = os.path.join(folder, category)
                        
                        # Check if the folder has files to be moved before creating it
                        if not moved and not file_summary[category]:
                            os.makedirs(category_path, exist_ok=True)

                        shutil.move(file_path, category_path)
                        file_summary[category].append(file_name)
                        moved = True
                        break

                if not moved:
                    # Move to 'Others' folder if no category matches
                    others_path = os.path.join(folder, "Others")
                    if not os.path.exists(others_path):
                        os.makedirs(others_path, exist_ok=True)
                    shutil.move(file_path, others_path)
                    file_summary["Others"].append(file_name)

        self.display_summary(file_summary)

    def display_summary(self, file_summary):
        """Displays the file summary in the content frame with a scrollbar."""
        # Clear any existing widgets in the content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Create a canvas to enable scrolling
        canvas = tk.Canvas(self.content_frame)
        canvas.pack(side="left", fill="both", expand=True)

        # Add a scrollbar and link it to the canvas
        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Create a frame inside the canvas
        summary_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=summary_frame, anchor="nw")

        # Title for the summary
        title_label = ttk.Label(summary_frame, text="Summary", font=("Helvetica", 18, "bold"))
        title_label.grid(row=0, column=0, sticky="w", padx=10, pady=(10, 5))

        # Display the summary text
        summary_text = "Files organized:\n"
        for category, files in file_summary.items():
            if len(files) != 0:
                summary_text += f"\n{category} ({len(files)} files):\n"
                summary_text += "\n".join(f"  - {file}" for file in files)
                summary_text += "\n"

        summary_label = ttk.Label(summary_frame, text=summary_text, anchor="w", justify="left")
        summary_label.grid(row=1, column=0, sticky="nw", padx=10, pady=10)

        # Adjust the canvas scroll region
        summary_frame.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))
