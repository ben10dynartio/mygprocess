"""
MapYourGrid Toolbox for managing grid analysis
"""

import argparse
import os
import subprocess
from pathlib import Path
import shutil

from filorion import MinioFileStorage

MINIO_SECRETKEY_FILE = os.environ.get("MINIO_SECRETKEY_FILE")
with open(MINIO_SECRETKEY_FILE, "r") as f:
    MINIO_SECRETKEY = f.read().strip()  # strip() pour enlever le \n final
MINIO_ACCESSKEY = os.environ.get("MINIO_ACCESSKEY")

fileclient = MinioFileStorage(bucket_name="mapyourgrid", endpoint="myg-minio:9000",
                              access_key=MINIO_ACCESSKEY, secret_key=MINIO_SECRETKEY, secure=False)

LIST_COUNTRY_CODES = ['AD', 'AE', 'AF', 'AG', 'AI', 'AL', 'AM', 'AO', 'AQ', 'AR', 'AT', 'AU', 'AZ', 'BA', 'BB', 'BD',
                      'BE', 'BF', 'BG', 'BH', 'BI', 'BJ', 'BM', 'BN', 'BO', 'BR', 'BS', 'BT', 'BW', 'BY', 'BZ', 'CA',
                      'CD', 'CF', 'CG', 'CH', 'CI', 'CL', 'CM', 'CN', 'CO', 'CR', 'CU', 'CV', 'CY', 'CZ', 'DE', 'DJ',
                      'DK', 'DM', 'DO', 'DZ', 'EC', 'EE', 'EG', 'EH', 'ER', 'ES', 'ET', 'FI', 'FJ', 'FK', 'FM', 'FO',
                      'FR', 'GA', 'GB', 'GD', 'GE', 'GG', 'GH', 'GI', 'GL', 'GM', 'GN', 'GQ', 'GR', 'GS', 'GT', 'GW',
                      'GY', 'HN', 'HR', 'HT', 'HU', 'ID', 'IE', 'IL', 'IM', 'IN', 'IO', 'IQ', 'IR', 'IS', 'IT', 'JE',
                      'JM', 'JO', 'JP', 'KE', 'KG', 'KH', 'KI', 'KM', 'KN', 'KP', 'KR', 'KW', 'KY', 'KZ', 'LA', 'LB',
                      'LC', 'LI', 'LK', 'LR', 'LS', 'LT', 'LU', 'LV', 'LY', 'MA', 'MC', 'MD', 'ME', 'MG', 'MH', 'MK',
                      'ML', 'MM', 'MN', 'MR', 'MS', 'MT', 'MU', 'MV', 'MW', 'MX', 'MY', 'MZ', 'NA', 'NC', 'NE', 'NG',
                      'NI', 'NL', 'NO', 'NP', 'NR', 'NZ', 'OM', 'PA', 'PE', 'PG', 'PH', 'PK', 'PL', 'PN', 'PS', 'PT',
                      'PW', 'PY', 'QA', 'RO', 'RS', 'RU', 'RW', 'SA', 'SB', 'SC', 'SD', 'SE', 'SG', 'SH', 'SI', 'SK',
                      'SL', 'SM', 'SN', 'SO', 'SR', 'SS', 'ST', 'SV', 'SY', 'SZ', 'TC', 'TD', 'TG', 'TH', 'TJ', 'TL',
                      'TM', 'TN', 'TO', 'TR', 'TT', 'TV', 'TW', 'TZ', 'UA', 'UG', 'US', 'UY', 'UZ', 'VA', 'VC', 'VE',
                      'VG', 'VN', 'VU', 'WS', 'XK', 'YE', 'ZA', 'ZM', 'ZW']

def pushminiocountry(country):
    print(f"> Starting pushing files to minio ({country})")

    GRID_PATH = Path("databox/shapes/")
    APPS_PATH = Path("gridinspector/databox/")


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
            subprocess.run(f"python osm-power-grid-map-analysis/scripts/podoma_extractor/run.py layerbuild ln -c {country}", shell=True, check=True)
            subprocess.run(f"python osm-power-grid-map-analysis/scripts/podoma_extractor/run.py layerbuild sub -c {country}", shell=True, check=True)
            subprocess.run(
                f"python osm-power-grid-map-analysis/scripts/podoma_extractor/run.py layerbuild cir -c {country}",
                shell=True, check=True)
            subprocess.run(f"python osm-power-grid-map-analysis/scripts/run.py {country} -d -k bcd", shell=True, check=True)
        subprocess.run(f"python osm-power-grid-map-analysis/scripts/run.py {country} -g -s podoma", shell=True, check=True)
        subprocess.run(f"python gridinspector/quality_grid_stats/run.py osmose {country}", shell=True, check=True)
        subprocess.run(f"python gridinspector/quality_grid_stats/run.py qgstats {country} -s podoma", shell=True, check=True)
        subprocess.run(f"python gridinspector/spatial_analysis/run.py geoclip {country}", shell=True, check=True)
        subprocess.run(f"python gridinspector/spatial_analysis/run.py geoanalysis {country}", shell=True,
                       check=True)
        subprocess.run(f"python gridinspector/voltage_operator_analysis/run.py voltageoperator {country} -s podoma",
                       shell=True, check=True)
        subprocess.run(f"python gridinspector/circuit_length/run.py circuitlength {country} -s podoma", shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Country error {country} The process has unexpectly ended")
        with open(f"logs/log_{country}.txt", "w") as file:
            file.write("Got Error =====\n")
            file.write(str(e))

############## ACTIONS

def mergeworld():
    subprocess.run(f"python gridinspector/merge_world/run.py qgstats", shell=True)
    #subprocess.run(f"python gridinspector/merge_world/run.py osmwiki", shell=True)
    subprocess.run(f"python gridinspector/merge_world/run.py spatialanalysis", shell=True)
    subprocess.run(f"python gridinspector/merge_world/run.py voltageoperator", shell=True)
    subprocess.run(f"python gridinspector/merge_world/run.py circuitlength", shell=True)

    subprocess.run(f"python gridinspector/circuit_length/run.py formatcircuitlengthofficial x", shell=True)
    subprocess.run(f"python gridinspector/circuit_length/run.py circuitlengthworldcomparison x", shell=True)

    subprocess.run(f"python gridinspector/merge_world/run.py buildworldmap", shell=True)
    countrypages()
    gathererrors()


def gathererrors():
    subprocess.run(f"python gridinspector/merge_world/run.py gathererrors", shell=True)


def countrypages():
    subprocess.run(f"python gridinspector/merge_world/run.py countrypages", shell=True)


def osmwiki():
    subprocess.run(f"python gridinspector/osmwiki/run.py osmwiki", shell=True)


def processworld():
    for mycountry in LIST_COUNTRY_CODES:
        subprocess_country(mycountry)


def pushminiocountries():
    for country in LIST_COUNTRY_CODES:
        pushminiocountry(country)


def pushminioworld():
    print(f"> Starting pushing files to minio (worldwide)")
    for filename in [
        "gridinspector_data.geojson",
        "gridinspector_data.json",
        "voltage_operator.csv",
        "list_osm_errors.json",
        "openinframap_countries_info_brut.csv",
        "openinframap_countries_info_lua.txt",
        "wikidata_countries_info_formatted.csv",
        "wikidata_countries_info_brut.csv",
        "wikidata_countries_info_lua.txt",
        "awesomelist.csv"
    ]:
        try:
            fileclient.push_file(f"databox/00_WORLD/{filename}",
                                 f"data-worldwide/{filename}")
        except Exception as e:
            print(f"** ERROR when pushing file '{filename}':")
            print(e)

def crosscheckdatasources():
    subprocess.run(f"python gridinspector/crosscheck_data_sources/run.py extractawesomelist", shell=True)
    #subprocess.run(f"python gridinspector/crosscheck_data_sources/run.py extractwiki", shell=True)
    # subprocess.run(f"python gridinspector/crosscheck_data_sources/run.py conflatedatesources", shell=True)

def fullupdate():
    osmwiki()
    crosscheckdatasources()
    processworld()
    mergeworld()
    pushminiocountries()
    pushminioworld()
    copywww()


def updatecountry(country):
    subprocess_country(country)
    mergeworld()
    pushminiocountry(country)
    pushminioworld()


def copywww():
    # List of files to serve on www
    files = [
        ("gridinspector/indicators_map/index.html", "gridinspector/index.html"),
        ("gridinspector/indicators_map/methodology.html", "gridinspector/methodology.html"),
        ("databox/00_WORLD/gridinspector_data.json", "gridinspector/gridinspector_data.json"),
        ("gridinspector/indicators_map/logo_openinframap.png","gridinspector/logo_openinframap.png"),
        ("gridinspector/indicators_map/logo-github.svg","gridinspector/logo-github.svg"),
        ("gridinspector/indicators_map/favicon.ico","gridinspector/favicon.ico"),
        ("databox/00_WORLD/awesomelist.csv","files/awesomelist.csv"),
        ("databox/00_WORLD/wikidata_countries_info_lua.txt","files/wikidata_countries_info_lua.txt"),
        ("databox/00_WORLD/openinframap_countries_info_lua.txt","files/openinframap_countries_info_lua.txt"),
    ]

    # Répertoire de destination
    destination = Path("www")

    # Copy file
    for fil in files:
        shutil.copy(fil[0], destination / fil[1])


############## SCRIPTS ARGUMENT

parser = argparse.ArgumentParser()
parser.add_argument("action", help="Action to process")
parser.add_argument("country", help="Country code iso a2")
parser.add_argument("-d", "--download", action="store_true", help="Download only")
parser.add_argument("-g", "--graph", action="store_true", help="Graph analysis only")
parser.add_argument("-nd", "--nodownload", action="store_true", help="No download")
parser.add_argument("-s", "--source", type=str, help="Source", default="podoma")
parser.add_argument("-t", "--time", type=str, help="Date of layer", default="CURRENT_TIMESTAMP")
args = parser.parse_args()

d, g, nd = args.download, args.graph, args.nodownload
if (not d) & (not g):
    d, g = True, True

match args.action:
    case "pushminiocountry":
        if not args.country:
            raise AttributeError("No country indicated")
        pushminiocountry(args.country)

    case "pushminiocountries":
        pushminiocountries()

    case "pushminioworld":
        pushminioworld()

    case "copywww":
        copywww()

    case "overpass":
        if not args.country:
            raise AttributeError("No country indicated")
        subprocess.run(f"python osm-power-grid-map-analysis/scripts/run.py {args.country} -d", shell=True)

    case "graphanalysis":
        if not args.country:
            raise AttributeError("No country indicated")
        subprocess.run(f"python osm-power-grid-map-analysis/scripts/run.py {args.country} -g", shell=True)

    case "buildgraphworld":
        subprocess.run(f"python osm-power-grid-map-analysis/scripts/gather_country_graph.py", shell=True)
    case _:
        print("Not in match case ...")


if args.action == "osmose":
    if not args.country:
        raise AttributeError("No country indicated")
    subprocess.run(f"python gridinspector/quality_grid_stats/run.py osmose {args.country}", shell=True)

if args.action == "qgstats":
    if not args.country:
        raise AttributeError("No country indicated")
    subprocess.run(f"python gridinspector/quality_grid_stats/run.py qgstats {args.country}", shell=True)

if args.action == "circuitlength":
    if not args.country:
        raise AttributeError("No country indicated")
    subprocess.run(f"python gridinspector/circuit_length/run.py circuitlength {args.country}", shell=True)

if args.action == "geoclip":
    if not args.country:
        raise AttributeError("No country indicated")
    subprocess.run(f"python gridinspector/spatial_analysis/run.py geoclip {args.country}", shell=True)

if args.action == "geoanalysis":
    if not args.country:
        raise AttributeError("No country indicated")
    subprocess.run(f"python gridinspector/spatial_analysis/run.py geoanalysis {args.country}", shell=True)

if args.action == "voltageoperator":
    if not args.country:
        raise AttributeError("No country indicated")
    subprocess.run(f"python gridinspector/voltage_operator_analysis/run.py voltageoperator {args.country}", shell=True)

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
    subprocess.run(f"python gridinspector/osmwiki/run.py wikidata", shell=True)

if args.action == "openinframap":
    subprocess.run(f"python gridinspector/osmwiki/run.py openinframap", shell=True)

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

if args.action == "layerbuild":
    if not args.country:
        raise AttributeError("No country indicated")
    if args.source == "podoma":
        script_base = "python osm-power-grid-map-analysis/scripts/podoma_extractor/run.py layerbuild"
        subprocess.run(f"{script_base} ln -c {args.country} -d {args.time}", shell=True, check=True)
        subprocess.run(f"{script_base} sub -c {args.country} -d {args.time}", shell=True, check=True)
        subprocess.run(f"{script_base} cir -c {args.country} -d {args.time}", shell=True, check=True)