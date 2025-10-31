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
    print(f"> Starting pushing files to minio ({args.country})")

    for filename in [
        "osm_clean_power_substation.gpkg",
        "osm_brut_power_line.gpkg",
        "osm_brut_power_line.gpkg",
        "post_graph_power_nodes.gpkg",
        "post_graph_power_nodes_circuit.gpkg",
        "post_graph_power_lines.gpkg",
        "post_graph_power_lines_circuit.gpkg",
    ]:
        try:
            fileclient.push_file(f"osm-power-grid-map-analysis/data/{country}/{filename}",
                                 f"data-countries/{country}/{filename}")
        except Exception as e:
            print("** ERROR when pushing file =", filename)
            print(e)
    try:
        fileclient.push_file(f"apps_mapyourgrid/data_out/errors_compile/{country}/{country}_list_errors.json",
                                 f"data-countries/{country}/{country}_list_errors.json")
    except Exception as e:
        print(f"** ERROR when pushing file {country}_list_errors.json")
        print(e)


def subprocess_country(country):
    try:
        subprocess.run(f"python osm-power-grid-map-analysis/scripts/run.py {country} -d", shell=True, check=True)
        subprocess.run(f"python osm-power-grid-map-analysis/scripts/run.py {country} -g", shell=True, check=True)
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
    subprocess.run(f"python apps_mapyourgrid/merge_world/run.py osmwiki", shell=True)
    subprocess.run(f"python apps_mapyourgrid/merge_world/run.py spatialanalysis", shell=True)
    subprocess.run(f"python apps_mapyourgrid/merge_world/run.py voltageoperator", shell=True)
    subprocess.run(f"python apps_mapyourgrid/merge_world/run.py circuitlength", shell=True)
    subprocess.run(f"python apps_mapyourgrid/merge_world/run.py buildworldmap", shell=True)
    gathererrors()


def gathererrors():
    subprocess.run(f"python apps_mapyourgrid/merge_world/run.py gathererrors", shell=True)


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
    ]:
        fileclient.push_file(f"apps_mapyourgrid/data_out/00_WORLD/{filename}",
                             f"data-worldwide/{filename}")


def fullupdate():
    osmwiki()
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
args = parser.parse_args()

d, g = args.download, args.graph
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

