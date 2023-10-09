# db-migration-api
A RESTful API designed to facilitate database migrations. This project provides endpoints for uploading historical data from CSV files, batch transactions, and seamless integration into a SQL database. Built with Flask, SQLAlchemy, and pandas, it aims to provide a robust solution for managing and migrating department, job, and employee data.

## API Endpoints Documentation

### Endpoints for Uploading CSVs and Viewing Data:

1. **Upload CSVs**:
   - **Endpoint**: `/upload-csv`
   - **Method**: `POST`
   - **Description**: This endpoint allows you to upload CSV files for the `department`, `job`, and `employee` tables. The system will determine which table the file belongs to based on the file's name.
   - **Parameters**: 
     - `file`: CSV file to upload.

2. **Batch Insert**:
   - **Endpoint**: `/batch-insert`
   - **Method**: `POST`
   - **Description**: Allows batch insertion of data for the `department`, `job`, and `employee` tables.
   - **Body**: List of data to insert. Each item should have a type (`type`) which can be `employee`, `department`, or `job`.

3. **View Departments Data**:
   - **Endpoint**: `/upload-csv/table-department`
   - **Method**: `GET`
   - **Description**: Displays all departments.

4. **View Jobs Data**:
   - **Endpoint**: `/upload-csv/table-job`
   - **Method**: `GET`
   - **Description**: Displays all jobs.

5. **View Employees Data**:
   - **Endpoint**: `/upload-csv/table-employee`
   - **Method**: `GET`
   - **Description**: Displays all employees.

### Endpoints for Deleting Data:

1. **Delete All Departments**:
   - **Endpoint**: `/upload-csv/table-department`
   - **Method**: `DELETE`
   - **Description**: Deletes all records from the departments table.

2. **Delete All Jobs**:
   - **Endpoint**: `/upload-csv/table-job`
   - **Method**: `DELETE`
   - **Description**: Deletes all records from the jobs table.

3. **Delete All Employees**:
   - **Endpoint**: `/upload-csv/table-employee`
   - **Method**: `DELETE`
   - **Description**: Deletes all records from the employees table.

### SQL Additional Endpoints:

1. **Hires by Quarter**:
   - **Endpoint**: `/hires-by-quarter`
   - **Method**: `GET`
   - **Description**: Displays the number of employees hired for each job and department in 2021 divided by quarter.

2. **Departments Above Average**:
   - **Endpoint**: `/departments-above-average`
   - **Method**: `GET`
   - **Description**: Lists the departments that hired more employees than the average number of employees hired in 2021 for all departments.

