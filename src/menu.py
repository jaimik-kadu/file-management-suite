import tkinter as tk
from tkinter import ttk

from folder_cleaner import FolderCleaner
from duplicate_finder import DuplicateFinder
from disk_space_monitor import StorageInfoApp
from media_organizer import MediaCleaner
from temp_file_remover import WindowsTempCleaner

class Menu(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.folder_cleaner = FolderCleaner(parent.content)
        self.duplicate_finder = DuplicateFinder(parent.content)
        self.media_organizer = MediaCleaner(parent.content)
        self.disk_monitor = StorageInfoApp(parent.content)
        self.temp_file_remover = WindowsTempCleaner()

        self.grid(row=0, column=0, sticky="nswe")

        # Define a style for the buttons
        style = ttk.Style()
        style.configure("Custom.TButton", font=("Helvetica", 16))

        self.create_widgets()
    
    def create_widgets(self):

        # Create widgets

        # Working
        file_organizer = ttk.Button(self, text="File Organizer", style="Custom.TButton", command=self.folder_cleaner.organize_files, width=15)
        duplicates_finder = ttk.Button(self, text="Find Duplicates", style="Custom.TButton", command=self.duplicate_finder.find_duplicates, width=15)
        organize_media = ttk.Button(self, text="Organize Media", style="Custom.TButton", command=self.media_organizer.organize_media_files, width=15)
        temp_files_deleter = ttk.Button(self, text="Remove Temp Files", style="Custom.TButton", command=self.temp_file_remover.scan_and_delete_temp_files, width=15)
        monitor_disk_space = ttk.Button(self, text="Monitor Disk Space", style="Custom.TButton", command=self.disk_monitor.display_storage_info, width=15)

        # Configure rows and columns
        self.columnconfigure(0, weight=1, uniform='a')
        for i in range(9):
            self.rowconfigure(i, weight=1, uniform='a')

        # Place widgets
        file_organizer.grid(row=0, column=0, sticky='nswe', pady=5, padx=10)
        duplicates_finder.grid(row=1, column=0, sticky='nswe', pady=5, padx=10)
        organize_media.grid(row=2, column=0, sticky='nswe', pady=5, padx=10)
        temp_files_deleter.grid(row=3, column=0, sticky='nswe', pady=5, padx=10)
        monitor_disk_space.grid(row=4, column=0, sticky='nswe', pady=5, padx=10)
