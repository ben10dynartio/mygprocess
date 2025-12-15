FROM qgis/qgis:3.44.5-noble

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "${PYTHONPATH}:/app/lib"

# Définit le répertoire de travail à l'intérieur du conteneur
WORKDIR /app

# Installer bash et outils de base
RUN apt-get update && apt-get install -y \
    bash \
    bash-completion \
    nano \
    && rm -rf /var/lib/apt/lists/*

# Utiliser bash comme shell par défaut
SHELL ["/bin/bash", "-c"]

# (Optionnel) Met à jour pip
#RUN pip install --no-cache-dir --upgrade pip

RUN echo "Processing git cloning v0"
RUN git clone https://github.com/ben10dynartio/osm-power-grid-map-analysis.git

WORKDIR /app/osm-power-grid-map-analysis/
RUN ln -s ../databox/ databox

WORKDIR /app