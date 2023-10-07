from api import db

class Department(db.Model):
    __tablename__ = 'department'
    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(255), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'department': self.department
        }

class Job(db.Model):
    __tablename__ = 'job'
    id = db.Column(db.Integer, primary_key=True)
    job = db.Column(db.String(255), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'job': self.job
        }

class Employee(db.Model):
    __tablename__ = 'employee'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    datename = db.Column(db.String(255), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'datename': self.datename,
            'department_id': self.department_id,
            'job_id': self.job_id
        }




    