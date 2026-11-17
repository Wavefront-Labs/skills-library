---
id: computing-software.cloud-infrastructure-engineering.k3s.k3s-service-account-issuer-key-rotation
name: k3s-service-account-issuer-key-rotation
category: computing-software
field: cloud-infrastructure-engineering
product: k3s
tags: [k3s, service-account-key, service-key, openssl-genrsa]
level: sme
status: docs-checked
description: "Rotate only the service-account issuer key by installing a service.key that holds both the new and the old key."
sources:
  - https://docs.k3s.io/cli/certificate
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The service-account issuer key is an RSA private key that signs service-account tokens. When rotating, keep at least one old key in the file so existing tokens stay valid. It rotates independently of the cluster CAs via `k3s certificate rotate-ca`, installing only an updated service.key.

Do not overwrite /var/lib/rancher/k3s/server/tls; stage the key elsewhere:

```
mkdir -p /opt/k3s/server/tls
openssl version | grep -qF 'OpenSSL 3' && OPENSSL_GENRSA_FLAGS=-traditional
openssl genrsa ${OPENSSL_GENRSA_FLAGS:-} -out /opt/k3s/server/tls/service.key 2048
cat /var/lib/rancher/k3s/server/tls/service.key >> /opt/k3s/server/tls/service.key
k3s certificate rotate-ca --path=/opt/k3s/server
```

The first command creates the staging directory; the second sets the traditional-format flag when OpenSSL 3 is present; the third generates the new key; the fourth appends the current key so current tokens remain valid; the last loads the file into the datastore.

Warnings for files that are not being updated are normal. On an error, check the service log.

After success, restart K3s on all servers. It is not necessary to restart agents or any pods.

## Checked

2026-11-08: read the whole k3s certificate page (raw markdown from the k3s-io/docs repo, which backs docs.k3s.io/cli/certificate), including the Service-Account Issuer Key Rotation section. Confirmed the commands, the keep-the-old-key rule, the warnings note and the restart scope.

Method: documentation only; no commands were run.
