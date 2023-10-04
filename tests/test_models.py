import pytest
from api import app, db
from api.models import Department, Job, Employee

# Setup and Teardown
@pytest.fixture(scope='module')
def test_client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # Use a separate test database
    with app.test_client() as testing_client:
        with app.app_context():
            db.create_all()
            yield testing_client
            db.drop_all()

def test_department_creation(test_client):
    with app.app_context():
        department = Department(id=1, department="Test Department")
        db.session.add(department)
        db.session.commit()
        retrieved_department = Department.query.get(1)
        assert retrieved_department is not None
        assert retrieved_department.department == "Test Department"

def test_job_creation(test_client):
    with app.app_context():
        job = Job(id=1, job="Test Job")
        db.session.add(job)
        db.session.commit()
        retrieved_job = Job.query.get(1)
        assert retrieved_job is not None
        assert retrieved_job.job == "Test Job"

def test_employee_creation(test_client):
    with app.app_context():
        employee = Employee(id=1, name="Test Employee", datename="2021-01-01", department_id=1, job_id=1)
        db.session.add(employee)
        db.session.commit()
        retrieved_employee = Employee.query.get(1)
        assert retrieved_employee is not None
        assert retrieved_employee.name == "Test Employee"
