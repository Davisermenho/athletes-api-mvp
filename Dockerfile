FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install system deps (kept minimal). Add build-essential if you compile wheels.
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt requirements-dev.txt /app/
RUN python -m pip install --upgrade pip setuptools wheel && \
    python -m pip install --no-cache-dir -r /app/requirements.txt -r /app/requirements-dev.txt

# Copy project
COPY . /app

# Default: run tests
CMD ["python", "-m", "pytest", "-q"]
