from flask import Flask, jsonify, request
import numpy as np
import pytesseract
import re
from fileinput import filename
import base64
# from io import StringIO

app = Flask(__name__)

path = r"C:\Users\suchita.berde\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
pytesseract.pytesseract.tesseract_cmd = path

@app.route("/extract_pandata_base64", methods = ["POST"])
def extract_pandata():
    data = request.get_json()
    # file_name = data["filename"]
    # f = request.files["file_name"]
    # print(f)
    # f.save(f.filename)
    image_string = data["base64"]
    img_string = image_string.split('base64,')[-1].strip()
    print(img_string)
    decoded_data = base64.b64decode((img_string))
    print(decoded_data)
    img_file = open("image.jpeg","wb")
    img_file.write(decoded_data)
    img_file.close()


    pan_data = pytesseract.image_to_string("image.jpeg")
    print(pan_data)

    dob = re.findall("\d{2}[/]\d{2}[/]\d{4}", pan_data)
    print(dob)

    pan_num = re.findall("[A-Z]{5}\d{4}[A-Z]",pan_data)
    print(pan_num)

    return jsonify({"DOB" : dob[0], "Pan Number":pan_num[0]})
    

    # return jsonify({"Predicted Sepal length" : prediction})


if __name__ == "__main__":
    app.run(debug = True)