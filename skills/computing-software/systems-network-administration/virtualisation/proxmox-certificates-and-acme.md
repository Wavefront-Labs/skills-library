---
id: computing-software.systems-network-administration.virtualisation.proxmox-certificates-and-acme
name: proxmox-certificates-and-acme
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [pve-acme, pve-certificates, lets-encrypt, dns-01, pveproxy, custom-certificate, proxmox, proxmox-ve, tls]
level: practitioner
status: docs-checked
description: "Give Proxmox VE nodes trusted certificates: ACME (Let's Encrypt) with HTTP-01 or DNS-01 plugins, uploading a custom CA-signed cert, and what not to touch in /etc/pve."
sources:
  - https://pve.proxmox.com/pve-docs/pve-admin-guide.html#sysadmin_certificate_management
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Proxmox VE certificates and ACME

**Goal:** the web UI and API (port 8006) present a trusted certificate that renews itself.

## How PVE certificates work
- The cluster has its own CA (`/etc/pve/pve-root-ca.pem`) that signs each node's
  `pve-ssl.pem`; used internally between nodes. **Do not replace these.**
- For browsers/API clients, add `pveproxy-ssl.pem`/`.key` per node (custom or ACME);
  pveproxy prefers it when present.

## ACME (Let's Encrypt or internal ACME CA)
1. Datacenter → ACME → Accounts → register (email, directory: Let's Encrypt production or staging,
   the endpoints the admin guide lists).
2. **Challenge plugin:**
   - HTTP-01: node must be reachable on port 80 from the CA (rare for internal nodes).
   - **DNS-01:** add a DNS plugin (any API supported by acme.sh) with API
     credentials; works for internal-only nodes.
3. Node → System → Certificates → ACME → add domain (node FQDN), choose plugin → Order.
CLI:
```sh
pvenode acme account register default admin@<domain>
pvenode config set --acme domains=pve1.<domain>   # plus acmedomain0 for DNS plugin
pvenode acme cert order
```
Renewal is automatic via `pve-daily-update.service` (attempted when expired or expiring within 30 days).

## Custom certificate
Node → System → Certificates → Upload Custom Certificate (cert chain + key) or
`pvenode cert set cert.pem key.pem --restart`. Include the full chain.

## Gotchas
- Cluster with one FQDN behind a load balancer: each node still needs its own cert; put
  the LB name in SANs if clients use it.
- DNS plugin configuration is stored in `/etc/pve/priv/acme/plugins.cfg`; scope API tokens to the one zone.
- Removing the custom cert reverts to the self-signed PVE cert; clients pinning
  fingerprints (e.g. PBS storage config) need updating after any change.

## Verify
`openssl s_client -connect pve1.<domain>:8006 -servername pve1.<domain> </dev/null | openssl x509 -noout -issuer -dates`
shows your CA/Let's Encrypt and a future expiry; the browser shows no warning.

## Checked
2026-11-01. Confirmed in the Proxmox VE admin guide: `pveproxy-ssl.pem`/`.key` override, `pvenode acme account register`, `pvenode acme cert order`, `pvenode cert set` with `--restart`, ACME endpoints, renewal timer and 30-day window, `/etc/pve/priv/acme/plugins.cfg`. Removed: named DNS providers and non-Let's Encrypt directories.
Method: documentation only; no commands were run.
