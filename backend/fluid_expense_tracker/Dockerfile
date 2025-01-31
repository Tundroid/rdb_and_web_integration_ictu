# Base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install required system dependencies
RUN apt update && apt install -y pkg-config && apt install -y \
    default-libmysqlclient-dev gcc && \
    rm -rf /var/lib/apt/lists/*

# RUN apt install -y python3-dev default-libmysqlclient-dev build-essential

# Copy requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . /app

# Expose port for the Flask app
EXPOSE 5000

# Run the app using Gunicorn
# CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:5000", "api.v1.app:app"]

# Run the app using Gunicorn with debugging enabled
CMD ["gunicorn", "--capture-output", "--log-level", "debug", "--workers", "4", "--bind", "0.0.0.0:5000", "api.v1.app:app"]
