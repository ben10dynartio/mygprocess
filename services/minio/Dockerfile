FROM alpine:3 AS certs_gen

RUN apk -U add openssl
RUN mkdir -p /opt/minio/certs && \
	openssl req -x509 -newkey rsa:4096 -days 365 -nodes -sha256 \
	-keyout /opt/minio/certs/private.key \
	-out /opt/minio/certs/public.crt \
	-subj "/CN=localhost" && \
	chmod 600 /opt/minio/certs/private.key


FROM minio/minio

COPY --from=certs_gen /opt/minio/certs /opt/minio/certs
