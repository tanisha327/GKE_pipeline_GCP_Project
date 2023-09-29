# DockerFile referenced from below source. 
# Modifications are made to meet the requirement of the assignment
# Source: https://docs.docker.com/engine/reference/builder/ 

# Use a base image with Python pre-installed
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . .


# Expose port 6000
EXPOSE 6000

# Set the command to run when the container starts
CMD ["python", "app.py"]

