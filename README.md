# mygprocess

This docker image for automating quality analysis of electrical networks on OpenStreetMap.

It is build to runs the python scripts in the following repositories : 
[Apps MapYourGrid](https://github.com/ben10dynartio/apps_mapyourgrid/) &
[OSM Power Grid Map Analysis](https://github.com/ben10dynartio/osm-power-grid-map-analysis).

This tool is build in the context of #MapYourGrid project. 
[Learn more about the project ](https://mapyourgrid.org/fr/)

## Set up

1. Clone this repository. `git clone https://github.com/ben10dynartio/mygprocess.git`
2. Create the password files into `multipass` folder (see [Readme file](multipass/README.md))
3. Go to the root of the repository. Build docker containers `docker compose up -d --build`
4. (Optional) Set up CRON task if you want to process regularly
( `python myg.py fullupdate x` from inside the docker (not tested), 
or `docker exec -d myg-pyscripts python myg.py fullupdate x` from outside)

   
## How it works

You can call the different analysis on the OSM power grid through the `myg.py` script
from docker root.

Run `docker exec -it myg-pyscripts bash` to get into the docker.

Then call the `myg.py` script in the `/app` folder with 2 arguments : 
analysis name and country code (2 letters). 
For no country code, set `x` or whatever.

For example :
```commandline
python myg.py osmwiki x            # Get Wikidata and OpenInfraMap Data
python myg.py fullupdate x         # Process all countries, then load to Minio
python myg.py updatecountry BG     # Update Bulgaria data, then load to Minio
python myg.py processworld x       # Process all countries
python myg.py processcountry TZ    # Process Tanzania
```

Look at `myg.py` file for all available options.

You can also set an alias for execution from outside docker : `alias='docker exec -it myg-pyscripts python myg.py'`
then simply run for example `myg updatecountry BG` from shell, outside docker.

## Architecture
The docker image, on its building will download several repositories and data.

**Repositories :**
* https://github.com/ben10dynartio/apps_mapyourgrid/
* https://github.com/ben10dynartio/osm-power-grid-map-analysis
* https://github.com/ben10dynartio/filorion (utils repository to manage Minio)

**Data :**
* `releasedata.zip` from https://github.com/ben10dynartio/mygprocess/releases/latest (used for substation coverage evaluation)

The docker compose build two containers :
- A python environment for running the scripts.
- A Minio instance for data storage and serving.

