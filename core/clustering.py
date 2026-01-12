# core/clustering.py
import cv2
import numpy as np
from sklearn.cluster import MiniBatchKMeans

def cluster_image(image, k=3, grid_step=5):
    """
    Apply MiniBatch K-means clustering to the image for faster performance.

    Args:
        image: Input image as a NumPy array.
        k: Number of clusters (colors).
        grid_step: Step size for the grid (e.g., 5x5 blocks).

    Returns:
        Clustered image as a NumPy array.
    """
    h, w, _ = image.shape

    # Crop the image to make dimensions divisible by grid_step
    new_h = h // grid_step * grid_step
    new_w = w // grid_step * grid_step
    cropped_image = image[:new_h, :new_w, :]

    # Reshape the image to a 2D array of pixels
    pixel_values = cropped_image.reshape((-1, 3))
    pixel_values = np.float32(pixel_values) / 255.0  # Normalize to [0, 1]

    # Apply MiniBatch K-means for faster clustering
    kmeans = MiniBatchKMeans(n_clusters=k, max_iter=20, batch_size=1024, n_init=3)
    labels = kmeans.fit_predict(pixel_values)

    # Replace pixel values with cluster centers
    centers = np.uint8(kmeans.cluster_centers_ * 255)
    clustered_pixels = centers[labels]

    # Reshape clustered_pixels to match the cropped image shape
    clustered_image = clustered_pixels.reshape(cropped_image.shape)

    return clustered_image, cropped_image
