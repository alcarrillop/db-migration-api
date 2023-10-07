from flask import request, jsonify
from flask_restful import Resource, Api, reqparse
from sqlalchemy import text
from werkzeug.datastructures import FileStorage
from api import app, db
from api.models import Department, Job, Employee
import csv

api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('file', type=FileStorage, location='files')

@app.route('/upload-csv/table-department', methods=['GET'])
def get_departments():
    departments = Department.query.all()  # Fetch all departments
    return jsonify([dept.serialize() for dept in departments])

@app.route('/upload-csv/table-job', methods=['GET'])
def get_jobs():
    jobs = Job.query.all()  # Fetch all jobs
    return jsonify([job.serialize() for job in jobs])

@app.route('/upload-csv/table-employee', methods=['GET'])
def get_employees():
    employees = Employee.query.all()  # Fetch all employees
    return jsonify([emp.serialize() for emp in employees])

@app.route('/hires-by-quarter', methods=['GET'])
def hires_by_quarter():
    try:
        sql = text("""
            SELECT 
                department,
                job,
                SUM(CASE WHEN strftime('%m', datename) IN ('01', '02', '03') THEN 1 ELSE 0 END) AS Q1,
                SUM(CASE WHEN strftime('%m', datename) IN ('04', '05', '06') THEN 1 ELSE 0 END) AS Q2,
                SUM(CASE WHEN strftime('%m', datename) IN ('07', '08', '09') THEN 1 ELSE 0 END) AS Q3,
                SUM(CASE WHEN strftime('%m', datename) IN ('10', '11', '12') THEN 1 ELSE 0 END) AS Q4
            FROM 
                employee 
            JOIN 
                department ON department.id = employee.department_id
            JOIN 
                job ON job.id = employee.job_id
            WHERE 
                strftime('%Y', datename) = '2021'
            GROUP BY 
                department, job
            ORDER BY 
                department, job;
        """)

        result = db.session.execute(sql)
        hires = [{"department": row[0], "job": row[1], "Q1": row[2], "Q2": row[3], "Q3": row[4], "Q4": row[5]} for row in result]

        return jsonify(hires)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/departments-above-average', methods=['GET'])
def departments_above_average():
    try:
        sql = text("""
            WITH DepartmentHires AS (
                SELECT 
                    department.id AS department_id,
                    department.department AS department_name,
                    COUNT(employee.id) AS hires
                FROM 
                    department
                LEFT JOIN 
                    employee ON department.id = employee.department_id
                WHERE 
                    strftime('%Y', employee.datename) = '2021'
                GROUP BY 
                    department.id
            ),
            MeanHires AS (
                SELECT 
                    AVG(hires) AS average_hires
                FROM 
                    DepartmentHires
            )
            SELECT 
                department_id,
                department_name,
                hires
            FROM 
                DepartmentHires
            WHERE 
                hires > (SELECT average_hires FROM MeanHires)
            ORDER BY 
                hires DESC;
        """)

        result = db.session.execute(sql)
        departments = [{"id": row[0], "department": row[1], "hired": row[2]} for row in result]

        return jsonify(departments)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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