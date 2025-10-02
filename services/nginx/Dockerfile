FROM nginx:1.27

RUN openssl req -x509 -newkey rsa:4096 -days 365 -nodes -sha256 \
	-keyout /etc/ssl/private/sinamet_web_key.pem \
	-out /etc/ssl/certs/sinamet_web_cert.pem \
	-subj "/CN=localhost" && \
	chmod 600 /etc/ssl/private/sinamet_web_key.pem

COPY nginx.conf /etc/nginx/nginx.conf
