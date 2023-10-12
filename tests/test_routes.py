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

def test_departments_above_average(test_client):
    response = test_client.get('/departments-above-average')
    assert response.status_code == 200

def test_upload_csv(test_client):
    data = {
        'file': (open('data/departments.csv', 'rb'), 'departments.csv')
    }
    response = test_client.post('/upload-csv', content_type='multipart/form-data', data=data)
    assert response.status_code == 200

def test_batch_insert(test_client):
    # Abre el archivo de prueba
    with open('data/batch.json', 'rb') as data_file:
        # Envía el archivo en la solicitud
        response = test_client.post('/batch-insert', data={'file': data_file}, content_type='multipart/form-data')
    
    assert response.status_code == 200

