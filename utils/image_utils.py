# utils/image_utils.py
import cv2
from PIL import Image, ImageTk

def resize_image(image, max_dimension=600):
    """Resize an image to fit within a maximum dimension for faster processing."""
    h, w = image.shape[:2]
    if h > max_dimension or w > max_dimension:
        scale = max_dimension / max(h, w)
        new_w, new_h = int(w * scale), int(h * scale)
        image = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)
    return image

def convert_to_photoimage(image):
    """Convert a NumPy image to a Tkinter PhotoImage with efficient resizing."""
    image_pil = Image.fromarray(image)
    image_pil.thumbnail((400, 400))
    image_tk = ImageTk.PhotoImage(image_pil)
    return image_tk
