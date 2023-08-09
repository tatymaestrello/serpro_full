from flask import Flask

# https://flask.palletsprojects.com/en/2.3.x/quickstart/
# https://pythonbasics.org/flask-upload-file/

app = Flask(__name__)

# /// = relative path, //// = absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['UPLOAD_FOLDER'] = './uploaded_files/'
app.config['UPLOAD_EXTENSIONS'] = ['.csv']
app.config['MAX_CONTENT_PATH'] = 1024 * 1024 * 1024

from views import *
#from manage import manager

print("Init program: "+__name__)



def init_db():
    #from models import db
    db.engine.echo = True
    db.metadata.bind = db.engine
    db.metadata.create_all(checkfirst=True)
    db.create_all(checkfirst=True)

if __name__ == "__main__":
    #db.create_all()
    print("Init App")
    #manager.run(app)
    init_db()
    app.run(debug=True)
