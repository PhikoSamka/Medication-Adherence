# Base image for Python
FROM python:3.11-slim

# Prevent Python from buffering output
ENV PYTHONUNBUFFERED=TRUE

# Install dependencies
RUN pip install --no-cache-dir pipenv

# Set the working directory in the container
WORKDIR /app

# Copy dependency files into the container
COPY ["Pipfile", "Pipfile.lock", "./"]

# Install Python dependencies
RUN pipenv install --deploy --system && \
    rm -rf /root/.cache

# Copy Python scripts
COPY ["*.py", "./"]

# Copy the model file
COPY models/adherence_model-v1.0.bin ./models/

# Copy templates and static directories
COPY templates/ ./templates/
COPY static/ ./static/

# Expose port 9696 for Flask
EXPOSE 9696

# Use Gunicorn to serve the Flask application
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]

