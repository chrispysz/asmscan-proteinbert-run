# Use an official Python runtime as a parent image
FROM python:3.7-slim-bookworm

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define an environment variable
# This variable will ensure output from the python application is sent straight to the terminal without buffering it first
ENV PYTHONUNBUFFERED=0

# Run proteinbert.py when the container launches
ENTRYPOINT ["python", "-u", "process.py"]