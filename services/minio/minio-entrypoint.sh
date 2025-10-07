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

# Configurer l'alias mc
echo ">>>> Initialisation of Minio Bucket and key"
mc alias set $MINIO_USER_CONTAINER http://localhost:9000 $MINIO_ROOT_USER $MINIO_ROOT_PASSWORD
mc admin user add $MINIO_USER_CONTAINER $MINIO_USER_NAME $MINIO_USER_PASSWORD
mc admin accesskey create $MINIO_USER_CONTAINER/ $MINIO_USER_NAME --access-key $MINIO_ACCESSKEY --secret-key $MINIO_SECRETKEY
mc admin policy attach $MINIO_USER_CONTAINER/ readwrite --user=$MINIO_USER_NAME
# Public access to mapyourgrid bucket
mc mb $MINIO_USER_CONTAINER/$MINIO_USER_NAME
mc anonymous set download $MINIO_USER_CONTAINER/$MINIO_USER_NAME
echo ">>>> Minio Bucket and key are build"
# Laisser MinIO tourner au premier plan
wait
