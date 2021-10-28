from flask import Flask, render_template, request
import os, pytesseract
from flask_uploads import UploadSet, configure_uploads, IMAGES
from PIL import Image


pdir= os.path.dirname(os.path.abspath(__file__))


app = Flask(__name__, 
            static_url_path='',
            static_folder='static',
            template_folder='templates')

photos = UploadSet('photos', IMAGES)

app.config['DEBUG'] = True
app.config['UPLOAD_FOLDER'] = 'images'

class Gt(object):
    def __init__(self, file):
        self.file = pytesseract.image_to_string(Image.open(pdir+ '/images/' + file))


@app.route('/', methods = ['GET', 'POST'])
def home():
    print("aaaaaaaaa")
    if request.method == 'POST':
        name = request.form['image-name'] + '.jpg'
        print(name)
        photo = request.files['photo']
        print(type(photo))
        path = os.path.join(app.config['UPLOAD_FOLDER'], name)
        print(path)
        photo.save(path)


        tex = Gt(name)
        print('TEXT OBJECT' + tex.file)

        return tex.file

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug= True)

