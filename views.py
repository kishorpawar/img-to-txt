try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
from pprint import pprint

def get_attendence(filename):
    """
    This function will handle the core OCR processing of images.
    """
    text = pytesseract.image_to_string(Image.open(filename))  # We'll use Pillow's Image class to open the image and pytesseract to detect the string in the image
    pprint(text)    
    return text

#print(ocr_core('images/ocr_example_1.png'))
