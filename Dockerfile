# Use an official Python runtime as the parent image
FROM python:3.11

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set the Flask app environment variable
ENV FLASK_APP run.py

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable for Flask to run in production mode
ENV FLASK_ENV production

# Run app.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0"]
