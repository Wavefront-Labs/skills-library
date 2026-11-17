---
id: computing-software.cloud-infrastructure-engineering.rancher.certificate-troubleshooting-pem-chain-pkcs8
name: certificate-troubleshooting-pem-chain-pkcs8
category: computing-software
field: cloud-infrastructure-engineering
product: rancher
tags: [pem, pkcs8, pkcs1, certificate-chain, openssl, intermediate-certificates]
level: practitioner
status: docs-checked
description: "Troubleshoot certificates given to Rancher: PEM format, PKCS8 to PKCS1 with openssl, intermediate order, and chain validation."
sources:
  - https://ranchermanager.docs.rancher.com/getting-started/installation-and-upgrade/other-installation-methods/rancher-on-a-single-node-with-docker/certificate-troubleshooting
  - https://ranchermanager.docs.rancher.com/getting-started/installation-and-upgrade/resources/add-tls-secrets
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
This guidance comes from the Docker install troubleshooting page and applies to PEM files supplied to Rancher generally.

**PEM recognition:** a certificate starts with `-----BEGIN CERTIFICATE-----`, then a long base64 string, and ends with `-----END CERTIFICATE-----`. A traditional key starts with `-----BEGIN RSA PRIVATE KEY-----`.

**PKCS8 keys:** a key that begins `-----BEGIN PRIVATE KEY-----` is PKCS8. Rancher then logs an error of the form `failed to read private key: asn1: structure error: tags don't match`. Convert it to PKCS1 and use the output file as Rancher's key:

```
openssl rsa -in key.pem -out convertedkey.pem
```

**Chain order:** put your certificate first, then the intermediate certificate(s), each in its own BEGIN/END block, in one file. For the Kubernetes secret flow this combined file is `tls.crt`.

**Validate the chain** with `openssl s_client` against the Rancher host on port 443, passing `-CAfile ca.pem`. A valid chain ends with `Verify return code: 0 (ok)`. The `ca.pem` must be the same file you supplied to Rancher. For a certificate from a recognised CA, omit `-CAfile`.

A private CA also needs its own `tls-ca` secret in `cattle-system`, created from a `cacerts.pem` file (add-tls-secrets page).

## Checked

2026-11-09. Read both cited pages in full (Troubleshooting Certificates; Adding TLS Secrets) and checked every claim against them (PEM headers, PKCS8 error and openssl rsa conversion, chain order, tls.crt, s_client validation, tls-ca). Removed the hostname/CN/SAN match claim, which neither page states.

Method: documentation only; no commands were run.
