# mygprocess

This docker image for automating quality analysis of electrical networks on OpenStreetMap.

This is build in the context of #MapYourGrid project. 
[Learn more about the project ](https://mapyourgrid.org/fr/)

# Set up

Clone this repository.



# How it works

The docker image, on its building will download several repository and data.

Repositories :
https://github.com/ben10dynartio/apps_mapyourgrid/
https://github.com/ben10dynartio/osm-power-grid-map-analysis
https://github.com/ben10dynartio/filorion

Data :
(used for substation coverage evaluation)

The docker build two dockers :
- A python environment for running the scripts.
- A Minio instance for data storage and serving.