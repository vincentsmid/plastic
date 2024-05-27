FROM python:3.11-bullseye

WORKDIR /usr/src/app

# Install system dependencies for downloading and extracting PrusaSlicer
# Note: PrusaSlicer requires GTK3 for its GUI components, even though we are not using the GUI in this case, it's still better to have it installed. 
RUN apt-get update && apt-get install -y wget bzip2 libc6 libgtk-3-0  libgl1 mesa-utils && rm -rf /var/lib/apt/lists/*

# Download PrusaSlicer - make sure to include correct architecture (my dev is arm64)
RUN wget https://github.com/prusa3d/PrusaSlicer/releases/download/version_2.7.2/PrusaSlicer-2.7.2+linux-arm64-GTK3-202402291318.tar.bz2 -O prusaslicer.tar.bz2

# Extract PrusaSlicer
RUN tar -xjf prusaslicer.tar.bz2 -C /opt/ && rm prusaslicer.tar.bz2

# PrusaSlicer doesn't have a single executable like Slic3r, it's a bundle with various components.
# Therefore, you need to adjust the path according to where the PrusaSlicer binary is located within the extracted folder.
# Assuming PrusaSlicer-2.7.2+linux-arm64-GTK3 directory structure is used:
RUN ln -s /opt/PrusaSlicer-2.7.2+linux-arm64-GTK3-202402291318/prusa-slicer /usr/local/bin/prusaslicer

COPY . /usr/src/app

# Install poetry
RUN pip install poetry

# Install dependencies using poetry without dev dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev

CMD ["sh", "-c", "bash /usr/src/app/bin/dev/migrate.sh && poetry run uvicorn main_app.main:app --reload --host 0 --port 8000"]

# Expose the port the app runs on
EXPOSE 8000
