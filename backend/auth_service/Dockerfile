# Dockerfile

FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the application code
COPY app.py .

# Expose the port
EXPOSE 5000

# Set environment variables
ENV JWT_SECRET_KEY='your-very-secure-secret-key'

# Run the application
CMD ["python", "app.py"]

