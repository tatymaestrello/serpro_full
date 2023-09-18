from flask import Flask

# https://flask.palletsprojects.com/en/2.3.x/quickstart/
# https://pythonbasics.org/flask-upload-file/

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
from views import *

# /// = relative path, //// = absolute path
app.config['UPLOAD_FOLDER'] = './uploaded_files/'
app.config['MAX_CONTENT_PATH'] = 1024 * 1024 * 1024

print("Init program: "+__name__)

if __name__ == "__main__":
    print("Init App")
    app.run(debug=True)
