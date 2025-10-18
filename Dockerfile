FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 netcat-openbsd curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN playwright install --with-deps chromium

COPY . .

CMD sh -c "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"
