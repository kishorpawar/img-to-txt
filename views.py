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
    UserName = ''
    LicenseCode = ''
    
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

def use_google_vision(content):
    print(content.filename)
    """Detects document features in an image."""
    from google.cloud import vision
    import io, os
    from google.oauth2 import service_account
    import json
    credentials_raw = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    print("CREDs ")
    print(credentials_raw)
    service_account_info = json.loads(credentials_raw)
     
    credentials = service_account.Credentials.from_service_account_info(
    service_account_info)
    client = vision.ImageAnnotatorClient(credentials=credentials)

    with io.open('static/media/{}'.format(content.filename), 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.document_text_detection(image=image)

    items = []
    lines = {}

    for text in response.text_annotations[1:]:
        top_x_axis = text.bounding_poly.vertices[0].x
        top_y_axis = text.bounding_poly.vertices[0].y
        bottom_y_axis = text.bounding_poly.vertices[3].y
    
        if top_y_axis not in lines:
            lines[top_y_axis] = [(top_y_axis, bottom_y_axis), []]
    
        for s_top_y_axis, s_item in lines.items():
            if top_y_axis < s_item[0][1]:
                lines[s_top_y_axis][1].append((top_x_axis, text.description))
                break
    
    for _, item in lines.items():
        if item[1]:
            words = sorted(item[1], key=lambda t: t[0])
            items.append((item[0], ' '.join([word for _, word in words]), words))
        
    print(items)
    return " ".join([stri for _, stri, word in items])

#    for page in response.full_text_annotation.pages:
#        for block in page.blocks:
#            #print('\nBlock confidence: {}\n'.format(block))
#
#            for paragraph in block.paragraphs:
#            #    print('Paragraph confidence: {}'.format(
#            #        paragraph))
#
#                for word in paragraph.words:
#                    word_text = ''.join([
#                        symbol.text for symbol in word.symbols
#                    ])
#                    print('Word text: {} (confidence: {})'.format(
#                        word_text, word.confidence))
#
#                   # for symbol in word.symbols:
#                   #     print('\tSymbol: {} (confidence: {})'.format(
#                   #         symbol.text, symbol.confidence))
#
    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
