import os
import shutil
from tkinter import filedialog, messagebox, ttk, Canvas, Scrollbar
from datetime import datetime

# Define media file extensions
MEDIA_EXTENSIONS = {
    'images': ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.heic'],
    'audio': ['.mp3', '.wav', '.aac', '.flac', '.ogg', '.m4a'],
    'video': ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.mpg']
}

class MediaCleaner:
    def __init__(self, content_frame):
        """
        Initializes the MediaCleaner with a reference to the Content frame.
        :param content_frame: The frame in which to display the output.
        """
        self.content_frame = content_frame

    def organize_media_files(self):
        """Organizes media files (images, audio, video) by creation date (year and month)."""
        
        # Select folder to organize
        folder = filedialog.askdirectory(title="Select Folder with Media Files")
        if not folder:
            return
        
        # Track files moved
        files_moved = []

        # Iterate over each file in the folder
        for file_name in os.listdir(folder):
            file_path = os.path.join(folder, file_name)
            
            # Check if it's a file and matches any media type
            if os.path.isfile(file_path) and any(file_name.lower().endswith(ext) for ext_list in MEDIA_EXTENSIONS.values() for ext in ext_list):
                
                # Get the file's creation time and format date
                modified_time = os.path.getmtime(file_path)
                modified_date = datetime.fromtimestamp(modified_time)
                
                # Define folder names for year and month
                year_folder = os.path.join(folder, str(modified_date.year))
                month_folder = os.path.join(year_folder, modified_date.strftime('[%m] %B'))
                
                # Create directories if they don't exist
                os.makedirs(month_folder, exist_ok=True)
                
                # Move file to the appropriate year/month folder
                shutil.move(file_path, os.path.join(month_folder, file_name))
                files_moved.append(f"{file_name} -> {month_folder}")

        self.display_summary(files_moved)

    def display_summary(self, files_moved):

        canvas = Canvas(self.content_frame)  # Create a Canvas widget
        scrollbar = Scrollbar(self.content_frame, orient="vertical", command=canvas.yview)  # Create a vertical scrollbar
        canvas.configure(yscrollcommand=scrollbar.set)  # Link the scrollbar to the canvas

        # Create a frame inside the canvas for placing widgets dynamically
        inner_frame = ttk.Frame(canvas)
        
        # Add the inner_frame to the canvas window
        canvas.create_window((0, 0), window=inner_frame, anchor="nw")
        
        # Place the canvas and scrollbar in the content_frame
        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Configure grid weight so the content_frame can expand with the canvas
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

        # Bind the canvas to adjust when the content frame size changes
        inner_frame.bind(
            "<Configure>", 
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        """Displays the summary of moved files in the content frame."""
        # Clear any existing widgets in the inner frame
        for widget in inner_frame.winfo_children():
            widget.destroy()

        # Title for the summary
        title_label = ttk.Label(inner_frame, text="Media Files Organized", font=("Helvetica", 16, "bold"))
        title_label.grid(row=0, column=0, sticky="w", padx=10, pady=(10, 5))

        # Display the list of moved files
        if files_moved:
            summary_text = "\n\n".join(files_moved)
        else:
            summary_text = "No media files were found to organize."

        summary_label = ttk.Label(inner_frame, text=summary_text, anchor="w", justify="left")
        summary_label.grid(row=1, column=0, sticky="nw", padx=10, pady=10)

        # Ensure the canvas updates its size based on the content
        canvas.update_idletasks()
