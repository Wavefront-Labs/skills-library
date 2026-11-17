---
id: computing-software.messaging-and-integration.dapr.mtls-bring-your-own-certificates-helm
name: mtls-bring-your-own-certificates-helm
category: computing-software
field: messaging-and-integration
product: dapr
tags: [mtls, certificates, openssl, helm, sentry, root-ca, issuer-ca, kubernetes]
level: advanced
status: docs-checked
description: "Supply your own root and issuer certificates to Sentry on Kubernetes: OpenSSL v3 config, prime256v1 keys, pathlen:0 issuer, and helm --set-file dapr_sentry.tls values."
sources:
  - https://github.com/dapr/docs/blob/v1.15/daprdocs/content/en/operations/security/mtls.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Use this to replace self-signed certs with ones from your PKI. Always sign new certs with the same private root key when rotating, to avoid downtime.

Save as `root.conf` (v3 certificate with SAN):

```ini
[req]
distinguished_name = req_distinguished_name
x509_extensions = v3_req
prompt = no
[req_distinguished_name]
C = US
ST = VA
L = Daprville
O = dapr.io/sentry
OU = dapr.io/sentry
CN = cluster.local
[v3_req]
basicConstraints = critical, CA:true
keyUsage = critical, digitalSignature, cRLSign, keyCertSign
extendedKeyUsage = serverAuth, clientAuth
subjectAltName = @alt_names
[alt_names]
DNS.1 = cluster.local
```

`issuer.conf` is identical except `basicConstraints = critical, CA:true, pathlen:0`. Generate the root, then the issuer:

```bash
openssl ecparam -genkey -name prime256v1 | openssl ec -out root.key
openssl req -new -nodes -sha256 -key root.key -out root.csr -config root.conf -extensions v3_req
openssl x509 -req -sha256 -days 365 -in root.csr -signkey root.key -outform PEM -out root.pem -extfile root.conf -extensions v3_req
openssl ecparam -genkey -name prime256v1 | openssl ec -out issuer.key
openssl req -new -sha256 -key issuer.key -out issuer.csr -config issuer.conf -extensions v3_req
openssl x509 -req -in issuer.csr -CA root.pem -CAkey root.key -CAcreateserial -outform PEM -out issuer.pem -days 365 -sha256 -extfile issuer.conf -extensions v3_req
```

Skip the key-generation lines to reuse existing keys when renewing. Install with:

```bash
helm install \
  --set-file dapr_sentry.tls.issuer.certPEM=issuer.pem \
  --set-file dapr_sentry.tls.issuer.keyPEM=issuer.key \
  --set-file dapr_sentry.tls.root.certPEM=root.pem \
  --namespace dapr-system \
  dapr \
  dapr/dapr
```

Use `helm upgrade` with the same flags to roll new certs onto an existing install.

## Checked

2026-11-08. Read the cited dapr/docs v1.15 page in full and compared each claim; all claims matched the page and none were changed.

Method: documentation only; no commands were run.
