---
id: computing-software.systems-network-administration.pki-tls-administration.os-trust-store-install
name: os-trust-store-install
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [os-trust-store-install, pki-trust-distribution, trust-store, update-ca-certificates, update-ca-trust, certutil-addstore, pki-tls-administration]
level: practitioner
status: draft
description: "Install a private root CA into Debian, RHEL, macOS and Windows trust stores and containers."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-cs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Installing a private root in OS trust stores
Goal: system tools trust your internal CA.
- Debian/Ubuntu: copy `root.crt` (PEM, .crt extension) to `/usr/local/share/ca-certificates/` and run `update-ca-certificates`.
- RHEL/Fedora: copy to `/etc/pki/ca-trust/source/anchors/` and `update-ca-trust`.
- Alpine: `/usr/local/share/ca-certificates` + `update-ca-certificates`.
- macOS: `sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain root.crt`.
- Windows: `certutil -addstore -f Root root.crt` (local) or GPO Trusted Root Certification Authorities (domain). Enterprise CAs publish via AD.
- Containers: add the cert in the image, run the update command, or mount into `/etc/ssl/certs`.
- Tools with own stores: Java cacerts, Python `certifi`/`REQUESTS_CA_BUNDLE`, Node `NODE_EXTRA_CA_CERTS`, Git `http.sslCAInfo`, Firefox policy `Certificates.Install`.
Gotcha: Debian ignores files without `.crt`; and a file containing several certs may only partly load, so one cert per file.
Verify:
- [ ] `openssl verify -CApath /etc/ssl/certs leaf.pem` returns OK.
- [ ] `curl https://internal.example.com` works without `-k` from a fresh host.
