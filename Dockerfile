# Use an official Python runtime as the base image
FROM python:3.10-slim-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install VIPS dependencies and libvips
RUN apt-get update && apt-get install -y \
    build-essential \
    libvips \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the project code into the container
COPY . .
# Set the environment variable for Django
ENV DJANGO_SETTINGS_MODULE=wsu_viewer.settings

# Expose the port the app runs on
EXPOSE 8000

#CMD ["gunicorn", "tif_project.wsgi:application", "--bind", "0.0.0.0:8000"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]