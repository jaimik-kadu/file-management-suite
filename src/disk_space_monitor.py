import os
import psutil
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def get_storage_info():
    """Fetches storage information of the system."""
    partitions = psutil.disk_partitions()
    storage_info = []

    for partition in partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            storage_info.append({
                "Device": partition.device,
                "Mountpoint": partition.mountpoint,
                "Filesystem": partition.fstype,
                "Total Space (GB)": round(usage.total / (1024 ** 3), 2),
                "Used Space (GB)": round(usage.used / (1024 ** 3), 2),
                "Free Space (GB)": round(usage.free / (1024 ** 3), 2),
                "Usage Percentage": usage.percent
            })
        except PermissionError:
            # Skip system-reserved partitions
            continue

    return storage_info

class StorageInfoApp:
    def __init__(self, content_frame):
        self.content_frame = content_frame

    def display_storage_info(self):
        """Fetches and displays storage stats with a stacked bar chart."""
        storage_info = get_storage_info()

        # Clear existing widgets in content_frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Data preparation for charts
        devices = [entry["Device"] for entry in storage_info]
        total_space = [entry["Total Space (GB)"] for entry in storage_info]
        used_space = [entry["Used Space (GB)"] for entry in storage_info]
        free_space = [entry["Free Space (GB)"] for entry in storage_info]

        # Create a Matplotlib figure with a smaller size
        fig = Figure(figsize=(6, 4), dpi=100)

        # Subplot: Stacked Bar Chart for Storage Info
        ax = fig.add_subplot(111)
        index = range(len(devices))

        # Dark theme colors
        fig.patch.set_facecolor('#2e2e2e')  # Dark background for the figure
        ax.set_facecolor('#2e2e2e')  # Dark background for the axes
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.tick_params(colors='white')
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        ax.title.set_color('white')

        # Plot the stacked bars
        ax.bar(index, used_space, label="Used Space (GB)", color="#ff6361")
        ax.bar(index, free_space, bottom=used_space, label="Free Space (GB)", color="#47d147")

        ax.set_xlabel("Drives")
        ax.set_ylabel("Space (GB)")
        ax.set_title("Disk Storage Status")
        ax.set_xticks(index)
        ax.set_xticklabels(devices, rotation=45, ha="right")
        ax.legend(facecolor='#2e2e2e', edgecolor='white', labelcolor='white')

        # Embed the Matplotlib chart into Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.content_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill="both", expand=True)

        # Draw the figure
        canvas.draw()
