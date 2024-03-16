import cv2
import pytesseract
import numpy as np
from PIL import Image

# Function to check image resolution (a minimum width and height)
def check_image_resolution(image, min_width=300, min_height=200):
    width, height = image.size
    return width >= min_width and height >= min_height

# Function to check image quality using blur detection(using a threshold value)
def check_image_blur(image, threshold=100):
    np_image = np.array(image)
    gray_image = cv2.cvtColor(np_image, cv2.COLOR_BGR2GRAY)
    laplacian = cv2.Laplacian(gray_image, cv2.CV_64F).var()
    return laplacian > threshold

# Function to check image quality (returns the status and message)
def check_image_quality(image):
    image = Image.open(image)
    if not check_image_resolution(image):
        return False, 'Image resolution is too low'
    if not check_image_blur(image):
        return False, 'Image is too blurry'
    return True, ''

# Function to preprocess the image (converts the input image to grayscale)
def preprocess_image(image):
    np_image = np.array(Image.open(image))
    gray_image = cv2.cvtColor(np_image, cv2.COLOR_BGR2GRAY)
    # Apply a Gaussian blur to the image to reduce noise
    blurred_image = cv2.GaussianBlur(gray_image, (3, 3), 0)
    # Use the OTSU thresholding method to binarize the image
    _, thresh_image = cv2.threshold(blurred_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh_image

# Function to perform OCR (returns the extracted text)
def perform_ocr(image):
    # Configure pytesseract with custom settings for better text extraction
    custom_config = '--oem 3 --psm 12'
    text = pytesseract.image_to_string(image, config=custom_config)
    return text

# Main function to process the image
def process_image(image):
    quality_status, message = check_image_quality(image)
    if not quality_status:
        return {'status': 'error', 'message': message}

    preprocessed_image = preprocess_image(image)
    text = perform_ocr(preprocessed_image)
    return {'status': 'success', 'text': text}

# Convert text to a dictionary
def text_to_dict(text):
    lines = text.strip().split("\n")
    data = {}

    for line in lines:
        if line.strip():
            key, value = line.split(":", 1)  # Split by the first colon
            data[key.strip().lower()] = value.strip()

    return data
