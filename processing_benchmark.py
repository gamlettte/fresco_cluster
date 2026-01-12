import time
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
    start_time = time.time()  # Start time measurement

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
    clustered_pixels = centers[labels.flatten()]

    # Reshape clustered_pixels to match the cropped image shape
    clustered_image = clustered_pixels.reshape(cropped_image.shape)

    end_time = time.time()  # End time measurement
    execution_time = end_time - start_time
    print(f"Clustering execution time: {execution_time:.4f} seconds")

    return clustered_image, cropped_image, execution_time

def benchmark_clustering(image_paths, k_values, grid_steps, iterations=10):
    """
    Benchmark clustering performance on different images and parameters.

    Args:
        image_paths: List of paths to test images.
        k_values: List of K values to test.
        grid_steps: List of grid step values to test.
        iterations: Number of iterations for each configuration.
    """
    results = []

    for image_path in image_paths:
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        for k in k_values:
            for grid_step in grid_steps:
                total_time = 0

                for _ in range(iterations):
                    _, _, execution_time = cluster_image(image, k, grid_step)
                    total_time += execution_time

                avg_time = total_time / iterations
                results.append({
                    'image_path': image_path,
                    'k': k,
                    'grid_step': grid_step,
                    'avg_execution_time': avg_time
                })

    return results

# Example usage
if __name__ == "__main__":
    # Define test parameters
    image_paths = ['test_images/small_image.jpg', 'test_images/medium_image.jpg', 'test_images/large_image.jpg']
    k_values = [3, 5, 8]
    grid_steps = [5, 10, 15]

    # Run benchmark
    results = benchmark_clustering(image_paths, k_values, grid_steps)

    # Print results
    print("\nBenchmark Results:")
    print("Image Path\t\tK\tGrid Step\tAvg Execution Time (s)")
    print("-" * 80)
    for result in results:
        print(f"{result['image_path']}\t{result['k']}\t{result['grid_step']}\t\t{result['avg_execution_time']:.4f}")
