# tests/test_routes.py
import pytest
import json
from api import app, db

@pytest.fixture(scope='module')
def test_client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # Use a separate test database
    with app.test_client() as testing_client:
        with app.app_context():
            db.create_all()
        yield testing_client
        db.drop_all()

def test_hires_by_quarter(test_client):
    response = test_client.get('/hires-by-quarter')
    assert response.status_code == 200
    # Add more assertions based on expected data

def test_departments_above_average(test_client):
    response = test_client.get('/departments-above-average')
    assert response.status_code == 200
    # Add more assertions based on expected data

def test_upload_csv(test_client):
    data = {
        'file': (open('data/departments.csv', 'rb'), 'departments.csv')
    }
    response = test_client.post('/upload-csv', content_type='multipart/form-data', data=data)
    assert response.status_code == 200
    # Add more assertions based on expected data

def test_batch_insert(test_client):
    data = [
        {
            "type": "employee",
            "id": 1,
            "name": "Test Employee",
            "datename": "2021-01-01",
            "department_id": 1,
            "job_id": 1
        }
    ]
    response = test_client.post('/batch-insert', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    # Add more assertions based on expected data
