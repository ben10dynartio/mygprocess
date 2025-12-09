FROM qgis/qgis

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "${PYTHONPATH}:/app/lib"

# Définit le répertoire de travail à l'intérieur du conteneur
WORKDIR /app

# Installer bash et outils de base
RUN apt-get update && apt-get install -y \
    bash \
    bash-completion \
    && rm -rf /var/lib/apt/lists/*

# Utiliser bash comme shell par défaut
SHELL ["/bin/bash", "-c"]

# (Optionnel) Met à jour pip
#RUN pip install --no-cache-dir --upgrade pip

RUN echo "Processing git cloning v0"
#RUN git clone https://github.com/ben10dynartio/apps_mapyourgrid.git
RUN git clone https://github.com/ben10dynartio/osm-power-grid-map-analysis.git

#WORKDIR /app/lib
#RUN git clone https://github.com/ben10dynartio/filorion.git

#WORKDIR /app
#pip3 install -r osm-power-grid-map-analysis/scripts/requirements.txt --break-system-packages
#RUN pip3 install -r osm-power-grid-map-analysis/scripts/requirements.txt --break-system-packages
#RUN pip3 install -r apps_mapyourgrid/requirements.txt
#RUN pip3 install -r lib/filorion/requirements.txt

# Get and copy release data
#COPY ./services/pyscripts/get_releasedata.sh .
#RUN sh get_releasedata.sh
#COPY ./releasedata/kontur/ ./apps_mapyourgrid/spatial_analysis/data_kontur

#COPY ./services/pyscripts/pullrepo.sh /usr/local/bin/pullrepo
#RUN chmod +x /usr/local/bin/pullrepo

#RUN echo "Git repull v14"
#RUN pullrepo

WORKDIR /app/osm-power-grid-map-analysis/
RUN ln -s ../databox/ databox

WORKDIR /app