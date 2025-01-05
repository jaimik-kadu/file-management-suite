import os
import shutil
import tkinter as tk
from tkinter import messagebox

class WindowsTempCleaner:
    def __init__(self):
        self.temp_dirs = [
            os.path.expandvars(r"%TEMP%"),            # Default Windows Temp directory
            os.path.expandvars(r"%APPDATA%\Local\Temp")  # AppData Local Temp
        ]

    def scan_and_delete_temp_files(self):
        """Scan and delete files in the temporary directories."""
        deleted_files = 0
        deleted_size = 0

        for temp_dir in self.temp_dirs:
            if os.path.exists(temp_dir):
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        try:
                            file_path = os.path.join(root, file)
                            file_size = os.path.getsize(file_path)
                            os.remove(file_path)
                            deleted_files += 1
                            deleted_size += file_size
                        except Exception as e:
                            print(f"Error deleting {file_path}: {e}")

                    for dir_ in dirs:
                        try:
                            dir_path = os.path.join(root, dir_)
                            shutil.rmtree(dir_path, ignore_errors=True)
                        except Exception as e:
                            print(f"Error deleting {dir_path}: {e}")

        deleted_size_mb = deleted_size / (1024 * 1024)
        messagebox.showinfo("Cleanup Complete", f"Deleted {deleted_files} files, freeing {deleted_size_mb:.2f} MB.")

