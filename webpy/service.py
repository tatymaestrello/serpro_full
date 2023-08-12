import os
from app import app
from werkzeug.utils import secure_filename

# def getFile(register_id):
#     register = Register.query.filter_by(id=register_id).first()
#     workload = Workload.query.filter_by(id=register.workload).first()
#     payload = workload.payload
#     file_path = os.path.join(app.config['UPLOAD_FOLDER'], workload.filename)
#     with open(file_path, "wb") as output_file:
#         output_file.write(payload)
#     return payload, workload

# def convertFileToDatabase(uploaded_file):
#     # Convert digital data to binary format
    
#     file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(uploaded_file.filename))

#     print(file_path)
#     uploaded_file.save(file_path)

#     with open(file_path, 'rb') as file:
#         blobData = file.read()
#     stmt = (
#         insert(Workload)
#         .values(filename=uploaded_file.filename, payload=blobData, mimetype=uploaded_file.mimetype)
#         .returning(Workload.id)
#     )
#     id=db.session.execute(stmt).scalar_one()
#     return id

# def execute_job(id):
#     print('executing job for id ' + str(id))
#     register = Register.query.filter_by(id=id).first()
#     print(register)
#     if(register.workload != None):
#         register.error='File not found'
#         db.session.commit()
#         return
#     workload = Workload.query.filter_by(id=register.worload).first()
#     error=execute_workload(workload)
#     register.error=error
#     register.complete = True
#     db.session.commit()

def execute_workload(workload):
    print(workload)
    from API.api_SERPRO import process_client 
    process_client(workload)
    