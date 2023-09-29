
# DockerFile referenced from below source. 
# Modifications are made to meet the requirement of the assignment
# Source: https://docs.docker.com/engine/reference/builder/ 

# Use a Python base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Set the entry point command to run the application
CMD ["python", "app.py"]

