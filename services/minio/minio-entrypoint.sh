#!/bin/sh

#!/bin/sh
set -e

# Lancer MinIO en arrière-plan
minio server /data --console-address ":9001" &

# Attendre que MinIO soit prêt
sleep 5

# Configurer l'alias mc
echo ">>>> Initialisation of Minio Bucket and key"
mc alias set mygfiles http://localhost:9000 $MINIO_ROOT_USER $MINIO_ROOT_PASSWORD
mc admin user add mygfiles mapyourgrid mapyourgrid_pass
mc admin accesskey create mygfiles/ mapyourgrid --access-key AKYGhrfree6687 --secret-key hirfiecbreverehidbz9863894gbjdeok
mc admin policy attach mygfiles/ readwrite --user=mapyourgrid
mc mb mygfiles/mapyourgrid
echo ">>>> Minio Bucket and key are build"
# Laisser MinIO tourner au premier plan
wait


#sleep 5
#echo ">> Initialisation of Minio Bucket and key"
#mc alias list
#mc alias set mygfiles http://localhost:9000 minioadmin miniopass
#mc admin user add mygfiles mapyourgrid mapyourgrid_pass
#mc admin accesskey create mygfiles/ mapyourgrid --access-key AKYGhrfree6687 --secret-key hirfiecbreverehidbz9863894gbjdeok
#mc admin policy attach mygfiles/ readwrite --user=mapyourgrid
#echo ">> Initialisation of Minio Bucket and key"
#tail -f /dev/null