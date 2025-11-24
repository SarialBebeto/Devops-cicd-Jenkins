# syntax=docker/dockerfile:1.7

# Use official slim Python image
FROM python:3.11.1-slim AS base

# Set working directory
WORKDIR /app

# Prevent Python from writing .pyc files & ensure unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies in a single layer
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage caching
COPY requirements.txt .

# ---------- Install Python dependencies with BuildKit cache ----------
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ---------- Copy project source ----------
COPY . .

# ---------- Command ----------
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
