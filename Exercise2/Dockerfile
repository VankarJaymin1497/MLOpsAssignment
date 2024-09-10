# Use the official Python image from DockerHub as a base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install necessary Python libraries
RUN pip install --no-cache-dir fastapi uvicorn joblib scikit-learn numpy pydantic

# Expose port 8000
EXPOSE 8000

# Define the command to run the FastAPI app using Uvicorn
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]