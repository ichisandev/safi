# Use the official Python base image with Python 3.10
FROM python:3.10-slim

# # Install firefox
# RUN apt-get update                             \
#  && apt-get install -y --no-install-recommends \
#     ca-certificates curl firefox-esr           \
#  && rm -fr /var/lib/apt/lists/*                \
#  && curl -L https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz | tar xz -C /usr/local/bin 

WORKDIR /app

# Install the Python dependencies
COPY setup.py ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir . 

# Copy the required files
COPY main.py .env ./
COPY servicess ./servicess
COPY routers ./routers
COPY utils ./utils

# Run the main.py script
CMD ["python3", "main.py"]
