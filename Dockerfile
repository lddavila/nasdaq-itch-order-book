FROM python:3.11-slim

WORKDIR /app

# Install dependencies first to leverage Docker caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy configuration structure and application logic
COPY config.yaml .
COPY main.py .

# Define execution command
CMD ["python", "main.py"]