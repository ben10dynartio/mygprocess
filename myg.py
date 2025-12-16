"""
MapYourGrid Toolbox for managing grid analysis
"""

import argparse
import os
import subprocess
from pathlib import Path

from filorion import MinioFileStorage

MINIO_SECRETKEY_FILE = os.environ.get("MINIO_SECRETKEY_FILE")
with open(MINIO_SECRETKEY_FILE, "r") as f:
    MINIO_SECRETKEY = f.read().strip()  # strip() pour enlever le \n final
MINIO_ACCESSKEY = os.environ.get("MINIO_ACCESSKEY")

fileclient = MinioFileStorage(bucket_name="mapyourgrid", endpoint="myg-minio:9000",
                              access_key=MINIO_ACCESSKEY, secret_key=MINIO_SECRETKEY, secure=False)

LIST_COUNTRY_CODES = ["AF", "AL", "DZ", "AD", "AO", "AG", "AR", "AM", "AU", "AT", "AZ", "BH", "BD", "BB", "BY", "BE",
                      "BZ", "BJ", "BT", "BO", "BA", "BW", "BR", "BN", "BG", "BF", "BI", "KH", "CM", "CA", "CV", "CF",
                      "TD", "CL", "CO", "KM", "CR", "HR", "CU", "CY", "CZ", "CD", "DK", "DJ", "DM", "DO", "EC", "EG",
                      "SV", "GQ", "ER", "EE", "SZ", "ET", "FM", "FJ", "FI", "FR", "GA", "GE", "DE", "GH", "GR", "GD",
                      "GT", "GN", "GW", "GY", "HT", "HN", "HU", "IS", "IN", "ID", "IR", "IQ", "IE", "IL", "IT", "CI",
                      "JM", "JP", "JO", "KZ", "KE", "NL", "KI", "KW", "KG", "LA", "LV", "LB", "LS", "LR", "LY", "LI",
                      "LT", "LU", "MG", "MW", "MY", "MV", "ML", "MT", "MH", "MR", "MU", "MX", "MD", "MC", "MN", "ME",
                      "MA", "MZ", "MM", "NA", "NR", "NP", "NZ", "NI", "NE", "NG", "KP", "MK", "NO", "OM", "PK", "PW",
                      "PA", "PG", "PY", "CN", "PE", "PH", "PL", "PT", "QA", "CG", "RO", "RU", "RW", "KN", "LC", "VC",
                      "WS", "SM", "SA", "SN", "RS", "SC", "SL", "SG", "SK", "SI", "SB", "SO", "ZA", "KR", "SS", "ES",
                      "LK", "PS", "SD", "SR", "SE", "CH", "SY", "ST", "TW", "TJ", "TZ", "TH", "BS", "GM", "TL", "TG",
                      "TO", "TT", "TN", "TR", "TM", "TV", "UG", "UA", "AE", "GB", "US", "UY", "UZ", "VU", "VA", "VE",
                      "VN", "XK", "YE", "ZM", "ZW"]

def pushminiocountry(country):
    print(f"> Starting pushing files to minio ({country})")

    GRID_PATH = Path("databox/shapes/")
    APPS_PATH = Path("apps_mapyourgrid/databox/")


    for filename in [
        "osm_brut_power_line.gpkg",
        "osm_brut_power_line.gpkg",
        "post_graph_power_nodes.gpkg",
        "post_graph_power_nodes_circuit.gpkg",
        "post_graph_power_lines.gpkg",
        "post_graph_power_lines_circuit.gpkg",
    ]:
        try:
            fileclient.push_file(f"databox/shapes/{country}/{filename}",
                                 f"data-countries/{country}/{filename}")
        except Exception as e:
            print("** ERROR when pushing file =", filename)
            print(e)

    files = [
        (GRID_PATH / f"{country}/osm_clean_power_substation.gpkg",
         f"data-countries/{country}/osm_clean_power_substation.gpkg"),
        (GRID_PATH / f"{country}/osm_pdm_power_substations.gpkg",
         f"data-countries/{country}/osm_pdm_power_substations.gpkg"),
        (GRID_PATH / f"{country}/osm_pdm_power_linesxnodes.gpkg",
         f"data-countries/{country}/osm_pdm_power_linesxnodes.gpkg"),
        (GRID_PATH / f"{country}/osm_pdm_power_lines.gpkg",
         f"data-countries/{country}/osm_pdm_power_lines.gpkg"),
        (GRID_PATH / f"{country}/osm_pdm_power_nodes.gpkg",
         f"data-countries/{country}/osm_pdm_power_nodes.gpkg"),
        (GRID_PATH / f"{country}/osm_clean_power_substation.gpkg",
         f"data-countries/{country}/osm_clean_power_substation.gpkg"),
        (APPS_PATH / f"errors_compile/{country}/{country}_list_errors.json",
         f"data-countries/{country}/{country}_list_errors.json"),
        (APPS_PATH / f"errors_compile/{country}/{country}_list_errors.js",
         f"data-countries/{country}/{country}_list_errors.js"),
        (APPS_PATH / f"transmission_layer/{country}_osm_transmission_grid.gpkg",
         f"data-countries/{country}/{country}_osm_transmission_grid.gpkg"),
    ]

    for source_file, dest_file in files:
        try:
            fileclient.push_file(str(source_file), str(dest_file))
        except Exception as e:
            print(f"** ERROR when pushing file :")
            print(e)


def subprocess_country(country):
    try:
        if not nd:
            subprocess.run(f"python apps_mapyourgrid/podoma/run.py layerbuild ln -c {country}", shell=True, check=True)
            subprocess.run(f"python apps_mapyourgrid/podoma/run.py layerbuild sub -c {country}", shell=True, check=True)
            subprocess.run(f"python osm-power-grid-map-analysis/scripts/run.py {country} -d -k bc", shell=True, check=True)
        subprocess.run(f"python osm-power-grid-map-analysis/scripts/run.py {country} -g -s podoma", shell=True, check=True)
        subprocess.run(f"python apps_mapyourgrid/quality_grid_stats/run.py osmose {country}", shell=True, check=True)
        subprocess.run(f"python apps_mapyourgrid/quality_grid_stats/run.py qgstats {country}", shell=True, check=True)
        subprocess.run(f"python apps_mapyourgrid/spatial_analysis/run.py geoclip {country}", shell=True, check=True)
        subprocess.run(f"python apps_mapyourgrid/spatial_analysis/run.py geoanalysis {country}", shell=True,
                       check=True)
        subprocess.run(f"python apps_mapyourgrid/voltage_operator_analysis/run.py voltageoperator {country}",
                       shell=True, check=True)
        subprocess.run(f"python apps_mapyourgrid/circuit_length/run.py circuitlength {country}", shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Country error {country} The process has unexpectly ended")
        with open(f"logs/log_{country}.txt", "w") as file:
            file.write("Got Error =====\n")
            file.write(str(e))

############## ACTIONS

def mergeworld():
    subprocess.run(f"python apps_mapyourgrid/merge_world/run.py qgstats", shell=True)
    #subprocess.run(f"python apps_mapyourgrid/merge_world/run.py osmwiki", shell=True)
    subprocess.run(f"python apps_mapyourgrid/merge_world/run.py spatialanalysis", shell=True)
    subprocess.run(f"python apps_mapyourgrid/merge_world/run.py voltageoperator", shell=True)
    subprocess.run(f"python apps_mapyourgrid/merge_world/run.py circuitlength", shell=True)

    subprocess.run(f"python apps_mapyourgrid/circuit_length/run.py formatcircuitlengthofficial x", shell=True)
    subprocess.run(f"python apps_mapyourgrid/circuit_length/run.py circuitlengthworldcomparison x", shell=True)

    subprocess.run(f"python apps_mapyourgrid/merge_world/run.py buildworldmap", shell=True)
    countrypages()
    gathererrors()


def gathererrors():
    subprocess.run(f"python apps_mapyourgrid/merge_world/run.py gathererrors", shell=True)


def countrypages():
    subprocess.run(f"python apps_mapyourgrid/merge_world/run.py countrypages", shell=True)


def osmwiki():
    subprocess.run(f"python apps_mapyourgrid/osmwiki/run.py osmwiki", shell=True)


def processworld():
    for mycountry in LIST_COUNTRY_CODES:
        subprocess_country(mycountry)


def pushminiocountries():
    for country in LIST_COUNTRY_CODES:
        pushminiocountry(country)


def pushminioworld():
    print(f"> Starting pushing files to minio (worldwide)")
    for filename in [
        "worldmap_indicators.geojson",
        "voltage_operator.csv",
        "list_osm_errors.json",
        "openinframap_countries_info_brut.csv",
        "openinframap_countries_info_lua.txt",
        "wikidata_countries_info_formatted.csv",
        "wikidata_countries_info_brut.csv",
        "wikidata_countries_info_lua.txt",
        "awesomelist.csv"
    ]:
        fileclient.push_file(f"apps_mapyourgrid/data_out/00_WORLD/{filename}",
                             f"data-worldwide/{filename}")

def crosscheckdatasources():
    subprocess.run(f"python apps_mapyourgrid/crosscheck_data_sources/run.py extractawesomelist", shell=True)
    #subprocess.run(f"python apps_mapyourgrid/crosscheck_data_sources/run.py extractwiki", shell=True)
    # subprocess.run(f"python apps_mapyourgrid/crosscheck_data_sources/run.py conflatedatesources", shell=True)

def fullupdate():
    osmwiki()
    crosscheckdatasources()
    processworld()
    mergeworld()
    pushminiocountries()
    pushminioworld()


def updatecountry(country):
    subprocess_country(country)
    mergeworld()
    pushminiocountry(country)
    pushminioworld()


############## SCRIPTS ARGUMENT

parser = argparse.ArgumentParser()
parser.add_argument("action", help="Action to process")
parser.add_argument("country", help="Country code iso a2")
parser.add_argument("-d", "--download", action="store_true", help="Download only")
parser.add_argument("-g", "--graph", action="store_true", help="Graph analysis only")
parser.add_argument("-nd", "--nodownload", action="store_true", help="No download")
parser.add_argument("-s", "--source", action="store_true", help="Source")
args = parser.parse_args()

d, g, nd = args.download, args.graph, args.nodownload
if (not d) & (not g):
    d, g = True, True

if args.action == "pushminiocountry":
    if not args.country:
        raise AttributeError("No country indicated")
    pushminiocountry(args.country)

if args.action == "pushminiocountries":
    pushminiocountries()

if args.action == "pushminioworld":
    pushminioworld()

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

if args.action == "circuitlength":
    if not args.country:
        raise AttributeError("No country indicated")
    subprocess.run(f"python apps_mapyourgrid/circuit_length/run.py circuitlength {args.country}", shell=True)

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
    subprocess_country(args.country)

if args.action == "processworld":
    processworld()

if args.action == "mergeworld":
    mergeworld()

if args.action == "gathererrors":
    gathererrors()

if args.action == "wikidata":
    subprocess.run(f"python apps_mapyourgrid/osmwiki/run.py wikidata", shell=True)

if args.action == "openinframap":
    subprocess.run(f"python apps_mapyourgrid/osmwiki/run.py openinframap", shell=True)

if args.action == "osmwiki":
    osmwiki()

if args.action == "fullupdate":
    fullupdate()

if args.action == "updatecountry":
    if not args.country:
        raise AttributeError("No country indicated")
    updatecountry(args.country)

if args.action == "countrypages":
    countrypages()

if args.action == "crosscheckdatasources":
    crosscheckdatasources()

if args.action == "qgismap":
    subprocess.run(f"python3 osm-power-grid-map-analysis/qgis/standalone-automation.py", shell=True)

if args.action == "qgismapcountry":
    if not args.country:
        raise AttributeError("No country indicated")
    subprocess.run(f"python3 osm-power-grid-map-analysis/qgis/standalone-automation.py {args.country}", shell=True)

