---
id: computing-software.collaboration-platform-administration.mattermost.ssl-client-certificate-mutual-tls
name: ssl-client-certificate-mutual-tls
category: computing-software
field: collaboration-platform-administration
product: mattermost
tags: [client-certificates, mutual-tls, nginx-proxy, openssl]
level: advanced
status: docs-checked
description: "Require client TLS certificates for the Mattermost web and desktop apps through NGINX: create a CA, sign user certificates, configure NGINX and test."
sources: ["https://docs.mattermost.com/administration-guide/onboard/ssl-client-certificate.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# SSL client certificates (mutual TLS)

Prerequisite: Mattermost installed behind NGINX with SSL and HTTP/2 and a valid certificate. Client certificates work for the browser and desktop apps on Windows, macOS and Linux, but are not yet supported on the mobile apps.

Steps:
1. Create a CA key and a self-signed CA certificate: openssl genrsa -des3 -out ca.mattermost.key 4096, then openssl req -new -x509 -days 365 -key ca.mattermost.key -out ca.mattermost.crt. NGINX uses this CA to verify client certificates.
2. Per user, create a key and signing request: openssl genrsa -des3 -out <user>.key 1024 and openssl req -new -key <user>.key -out <user>.csr, using the user's name as the Common Name and a passphrase placeholder such as <PASSPHRASE>.
3. Sign it: openssl x509 -req -days 365 -in <user>.csr -CA ca.mattermost.crt -CAkey ca.mattermost.key -set_serial 01 -out <user>.crt.
4. Inspect with openssl x509 -in <user>.crt -text -noout.
5. In the NGINX site file add ssl_client_certificate pointing at the CA certificate and ssl_verify_client on, and in both the websocket location and the root location add proxy_set_header X-SSL-Client-Cert $ssl_client_cert and proxy_set_header X-SSL-Client-Cert-Subject-DN $ssl_client_s_dn.
6. Test with curl -v -s -k --key <user>.key --cert <user>.crt:<PASSPHRASE> https://<server>; the login page should appear. "No required SSL certificate was sent" means a step was missed. "Decryption has failed" means the passphrase must be given together with the certificate, since curl does not prompt separately.
7. Package for the browser: openssl pkcs12 -export -out <user>.p12 -inkey <user>.key -in <user>.crt -certfile ca.mattermost.crt.
8. Repeat steps 2 to 7 for other users, then import the .p12 into each machine's key store (for Chrome on macOS: Manage certificates opens Keychain Access, File > Import Items). Browsing to the site should now prompt for the certificate.

The guide strongly recommends an SSL certificate on the server for security, compliance and to avoid browser limitations. Generating the CA is optional if you already have one.

## Checked

2026-11-03. Confirmed against the Mattermost documentation page https://docs.mattermost.com/administration-guide/onboard/ssl-client-certificate (openssl and NGINX steps, curl test). Nothing removed.

Method: documentation only; no commands were run.
