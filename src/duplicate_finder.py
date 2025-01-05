import os
import hashlib
import tkinter as tk
from tkinter import filedialog, ttk, messagebox


class DuplicateFinder:
    def __init__(self, content_frame):
        """
        Initializes the DuplicateFinder with a reference to the content frame.
        :param content_frame: The frame in which to display the output.
        """
        self.content_frame = content_frame

    @staticmethod
    def calculate_file_hash(file_path):
        """Calculate and return the hash of a file."""
        hash_algo = hashlib.md5()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_algo.update(chunk)
        return hash_algo.hexdigest()

    def find_duplicates(self):
        """Prompts the user to select a directory and find duplicate files."""
        directory = filedialog.askdirectory(title="Select Folder to Scan for Duplicates")
        if not directory:
            return

        file_hash_map = {}
        duplicates = []

        # Setup progress bar
        file_count = sum(len(files) for _, _, files in os.walk(directory))
        progress_window = tk.Toplevel()
        progress_window.title("Finding Duplicates")
        progress_bar = ttk.Progressbar(progress_window, length=300, mode='determinate')
        progress_bar.pack(padx=10, pady=10)
        progress_bar["maximum"] = file_count

        processed_files = 0

        # Walk through the directory and check for duplicates
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                file_hash = self.calculate_file_hash(file_path)

                if file_hash in file_hash_map:
                    duplicates.append((file_hash_map[file_hash], file_path))
                else:
                    file_hash_map[file_hash] = file_path

                # Update progress
                processed_files += 1
                progress_bar["value"] = processed_files
                progress_window.update_idletasks()

        progress_window.destroy()

        if duplicates:
            self.display_duplicates(duplicates)
        else:
            messagebox.showinfo("No Duplicates", "No duplicate files found.")

    def display_duplicates(self, duplicates):
        """Displays duplicate files in the content frame with options to delete."""
        # Clear previous content
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Create a scrollable frame
        canvas = tk.Canvas(self.content_frame)
        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=canvas.yview)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)

        duplicate_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=duplicate_frame, anchor="nw")

        # Title
        ttk.Label(duplicate_frame, text="Duplicate Files", font=("Helvetica", 18, "bold")).pack(pady=10)

        # Variables to manage checkboxes
        self.file_vars = []

        # Add checkboxes for each duplicate file
        for orig_file, dup_file in duplicates:
            var = tk.BooleanVar()
            self.file_vars.append((var, orig_file, dup_file))
            frame = ttk.Frame(duplicate_frame)
            frame.pack(anchor='w', pady=5, padx=10)

            # Display the file names
            ttk.Checkbutton(
                frame,
                text=f"Original: {os.path.basename(orig_file)}\nDuplicate: {os.path.basename(dup_file)}",
                variable=var
            ).pack(anchor='w')

        # Add Select All button
        select_all_var = tk.BooleanVar()

        def toggle_select_all():
            for var, _, _ in self.file_vars:
                var.set(select_all_var.get())

        ttk.Checkbutton(
            self.content_frame,
            text="Select All",
            variable=select_all_var,
            command=toggle_select_all
        ).pack(anchor='w', padx=10, pady=10)

        # Add Delete button
        ttk.Button(self.content_frame, text="Delete Selected", command=self.delete_selected).pack(pady=10)

        # Configure scrollable region
        duplicate_frame.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

    def delete_selected(self):
        """Deletes selected duplicate files."""
        deleted_files = 0

        for var, orig_file, dup_file in self.file_vars:
            if var.get():
                try:
                    # Compare modification times and delete the newer file
                    orig_mod_time = os.path.getmtime(orig_file)
                    dup_mod_time = os.path.getmtime(dup_file)

                    if dup_mod_time > orig_mod_time:
                        os.remove(dup_file)
                        deleted_files += 1
                    else:
                        os.remove(orig_file)
                        deleted_files += 1
                except Exception as e:
                    messagebox.showerror("Error", f"Could not delete file\n{e}")
        
        # Clear previous content
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        messagebox.showinfo("Deletion Complete", f"Deleted {deleted_files} duplicate files.")
