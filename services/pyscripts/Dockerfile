FROM python:3.13

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "${PYTHONPATH}:/app/lib"

# Définit le répertoire de travail à l'intérieur du conteneur
WORKDIR /app

# Installer bash et outils de base
RUN apt-get update && apt-get install -y \
    bash \
    bash-completion \
    less \
    vim \
    && rm -rf /var/lib/apt/lists/*

# Utiliser bash comme shell par défaut
SHELL ["/bin/bash", "-c"]

# (Optionnel) Met à jour pip
RUN pip install --no-cache-dir --upgrade pip

RUN echo "Processing git cloning v3"
RUN git clone https://github.com/ben10dynartio/apps_mapyourgrid.git
RUN git clone https://github.com/ben10dynartio/osm-power-grid-map-analysis.git

WORKDIR /app/lib
RUN git clone https://github.com/ben10dynartio/filorion.git

WORKDIR /app
RUN pip install -r osm-power-grid-map-analysis/scripts/requirements.txt
RUN pip install -r apps_mapyourgrid/requirements.txt
RUN pip install -r lib/filorion/requirements.txt

COPY ./releasedata/kontur/ ./apps_mapyourgrid/spatial_analysis/data_kontur

#COPY scripts/update-all.sh /usr/local/bin/update-all
#RUN chmod +x /usr/local/bin/update-all

RUN echo "Git repull v14"
WORKDIR /app/apps_mapyourgrid
RUN git pull
WORKDIR /app/osm-power-grid-map-analysis
RUN git pull
WORKDIR /app/lib/filorion
RUN git pull

WORKDIR /app
# Par défaut, lance un shell python interactif
CMD ["python3"]