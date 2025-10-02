FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Définit le répertoire de travail à l'intérieur du conteneur
WORKDIR /app

# (Optionnel) Met à jour pip
RUN pip install --no-cache-dir --upgrade pip

# Par défaut, lance un shell python interactif
CMD ["python3"]

