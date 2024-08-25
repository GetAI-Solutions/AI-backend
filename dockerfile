# Use the official Python 3.10 image from Docker Hub as the base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /getai-app

# Copy the current directory contents into the container at /app
COPY . .

# Install any dependencies from requirements.txt if it exists
# (Make sure to have a requirements.txt file in your project if you want to install dependencies)
RUN pip install -r requirements.txt

# Set the default command to run when starting the container
CMD ["uvicorn", "--host", "0.0.0.0", "--port", "4600" ,"--reload", "main:app"]

