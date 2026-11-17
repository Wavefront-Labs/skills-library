---
id: computing-software.cloud-infrastructure-engineering.kubespray.cert-manager-addon-and-ingress-certificates
name: cert-manager-addon-and-ingress-certificates
category: computing-software
field: cloud-infrastructure-engineering
product: kubespray
tags: [cert-manager, tls, ingress, acme, cluster-issuer, internal-ca]
level: practitioner
status: docs-checked
description: "Enable cert-manager in Kubespray, request ingress certificates by annotation, trust an internal ACME CA and bootstrap a root CA key pair."
sources:
  - https://kubespray.io/docs/advanced/cert_manager.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
cert-manager is a Kubernetes certificate controller that issues from sources such as Let's Encrypt, Vault, Venafi, a signing key pair or self-signed, and renews before expiry. Enable it in the addons inventory (`group_vars/k8s_cluster/addons.yml`):

```ini
cert_manager_enabled: true
```

**CA issuer.** To secure ingress with a private CA, deploy the Kubernetes `ca-key-pair` secret holding the Root CA certificate and key. The page walks through creating one with Cloudflare's `cfssl` (`cfssl gencert -initca ca-csr.json | cfssljson -bare ca`), notes `ssh-keygen` and OpenSSL as alternatives, and sets default expiry `8760h` (one year). Verify with `openssl x509 -text -noout -in ca.pem` that the dates are right and `CA:TRUE` is present.

**Ingress certificates.** Add the annotation and a `tls` section to the Ingress; cert-manager's ingress-shim creates the Certificate:

```yaml
metadata:
  annotations:
    cert-manager.io/cluster-issuer: ca-issuer
spec:
  ingressClassName: "traefik"
  tls:
  - hosts:
    - prometheus.example.com
    secretName: prometheus-dashboard-certs
```

The page states the certificate is rotated every 3 months and stored in that secret.

**ACME with an internal CA.** cert-manager must trust the CA at deployment level. Add its certificate in `group_vars/k8s-cluster/addons.yml`:

```yaml
cert_manager_trusted_internal_ca: |
  -----BEGIN CERTIFICATE-----
  [REPLACE with your CA certificate]
  -----END CERTIFICATE-----
```

Then define the issuer normally.

## Checked

2026-11-08. Cited pages re-read in full. Enablement, annotation usage, rotation interval and the internal CA variable were confirmed on the cert-manager installation guide page; the full Ingress manifest and cfssl JSON files were not reproduced.

Method: documentation only; no commands were run.
