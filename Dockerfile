# Python 3.12 als Basis
FROM python:3.12-slim

# Setze Umgebungsvariablen
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Arbeitsverzeichnis
WORKDIR /app

# System-Dependencies installieren
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Python-Dependencies installieren
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Projekt-Code kopieren
COPY . /app/

# Statische Dateien sammeln (später)
# RUN python manage.py collectstatic --noinput

# Port freigeben
EXPOSE 8000

# Startbefehl
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
