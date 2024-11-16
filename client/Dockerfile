# Use the official Python image as the base image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy requirements.txt to the working directory
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files to the working directory
COPY . .


# Command to run the application (adjust as needed)
CMD ["python3", "main.py"]
