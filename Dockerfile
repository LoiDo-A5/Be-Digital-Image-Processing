FROM python:3.11
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies for OpenCV
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libgomp1 \
    libglib2.0-0 \
    ffmpeg \
    libfontconfig1 \
    libgstreamer1.0-0 \
    libjpeg62-turbo \
    libpng16-16 \
    libtiff6 \
    libopenblas0 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install --upgrade poetry
RUN pip install psycopg2-binary

WORKDIR /app

COPY pyproject.toml ./
COPY poetry.lock ./

RUN poetry install --no-root --only main
