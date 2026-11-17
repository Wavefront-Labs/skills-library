---
id: computing-software.networking-hardware-and-wireless.caddy.local-https-internal-ca
name: local-https-internal-ca
category: computing-software
field: networking-hardware-and-wireless
product: caddy
tags: [local-https, internal-ca, root-certificate, trust-store, skip-install-trust, caddy-trust, smallstep]
level: practitioner
status: docs-checked
description: "Caddy local CA: root and intermediate in pki/authorities/local, trust install, skip_install_trust, caddy trust/untrust, container caveats."
sources:
  - https://caddyserver.com/docs/automatic-https
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: understand and manage certificates for non-public hosts.

Caddy generates its own CA, built on Smallstep libraries, and signs certificates for local and non-public names. The chain is a root plus an intermediate; leaf certificates are signed by the intermediate. Files live in the data directory at `pki/authorities/local`. This does not use ACME or DNS validation; it works only on the local machine and is trusted only where the root is installed.

Root: its private key is generated from a cryptographically secure source, stored with limited permissions and loaded into memory only to sign (by default only to sign intermediates; signing leaves directly with the root can be configured for non-compliant clients). The first time it is used Caddy tries to install it in the system trust store(s) and may prompt for a password. Disable with `skip_install_trust` (Caddyfile) or `"install_trust": false` (JSON). If it failed because Caddy was unprivileged, run `caddy trust` as a privileged user. The cert appears as "Caddy Local Authority" unless renamed, and `caddy untrust` removes it.

Intermediates have much shorter lifetimes and renew automatically.

Caveats: automatic installation is a convenience, not guaranteed, especially in containers or unprivileged services; ensuring clients trust the root is the administrator's job. Clients that do not trust it show security errors. Trusting the root on your own machine is safe if the machine is not compromised and the unique root key does not leak.

## Checked

2026-11-08. Read the Automatic HTTPS page in full (Local HTTPS, CA Root and CA Intermediates sections). Confirmed: Smallstep-based CA, root and intermediate chain, `pki/authorities/local`, no ACME or DNS validation, root key handling, signing only intermediates by default, trust-store installation and password prompt, `skip_install_trust` and `"install_trust": false`, `caddy trust`, the Caddy Local Authority name, `caddy untrust`, shorter-lived auto-renewed intermediates, and the container and unprivileged-service caveat.

Method: documentation only; no commands were run.

