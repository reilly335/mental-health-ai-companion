# Dockerfile

FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the application code
COPY app.py .

# Expose the port
EXPOSE 5004

# Command to run the application
CMD ["python", "app.py"]

