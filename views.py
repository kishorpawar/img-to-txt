import json, shutil, requests

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


def get_text_from_api(filename):
    """
       This function will call the onlineocr api to get the string

       [language]     - Specifies the recognition language.
	   		This parameter can contain several language names separated with commas.
                        For example "language=english,german,spanish".
			Optional parameter. By default:english

	[pagerange]    - Enter page numbers and/or page ranges separated by commas.
			For example "pagerange=1,3,5-12" or "pagerange=allpages".
                        Optional parameter. By default:allpages

        [tobw]	      - Convert image to black and white (recommend for color image and photo).
			For example "tobw=false"
                        Optional parameter. By default:false

        [zone]         - Specifies the region on the image for zonal OCR.
			The coordinates in pixels relative to the left top corner in the following format: top:left:height:width.
			This parameter can contain several zones separated with commas.
		        For example "zone=0:0:100:100,50:50:50:50"
                        Optional parameter.

        [outputformat] - Specifies the output file format.
                        Can be specified up to two output formats, separated with commas.
			For example "outputformat=pdf,txt"
                        Optional parameter. By default:doc

        [gettext]	- Specifies that extracted text will be returned.
			For example "tobw=true"
                        Optional parameter. By default:false

        [description]  - Specifies your task description. Will be returned in response.
                        Optional parameter.


	!!!!  For getting result you must specify "gettext" or "outputformat" !!!!
    """
    UserName = 'ANDYSTORRISH'
    LicenseCode = '7F48FF17-6E19-40B6-82CC-127021E3A0E7'
    
    # Extract text with English language by default
    RequestUrl = "http://www.ocrwebservice.com/restservices/processDocument?gettext=true&tobw=true";
#    with open(filename, 'rb') as image_file:
#        image_data = image_file.read()

    #r = requests.post(RequestUrl, data=image_data, auth=(UserName, LicenseCode))
    r = requests.post(RequestUrl, data=filename, auth=(UserName, LicenseCode))
    if r.status_code == 401:
        #Please provide valid username and license code
        print("Unauthorized request")
        return ("Unauthorized request")

    # Decode Output response
    jobj = json.loads(r.content)
    
    ocrError = str(jobj["ErrorMessage"])
    
    if ocrError != '':
        #Error occurs during recognition
        print ("Recognition Error: " + ocrError)
        return ("Recognition Error: ", ocrError)

    # Extracted text from first or single page
    print("Extracted Text:" + str(jobj["OCRText"][0][0]))
    return ("Extracted Text:" + str(jobj["OCRText"][0][0]))

