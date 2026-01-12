import time
import cv2
import tracemalloc

def benchmark_image_loading(image_paths):
    results = []

    for image_path in image_paths:
        tracemalloc.start()
        start_time = time.time()

        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        resized_image = resize_image(image, max_dimension=800)

        end_time = time.time()
        loading_time = end_time - start_time

        snapshot = tracemalloc.take_snapshot()
        top_stats = snapshot.statistics('lineno')
        total_memory = sum(stat.size for stat in top_stats)
        tracemalloc.stop()

        results.append({
            'image_path': image_path,
            'loading_time': loading_time,
            'memory_usage_kb': total_memory / 1024
        })

    return results

def resize_image(image, max_dimension=800):
    h, w = image.shape[:2]
    if h > max_dimension or w > max_dimension:
        scale = max_dimension / max(h, w)
        new_w, new_h = int(w * scale), int(h * scale)
        image = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)
    return image

image_paths = ['test_images/small_image.jpg', 'test_images/medium_image.jpg', 'test_images/large_image.jpg']
results = benchmark_image_loading(image_paths)

for result in results:
    print(f"Image: {result['image_path']}")
    print(f"Loading time: {result['loading_time']:.4f} seconds")
    print(f"Memory usage: {result['memory_usage_kb']:.4f} KB")
    print("---")
