FROM python:3.11-bullseye

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y wget bzip2 libc6 libgtk-3-0 libgl1 mesa-utils && rm -rf /var/lib/apt/lists/*

RUN wget https://github.com/prusa3d/PrusaSlicer/releases/download/version_2.7.2/PrusaSlicer-2.7.2+linux-x64-GTK3-202402291307.tar.bz2  -O prusaslicer.tar.bz2

RUN tar -xjf prusaslicer.tar.bz2 -C /opt/ && rm prusaslicer.tar.bz2

RUN ln -s /opt/PrusaSlicer-2.7.2+linux-x64-GTK3-202402291307/prusa-slicer /usr/local/bin/prusaslicer

COPY . /usr/src/app

RUN pip install poetry

RUN poetry config virtualenvs.create false \
    && poetry install --no-dev

CMD ["sh", "-c", "bash /usr/src/app/bin/prod/migrate.sh && poetry run uvicorn main_app.main:app --reload --host 0 --port 8000"]

EXPOSE 8000
