import pytesseract
from PIL import Image
import cv2

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def ocr_detection(image_path):
    # Load image
    image = cv2.imread(image_path)
    # Convert image to RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # Use pytesseract to detect text
    text = pytesseract.image_to_string(image)

    return text

# Test
image_path = 'sample2.jpg'
text = ocr_detection(image_path)
print(text)
