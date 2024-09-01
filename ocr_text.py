import pytesseract
from PIL import Image
import numpy as np
import io

pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

def ocr_detection(pil_image):
    # Convert PIL image to RGB (necessary for pytesseract)
    image = pil_image.convert("RGB")
    
    # Convert PIL image to a NumPy array
    image_np = np.array(image)

    text = pytesseract.image_to_string(image)

    return text

# Test
if __name__ == "__main__":
#    image_path = 'sample2.jpg'
#    text = ocr_detection(image_path)
#    print(text)
    pass
