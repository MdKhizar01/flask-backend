# Use the official Python image from Docker Hub
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire app directory into the container
COPY . /app/

# Expose port 5000 for Flask app
EXPOSE 5000

# Set the environment variable for Flask app (Optional)
ENV FLASK_APP=app.py

# Run the application using gunicorn
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]
