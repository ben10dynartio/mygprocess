#!/bin/sh

CURRENT_DIR=$(pwd)
cd /app/osm-power-grid-map-analysis && git pull || exit
cd /app/apps_mapyourgrid && git pull || exit
cd /app/lib/filorion && git pull || exit
cd "$CURRENT_DIR"