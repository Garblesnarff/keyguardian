# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# The requirements will be installed manually

# Copy the application's code into the container
COPY app.py .
COPY auth_routes.py .
COPY category_routes.py .
COPY extensions.py .
COPY forms.py .
COPY models.py .
COPY utils.py .
COPY wallet_routes.py .
COPY api_models.py .
COPY templates/ ./templates/
COPY static/ ./static/

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=app.py

# Run app.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0"]
