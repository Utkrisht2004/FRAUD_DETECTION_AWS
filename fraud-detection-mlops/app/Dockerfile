# Use a lightweight Python base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the actual application code into the container
COPY . .

# Expose the port FastAPI will run on
EXPOSE 8000

# The command to start the web server when the container launches
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]