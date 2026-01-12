# gui/app.py
import customtkinter as ctk
from tkinter import filedialog
import threading
import cv2
from PIL import Image, ImageTk
from core.clustering import cluster_image
from utils.image_utils import resize_image, convert_to_photoimage

class FrescoClusterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fresco Cluster")
        self.root.geometry("1000x700")

        # Set a fancy dark theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Variables to store images
        self.original_image = None
        self.cropped_image = None
        self.clustered_image = None
        self.blended_image = None

        # Clustering parameters
        self.k = ctk.IntVar(value=3)
        self.grid_step = ctk.IntVar(value=5)

        # Create the GUI
        self.create_widgets()

    def create_widgets(self):
        """Create all GUI widgets with a fancy design."""

        # Frame for uploading images
        upload_frame = ctk.CTkFrame(self.root, corner_radius=10)
        upload_frame.pack(fill="x", padx=20, pady=10)

        self.upload_button = ctk.CTkButton(upload_frame, text="Upload Image", command=self.upload_image_thread,
                                           fg_color="#1f6aa5", hover_color="#144870")
        self.upload_button.pack(pady=10)

        # Frame for clustering parameters
        params_frame = ctk.CTkFrame(self.root, corner_radius=10)
        params_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(params_frame, text="Number of Clusters (K):", font=("Helvetica", 12)).grid(row=0, column=0, sticky="w", pady=5, padx=10)
        k_slider = ctk.CTkSlider(params_frame, from_=2, to=10, variable=self.k, command=self.update_cluster)
        k_slider.grid(row=0, column=1, sticky="ew", pady=5, padx=10)

        ctk.CTkLabel(params_frame, text="Grid Step:", font=("Helvetica", 12)).grid(row=1, column=0, sticky="w", pady=5, padx=10)
        grid_slider = ctk.CTkSlider(params_frame, from_=1, to=20, variable=self.grid_step, command=self.update_cluster)
        grid_slider.grid(row=1, column=1, sticky="ew", pady=5, padx=10)

        # Button to apply clustering
        self.cluster_button = ctk.CTkButton(params_frame, text="Apply Clustering", command=self.apply_clustering_thread,
                                             fg_color="#1f6aa5", hover_color="#144870", state="disabled")
        self.cluster_button.grid(row=2, column=0, columnspan=2, pady=15)

        # Frame for displaying images
        image_frame = ctk.CTkFrame(self.root, corner_radius=10)
        image_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Labels for images
        self.original_label = ctk.CTkLabel(image_frame, text="", corner_radius=10)
        self.original_label.pack(side="left", padx=10, pady=10, fill="both", expand=True)

        self.clustered_label = ctk.CTkLabel(image_frame, text="", corner_radius=10)
        self.clustered_label.pack(side="right", padx=10, pady=10, fill="both", expand=True)

        # Frame for opacity slider
        opacity_frame = ctk.CTkFrame(self.root, corner_radius=10)
        opacity_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(opacity_frame, text="Opacity:", font=("Helvetica", 12)).pack(side="left", padx=(0, 10))
        self.opacity_slider = ctk.CTkSlider(opacity_frame, from_=0, to=100, command=self.update_opacity)
        self.opacity_slider.pack(side="left", fill="x", expand=True, padx=5)
        self.opacity_slider.set(50)  # Default opacity

        # Button to save the clustered image
        self.save_button = ctk.CTkButton(self.root, text="Save Clustered Image", command=self.save_image,
                                          fg_color="#1f6aa5", hover_color="#144870", state="disabled")
        self.save_button.pack(pady=20)

    def upload_image_thread(self):
        """Upload an image from a file in a separate thread."""
        threading.Thread(target=self.upload_image, daemon=True).start()

    def upload_image(self):
        """Upload an image from a file."""
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        if file_path:
            self.original_image = cv2.imread(file_path)
            self.original_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)
            self.original_image = resize_image(self.original_image, max_dimension=600)

            image_tk = convert_to_photoimage(self.original_image)
            self.original_label.configure(image=image_tk)
            self.original_label.image = image_tk
            self.cluster_button.configure(state="normal")

    def apply_clustering_thread(self):
        """Apply clustering in a separate thread."""
        self.cluster_button.configure(state="disabled")
        threading.Thread(target=self.apply_clustering, daemon=True).start()

    def apply_clustering(self):
        """Apply K-means clustering to the image."""
        if self.original_image is None:
            self.cluster_button.configure(state="normal")
            return

        k = self.k.get()
        grid_step = self.grid_step.get()

        self.clustered_image, self.cropped_image = cluster_image(self.original_image, k, grid_step)

        image_tk = convert_to_photoimage(self.clustered_image)
        self.clustered_label.configure(image=image_tk)
        self.clustered_label.image = image_tk

        self.update_opacity()
        self.save_button.configure(state="normal")
        self.cluster_button.configure(state="normal")

    def update_opacity(self, event=None):
        """Update the blended image based on opacity."""
        if self.cropped_image is None or self.clustered_image is None:
            return

        opacity = self.opacity_slider.get() / 100
        cropped_resized = cv2.resize(self.cropped_image, (self.clustered_image.shape[1], self.clustered_image.shape[0]))
        blended = cv2.addWeighted(cropped_resized, 1 - opacity, self.clustered_image, opacity, 0)

        image_tk = convert_to_photoimage(blended)
        self.clustered_label.configure(image=image_tk)
        self.clustered_label.image = image_tk

    def update_cluster(self, event=None):
        """Update clustering when parameters change."""
        self.apply_clustering_thread()

    def save_image(self):
        """Save the clustered image to a file."""
        if self.clustered_image is None:
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            cv2.imwrite(file_path, cv2.cvtColor(self.clustered_image, cv2.COLOR_RGB2BGR))
            print(f"Clustered image saved to {file_path}")
