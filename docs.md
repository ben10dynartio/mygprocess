docker stop $(docker ps -a -q) && docker rm myg-minio && docker volume rm mygprocess_minio_data && docker compose up -d --build

rsync -avz -e "ssh -i /chemin/vers/cle_privee" /chemin/local/ fichier utilisateur@serveur.example.com:/chemin/distant/