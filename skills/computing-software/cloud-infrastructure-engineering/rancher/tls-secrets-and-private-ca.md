---
id: computing-software.cloud-infrastructure-engineering.rancher.tls-secrets-and-private-ca
name: tls-secrets-and-private-ca
category: computing-software
field: cloud-infrastructure-engineering
product: rancher
tags: [tls-rancher-ingress, tls-ca, tls-additional, private-ca, secrets, cattle-system]
level: practitioner
status: docs-checked
description: "Publish certificates to Rancher with kubectl: tls-rancher-ingress from tls.crt and tls.key, tls-ca for a private CA, and tls-additional for node driver CAs."
sources:
  - https://ranchermanager.docs.rancher.com/getting-started/installation-and-upgrade/resources/add-tls-secrets
  - https://ranchermanager.docs.rancher.com/getting-started/installation-and-upgrade/resources/custom-ca-root-certificates
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
With `ingress.tls.source=secret`, Rancher deploys but is not reachable until the `tls-rancher-ingress` secret in `cattle-system` holds your certificate and key. Put the server certificate followed by any intermediates in `tls.crt` (the page notes acme.sh's `fullchain.cer` can simply be renamed) and the key in `tls.key`.

```
kubectl -n cattle-system create secret tls tls-rancher-ingress \
  --cert=tls.crt \
  --key=tls.key
```

To replace the certificate, delete that secret and create it again. With a private CA, replacement is only possible if the new certificate is signed by the same CA.

For a private CA, Rancher needs the root certificate or chain so agents can validate the connection. Put only the CA material in `cacerts.pem` and create the `tls-ca` secret:

```
kubectl -n cattle-system create secret generic tls-ca \
  --from-file=cacerts.pem
```

The `tls-ca` secret is read when Rancher starts, so on a running install the new CA takes effect after new Rancher pods start. A badly formatted chain can stop components downloading from Rancher.

A third secret, `tls-additional`, takes one `.pem` file per extra root certificate for node drivers whose cloud API uses a different CA than Rancher; Rancher mounts them into the node driver pod during provisioning.

The custom CA page explains the related symptom, `x509: certificate signed by unknown authority`, when Rancher reaches catalogs, authentication providers or cloud APIs presenting an internal CA. For Docker installs it uses `SSL_CERT_DIR` with a mounted directory.

## Checked

2026-11-04. Checked against the Rancher Manager documentation pages: Adding TLS Secrets; About Custom CA Root Certificates. Nothing removed.

Method: documentation only; no commands were run.
