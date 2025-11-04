#!/usr/bin/env bash

# Variables à modifier
OWNER="ben10dynartio"
REPO="mygprocess"
ASSET_NAME="releasedata.zip"
DEST_DIR="."

# Step 1 : Get JSON about last release
API_URL="https://api.github.com/repos/$OWNER/$REPO/releases/latest"
JSON=$(curl -s "$API_URL")

# Step 2 : Extract file URL with grep + sed
DOWNLOAD_URL=$(echo "$JSON" | grep -oP '"browser_download_url":\s*"\K[^"]+' | grep "$ASSET_NAME")

if [ -z "$DOWNLOAD_URL" ]; then
    echo "❌ Asset '$ASSET_NAME' not found in last release."
    exit 1
fi

# Étape 3 : télécharger le fichier
echo "⬇️Download of $ASSET_NAME..."
curl -L -o "$ASSET_NAME" "$DOWNLOAD_URL"
echo "✅ Download complete : $ASSET_NAME"

unzip -o "$ASSET_NAME" -d "."

if [ $? -ne 0 ]; then
  echo "❌ Extraction failed"
  exit 1
fi

echo "✅ Extraction complete !"
