from flask import Flask, render_template, request
import os, pytesseract
from flask_uploads import UploadSet, configure_uploads, IMAGES
from PIL import Image
import cv2
from pyzbar.pyzbar import decode
from pdf2image import convert_from_path
import json
from flask_cors import CORS

pdir= os.path.dirname(os.path.abspath(__file__))


app = Flask(__name__, 
            static_url_path='',
            static_folder='static',
            template_folder='templates')

CORS(app)

photos = UploadSet('photos', IMAGES)

app.config['DEBUG'] = True
app.config['UPLOAD_FOLDER'] = 'images'

class Gt(object):
    def __init__(self, file):
        
        self.file = pytesseract.image_to_string(Image.open(pdir+ '/images/' + file))



class Gqr(object):
    def __init__(self, file) -> None:
        f = cv2.imread(pdir+ '/images/' + file)
        print(f.shape)
        self.file = f[500:900, 200:600]
        cv2.imwrite(pdir+ '/pdfs/' + file,self.file)
        self.file = decode(self.file)

def to_l(s):
    nom_prenom = s[s.index('Prénom:') + 8: s.index('Carte') - 1]
    print("=======nomprenom==========")
    print(nom_prenom)
    cin = s[s.index('nationale:')+11:s.index('Type')-1]
    return nom_prenom, cin

def compare(text, qrli):
    np, cin = to_l(text) 
    print("******************alo")
    ch = json.loads(qrli[0].data.decode('utf-8'))
    nm = ch['firstName']
    pr = ch['lastName']
    qrcin = ch['idNumber']
    
    

    #qrl = dict(qrli)

    qrnp = nm + ' ' + pr 
    #qrcin = qrl['idNumber']

    return np == qrnp and cin == qrcin
    




@app.route('/', methods = ['GET', 'POST'])
@cross_origin()
def home():
    print("aaaaaaaaa")
    if request.method == 'POST':
        name = request.form['image-name'] + '.jpg'
        path = os.path.join(app.config['UPLOAD_FOLDER'], name)
        photo = request.files['photo']
        


        photo.save(path)

        
        
        
        
        


        tex = Gt(name)
        print("=======================================")
        print('TEXT OBJECT' + tex.file)
        
        print("=======================================")    


        qr = Gqr(name)

        print('============================')
        print('QR OBJECT')
        print('==========================')
        print(qr.file)
        print(type(tex.file))
        print(type(qr.file))
        if compare(tex.file, qr.file):
            return "legit"
        else:
            return "omou kahba"
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug= True)

