from flask import request, jsonify
from flask_restful import Resource, Api, reqparse, inputs
from werkzeug.datastructures import FileStorage
from api import app, db
from api.models import Department, Job, Employee
import csv

api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('file', type=FileStorage, location='files')

class UploadCSV(Resource):
    def post(self):
        args = parser.parse_args()
        uploaded_file = args['file']
        if uploaded_file:
            filename = uploaded_file.filename.lower()
            uploaded_file.stream.seek(0)
            csv_data = csv.reader(uploaded_file.stream.read().decode("utf-8").splitlines())
            if "department" in filename:
                for row in csv_data:
                    department = Department(id=row[0], department=row[1])
                    db.session.add(department)
            elif "job" in filename:
                for row in csv_data:
                    job = Job(id=row[0], job=row[1])
                    db.session.add(job)
            elif "employee" in filename:
                for row in csv_data:
                    employee = Employee(id=row[0], name=row[1], datename=row[2], department_id=row[3], job_id=row[4])
                    db.session.add(employee)
            else:
                return {"message": "Invalid file name!"}, 400
            db.session.commit()
            return {"message": "Data uploaded successfully!"}, 200
        return {"message": "No file uploaded!"}, 400

class BatchInsert(Resource):
    def post(self):
        data = request.get_json()
        if not data:
            return {"message": "No data provided"}, 400
        if not isinstance(data, list) or len(data) > 1000:
            return {"message": "Data should be a list and not exceed 1000 items"}, 400
        for item in data:
            if item['type'] == 'employee':
                employee = Employee(id=item['id'], name=item['name'], datename=item['datename'], department_id=item['department_id'], job_id=item['job_id'])
                db.session.add(employee)
            elif item['type'] == 'department':
                department = Department(id=item['id'], department=item['department'])
                db.session.add(department)
            elif item['type'] == 'job':
                job = Job(id=item['id'], job=item['job'])
                db.session.add(job)
            else:
                return {"message": f"Invalid type {item['type']} found"}, 400
        db.session.commit()
        return {"message": "Data inserted successfully!"}, 200

# Add the resource to the API
api.add_resource(UploadCSV, '/upload-csv')
api.add_resource(BatchInsert, '/batch-insert')