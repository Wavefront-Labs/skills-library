---
id: computing-software.cloud-infrastructure-engineering.harbor.https-certificates
name: https-certificates
category: computing-software
field: cloud-infrastructure-engineering
product: harbor
tags: [https, openssl, san, certificates, docker-certs-d]
level: practitioner
status: docs-checked
description: "Create a CA and SAN server certificate with OpenSSL for Harbor, install it for Harbor and the Docker daemon, and switch an HTTP install to HTTPS."
sources:
  - https://goharbor.io/docs/main/install-config/configure-https/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Harbor ships without certificates. HTTP is acceptable only in air-gapped test or development environments. With a certificate and key from a trusted CA, skip the generation steps and put their paths in `harbor.yml`.

Self-signed chain with OpenSSL, for hostname `yourdomain.com`:
1. `openssl genrsa -out ca.key 4096`, then `openssl req -x509 -new -nodes -sha512 -days 3650 -subj "/C=CN/ST=Beijing/L=Beijing/O=example/OU=Personal/CN=MyPersonal Root CA" -key ca.key -out ca.crt`.
2. `openssl genrsa -out yourdomain.com.key 4096`, then a CSR with `openssl req -sha512 -new -subj ".../CN=yourdomain.com" -key yourdomain.com.key -out yourdomain.com.csr`.
3. Write `v3.ext` containing `authorityKeyIdentifier=keyid,issuer`, `basicConstraints=CA:FALSE`, `keyUsage`, `extendedKeyUsage = serverAuth` and `subjectAltName = @alt_names` with `DNS.1=yourdomain.com`. The SAN file is required whether you connect by FQDN or IP.
4. `openssl x509 -req -sha512 -days 3650 -extfile v3.ext -CA ca.crt -CAkey ca.key -CAcreateserial -in yourdomain.com.csr -out yourdomain.com.crt`.

Install: `sudo mkdir -p /data/cert/` (default location, absent until created) and copy the `.crt` and `.key` there. For Docker, convert with `openssl x509 -inform PEM -in yourdomain.com.crt -out yourdomain.com.cert`, then copy the `.cert`, `.key` and `ca.crt` into `/etc/docker/certs.d/yourdomain.com/` and run `systemctl restart docker`.

Switching an HTTP install: run `./prepare` (it configures nginx), `docker compose down -v` (image data remains), then `docker compose up -d`. Verify with `docker login yourdomain.com`, adding `:port` if nginx 443 is remapped, and make sure `-insecure-registry` is not set for it.

## Checked

2026-11-03. Every command, file name, directory and ordering step was read against the Harbor docs page Configure HTTPS Access to Harbor (goharbor.io/docs/main/install-config/configure-https). Nothing removed.

Method: documentation only; no commands were run.
