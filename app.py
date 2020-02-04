import os
from flask import Flask, render_template, request
from views import get_attendence, get_text_from_api, use_google_vision

MEDIA = 'static/media/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = MEDIA

# check the file extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# route and function to handle the upload page
@app.route('/', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        # check if there is a file in the request
        if 'file' not in request.files:
            return render_template('upload.html', msg='No file selected')
        file = request.files['file']
        # if no file is selected
        if file.filename == '':
            return render_template('upload.html', msg='No file selected')

        if file and allowed_file(file.filename):
            file.save(MEDIA+file.filename)

            # call the OCR function on it
            #extracted_text = get_attendence(file)
            #extracted_text = get_text_from_api(file)
            extracted_text = use_google_vision(file)

            # extract the text and display it
            return render_template('upload.html',
                                   msg='Successfully processed',
                                   extracted_text=extracted_text,
                                   img_src=MEDIA + file.filename)
    elif request.method == 'GET':
        return render_template('upload.html')

#@app.route('/')
#def home_page():
#    return render_template('index.html') 

if __name__ == '__main__':
    app.run()
