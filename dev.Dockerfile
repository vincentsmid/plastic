# Start from a base image with both Python and necessary utilities
FROM python:3.11-bullseye

# Set the working directory in the container
WORKDIR /usr/src/app

# Install system dependencies for downloading and extracting Slic3r
RUN apt-get update && apt-get install -y wget bzip2 libc6 && rm -rf /var/lib/apt/lists/*

# Download Slic3r
RUN wget https://github.com/slic3r/Slic3r/releases/download/1.3.0/slic3r-1.3.0-linux-x64.tar.bz2 -O slic3r.tar.bz2

# Extract Slic3r
RUN tar -xjf slic3r.tar.bz2 -C /opt/ && rm slic3r.tar.bz2

# Symlink Slic3r to a bin directory in PATH
RUN ln -s /opt/Slic3r/Slic3r /usr/local/bin/slic3r

# Copy the current directory contents into the container
COPY . /usr/src/app

# Install poetry
RUN pip install poetry

# Install dependencies using poetry without dev dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev

# Assuming you still need the Caddyfile operation from your Python setup
# RUN sed -i 's|/Users/user/GreenPanda/cdn/filedir|/usr/src/app/files/Uploads|g' /etc/caddy/Caddyfile

# Assuming you want to keep the uvicorn server for your app and not run Slic3r's GUI
CMD ["sh", "-c", "bash /usr/src/app/bin/dev/migrate.sh && poetry run uvicorn main_app.main:app --host 0 --port 8000"]

# Expose the port the app runs on
EXPOSE 8000