# Use an official Python runtime as a base image
FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    unixodbc \
    unixodbc-dev \
    curl \
    apt-transport-https \
    gnupg \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 for the Flask app
EXPOSE 5000

# Environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development

# Enable Datadog tracing for the application
# ENV DD_SERVICE=food-outlet-api-docker
# ENV DD_ENV=development
# ENV DD_VERSION=1.0.0
# ENV DD_TRACE_ENABLED=true
# ENV DD_LOGS_INJECTION=true

# Run the Flask application with ddtrace
CMD ["ddtrace-run", "flask", "run"]