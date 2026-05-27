import tkinter as tk
from tkinter import filedialog, messagebox

import cv2
import numpy as np
import pandas as pd
import os

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.widgets import RectangleSelector

import plotly.graph_objects as go


# ==========================================================
# MAIN APPLICATION
# ==========================================================

class LightCurveApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Exoplanet Light Curve Tool")
        self.root.geometry("1200x800")

        self.video_path = None

        self.x1 = None
        self.y1 = None
        self.x2 = None
        self.y2 = None

        self.frame_rgb = None

        self.frame_intensities = None
        self.time_stamps = None

        self.setup_ui()


    # ======================================================
    # UI
    # ======================================================

    def setup_ui(self):
        button_frame = tk.Frame(self.root)
        button_frame.pack(side=tk.TOP, pady=10)

        tk.Button(
            button_frame,
            text="Load Video",
            command=self.load_video,
            width=20,
            height=2
        ).pack(side=tk.LEFT, padx=10)

        tk.Button(
            button_frame,
            text="Generate Light Curve",
            command=self.process_video,
            width=20,
            height=2
        ).pack(side=tk.LEFT, padx=10)

        tk.Button(
            button_frame,
            text="Save CSV",
            command=self.save_csv,
            width=20,
            height=2
        ).pack(side=tk.LEFT, padx=10)

        self.status_label = tk.Label(
            self.root,
            text="Load a video to begin",
            font=("Arial", 12)
        )

        self.status_label.pack(pady=5)

        self.fig, self.ax = plt.subplots(figsize=(8, 6))

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)
        self.canvas.draw()

    # ======================================================
    # LOAD VIDEO
    # ======================================================

    def load_video(self):
        filepath = filedialog.askopenfilename(
            filetypes=[("Video files", "*.mp4 *.mov *.avi")])

        if not filepath:
            return

        self.video_path = filepath

        cap = cv2.VideoCapture(filepath)

        if not cap.isOpened():
            messagebox.showerror("Error", "Could not open video")
            return

        ret, frame = cap.read()
        cap.release()

        if not ret:
            messagebox.showerror("Error", "Could not read first frame")
            return

        self.frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        self.display_frame()

        self.status_label.config(
            text="Drag a rectangle around the star region"
        )

    # ======================================================
    # DISPLAY FRAME
    # ======================================================

    def display_frame(self):
        self.ax.clear()
        self.ax.imshow(self.frame_rgb)
        self.ax.set_title("Select ROI")
        self.canvas.draw()

        self.rectangle_selector = RectangleSelector(
            self.ax,
            self.on_select,
            useblit=True,
            button=[1],
            minspanx=5,
            minspany=5,
            interactive=True
        )

    # ======================================================
    # ROI SELECTION
    # ======================================================

    def on_select(self, eclick, erelease):
        self.x1 = int(eclick.xdata)
        self.y1 = int(eclick.ydata)

        self.x2 = int(erelease.xdata)
        self.y2 = int(erelease.ydata)

        self.status_label.config(
            text=f"ROI Selected: ({self.x1}, {self.y1}) → ({self.x2}, {self.y2})")

    # ======================================================
    # PROCESS VIDEO
    # ======================================================

    def process_video(self):
        if self.video_path is None:
            messagebox.showwarning("Warning", "Please load a video first")
            return

        if None in [self.x1, self.y1, self.x2, self.y2]:
            messagebox.showwarning("Warning", "Please select an ROI first")
            return

        x1, x2 = sorted([self.x1, self.x2])
        y1, y2 = sorted([self.y1, self.y2])

        cap = cv2.VideoCapture(self.video_path)

        if not cap.isOpened():
            messagebox.showerror("Error", "Could not open video")
            return

        frame_intensities = []
        time_stamps = []
        frame_count = 0

        while True:
            ret, frame = cap.read()

            if not ret:
                break

            roi_frame = frame[y1:y2, x1:x2]
            gray_roi = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2GRAY)

            brightness = np.mean(gray_roi)

            frame_intensities.append(brightness)
            time_stamps.append(frame_count)

            frame_count += 1

        cap.release()

        frame_intensities = np.array(frame_intensities)

        # ==================================================
        # RELATIVE FLUX NORMALISATION
        # ==================================================

        # baseline = np.mean(frame_intensities[:20])

        # frame_intensities /= baseline
        frame_intensities /= frame_intensities.max()


        self.frame_intensities = frame_intensities
        self.time_stamps = time_stamps

        self.plot_lightcurve()

        self.status_label.config(text=f"Processed {frame_count} frames")


    # ======================================================
    # PLOT LIGHT CURVE
    # ======================================================

    def plot_lightcurve(self):
        # self.ax.clear()
        #
        # self.ax.plot(
        #     self.time_stamps,
        #     self.frame_intensities
        # )
        #
        # self.ax.set_title("Light Curve")
        # self.ax.set_xlabel("Frame Number")
        # self.ax.set_ylabel("Relative Brightness")
        # self.ax.grid(True)
        # self.canvas.draw()


        # ==============================================
        # INTERACTIVE PLOTLY WINDOW
        # ==============================================

        fig = go.Figure(
            data=go.Scatter(
                x=self.time_stamps,
                y=self.frame_intensities,
                mode='lines'
            )
        )

        fig.update_layout(
            title='Interactive Light Curve',
            xaxis_title='Frame Number',
            yaxis_title='Relative Brightness',
            hovermode='x unified'
        )

        fig.show()

    # ======================================================
    # SAVE CSV
    # ======================================================

    def save_csv(self):
        if self.frame_intensities is None:
            messagebox.showwarning(
                "Warning",
                "Generate a light curve first")
            return

        # Default filename based on loaded video
        default_name = os.path.splitext(
            os.path.basename(self.video_path))[0]

        # Get original video filename without extension
        default_name = os.path.splitext(
            os.path.basename(self.video_path)
        )[0]

        filepath = filedialog.asksaveasfilename(
            initialfile=f"{default_name}_lightcurve.csv",
            defaultextension='.csv',
            filetypes=[('CSV Files', '*.csv')]
        )

        if not filepath:
            return

        df = pd.DataFrame({
            'Frame': self.time_stamps,
            'Relative_Brightness': self.frame_intensities})

        df.to_csv(filepath, index=False)

        messagebox.showinfo(
            "Saved",
            f"CSV saved to:\n{filepath}")

# ==========================================================
# RUN APP
# ==========================================================

root = tk.Tk()
app = LightCurveApp(root)
root.mainloop()
