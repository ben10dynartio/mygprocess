"""
MapYourGrid Toolbox for managing grid analysis
"""

import argparse
import os
import subprocess
from filorion import MinioFileStorage

MINIO_SECRETKEY_FILE = os.environ.get("MINIO_SECRETKEY_FILE")
with open(MINIO_SECRETKEY_FILE, "r") as f:
    MINIO_SECRETKEY = f.read().strip()  # strip() pour enlever le \n final
MINIO_ACCESSKEY = os.environ.get("MINIO_ACCESSKEY")

fileclient = MinioFileStorage(bucket_name="mapyourgrid", endpoint="myg-minio:9000",
                              access_key=MINIO_ACCESSKEY, secret_key=MINIO_SECRETKEY, secure=False)
print("acces with", MINIO_ACCESSKEY, MINIO_SECRETKEY)
def push_country_files_to_minio(country):
    print(f"> Starting pushing files to minio ({args.country})")
    if country:
        for filename in [
            "osm_clean_power_substation.gpkg",
            "osm_brut_power_line.gpkg",
            "osm_brut_power_line.gpkg",
            "post_graph_power_nodes.gpkg",
            "post_graph_power_nodes_circuit.gpkg",
            "post_graph_power_lines.gpkg",
            "post_graph_power_lines_circuit.gpkg",
        ]:
            fileclient.push_file(f"osm-power-grid-map-analysis/data/{country}/{filename}",
                                 f"data-countries/{country}/{filename}")
    else:
        raise ValueError("A country is required")

def push_worldwide_files_to_minio():
    print(f"> Starting pushing files to minio (worldwide)")
    for filename in [
        "worldmap_indicators.geojson",
        "voltage_operator.csv",
    ]:
        fileclient.push_file(f"apps_mapyourgrid/data_out/00_WORLD/{filename}",
                             f"data-worldwide/{filename}")

parser = argparse.ArgumentParser()
parser.add_argument("action", help="Action to process")
parser.add_argument("country", help="Country code iso a2")
parser.add_argument("-d", "--download", action="store_true", help="Download only")
parser.add_argument("-g", "--graph", action="store_true", help="Graph analysis only")
args = parser.parse_args()

d, g = args.download, args.graph
if (not d) & (not g):
    d, g = True, True

if args.action == "pushminiocountry":
    if not args.country:
        raise AttributeError("No country indicated")
    push_country_files_to_minio(args.country)

if args.action == "pushminioworld":
    push_worldwide_files_to_minio()

if args.action == "overpass":
    if not args.country:
        raise AttributeError("No country indicated")
    subprocess.run(f"python osm-power-grid-map-analysis/scripts/run.py {args.country} -d", shell=True)

if args.action == "graphanalysis":
    if not args.country:
        raise AttributeError("No country indicated")
    subprocess.run(f"python osm-power-grid-map-analysis/scripts/run.py {args.country} -g", shell=True)

if args.action == "osmose":
    if not args.country:
        raise AttributeError("No country indicated")
    subprocess.run(f"python apps_mapyourgrid/quality_grid_stats/run.py osmose {args.country}", shell=True)

if args.action == "qgstats":
    if not args.country:
        raise AttributeError("No country indicated")
    subprocess.run(f"python apps_mapyourgrid/quality_grid_stats/run.py qgstats {args.country}", shell=True)

if args.action == "geoclip":
    if not args.country:
        raise AttributeError("No country indicated")
    subprocess.run(f"python apps_mapyourgrid/spatial_analysis/run.py geoclip {args.country}", shell=True)

if args.action == "geoanalysis":
    if not args.country:
        raise AttributeError("No country indicated")
    subprocess.run(f"python apps_mapyourgrid/spatial_analysis/run.py geoanalysis {args.country}", shell=True)

if args.action == "voltageoperator":
    if not args.country:
        raise AttributeError("No country indicated")
    subprocess.run(f"python apps_mapyourgrid/voltage_operator_analysis/run.py voltageoperator {args.country}", shell=True)

if args.action == "processcountry":
    if not args.country:
        raise AttributeError("No country indicated")
    try:
        subprocess.run(f"python osm-power-grid-map-analysis/scripts/run.py {args.country} -d", shell=True, check=True)
        subprocess.run(f"python osm-power-grid-map-analysis/scripts/run.py {args.country} -g", shell=True, check=True)
        subprocess.run(f"python apps_mapyourgrid/quality_grid_stats/run.py osmose {args.country}", shell=True, check=True)
        subprocess.run(f"python apps_mapyourgrid/quality_grid_stats/run.py qgstats {args.country}", shell=True, check=True)
        subprocess.run(f"python apps_mapyourgrid/spatial_analysis/run.py geoclip {args.country}", shell=True, check=True)
        subprocess.run(f"python apps_mapyourgrid/spatial_analysis/run.py geoanalysis {args.country}", shell=True, check=True)
        subprocess.run(f"python apps_mapyourgrid/voltage_operator_analysis/run.py voltageoperator {args.country}",
                       shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print("The process has unexpectly ended")
        # Ouvre (ou crée) un fichier en mode écriture
        with open("logs/log_v1.txt", "w") as fichier:
            fichier.write("Got Error =====\n")
            fichier.write(str(e))
        raise e

if args.action == "mergeworld":
    subprocess.run(f"python apps_mapyourgrid/merge_world/run.py qgstats", shell=True)
    subprocess.run(f"python apps_mapyourgrid/merge_world/run.py osmwiki", shell=True)
    subprocess.run(f"python apps_mapyourgrid/merge_world/run.py spatialanalysis", shell=True)
    subprocess.run(f"python apps_mapyourgrid/merge_world/run.py voltageoperator", shell=True)
    subprocess.run(f"python apps_mapyourgrid/merge_world/run.py buildworldmap", shell=True)

if args.action == "wikidata":
    subprocess.run(f"python apps_mapyourgrid/osmwiki/run.py wikidata", shell=True)

if args.action == "openinframap":
    subprocess.run(f"python apps_mapyourgrid/osmwiki/run.py openinframap", shell=True)

if args.action == "osmwiki":
    subprocess.run(f"python apps_mapyourgrid/osmwiki/run.py wikidata", shell=True)
    subprocess.run(f"python apps_mapyourgrid/osmwiki/run.py openinframap", shell=True)