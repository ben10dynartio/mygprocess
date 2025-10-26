#!/bin/sh

#!/bin/sh
set -e

# Lancer MinIO en arrière-plan
minio server /data --console-address ":9001" &

# Attendre que MinIO soit prêt
sleep 5

export MINIO_USER_PASSWORD=$(cat $MINIO_USER_PASSWORD_FILE)
export MINIO_SECRETKEY=$(cat $MINIO_SECRETKEY_FILE)
export MINIO_ROOT_PASSWORD=$(cat $MINIO_ROOT_PASSWORD_FILE)

echo ">>>> Starting initialisation of Minio Bucket and key"
ALIASES=$(mc alias ls | cut -d' ' -f1) # Get list of aliases

FOUND=false
for alias in $ALIASES; do
  if [ "$alias" = "$MINIO_USER_CONTAINER" ]; then
    FOUND=true
    break
  fi
done

if [ "$FOUND" = true ]; then
  echo ">> The alias '$MINIO_USER_CONTAINER' is already existing, no necessary action."
else
  echo ">> The alias '$MINIO_USER_CONTAINER' is not existing, creation ..."
  mc alias set $MINIO_USER_CONTAINER http://localhost:9000 $MINIO_ROOT_USER $MINIO_ROOT_PASSWORD
  mc admin user add $MINIO_USER_CONTAINER $MINIO_USER_NAME $MINIO_USER_PASSWORD
  mc admin accesskey create $MINIO_USER_CONTAINER/ $MINIO_USER_NAME --access-key $MINIO_ACCESSKEY --secret-key $MINIO_SECRETKEY
  mc admin policy attach $MINIO_USER_CONTAINER/ readwrite --user=$MINIO_USER_NAME
  mc mb $MINIO_USER_CONTAINER/$MINIO_USER_NAME
  mc anonymous set download $MINIO_USER_CONTAINER/$MINIO_USER_NAME # Public access to bucket
fi
echo ">>>> End of initialisation of Minio Bucket and key"
wait

# mc alias set myminio http://<serveur>:9000 <ACCESS_KEY> <SECRET_KEY>
# mc anonymous set-json cors.json myminio/<bucket>
# OU BIEN
# mc cors set myminio/<bucket> cors.json
# mc cors set mygfiles/mapyourgrid cors.json
# TEST
# mc cors info myminio/<bucket>
