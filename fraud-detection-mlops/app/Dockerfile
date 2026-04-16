# 1. Use the version that matches the training environment
FROM python:3.13-slim

# 2. Install tiny system tools needed for ML library compilation
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 3. Set the working directory
WORKDIR /app

# 4. Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy your application code
COPY . .

# 6. Start the API
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]