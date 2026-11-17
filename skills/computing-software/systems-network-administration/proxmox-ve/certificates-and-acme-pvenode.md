---
id: computing-software.systems-network-administration.proxmox-ve.certificates-and-acme-pvenode
name: certificates-and-acme-pvenode
category: computing-software
field: systems-network-administration
product: proxmox-ve
tags: [certificates, acme, lets-encrypt, pvenode, pveproxy]
level: practitioner
status: docs-checked
description: "Get trusted TLS certificates for the Proxmox VE web UI via ACME with pvenode, using HTTP or DNS challenges."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-sysadmin.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Each cluster has a self-signed CA; node certificates are signed by it and live at `/etc/pve/nodes/NODENAME/pve-ssl.pem`. The `pveproxy` service serves the API and GUI. Custom or ACME certificates go to `/etc/pve/local/pveproxy-ssl.pem` and `/etc/pve/local/pveproxy-ssl.key` (key must have no password). Never edit the generated `pve-ssl.pem/key` or the CA files `/etc/pve/pve-root-ca.pem` and `/etc/pve/priv/pve-root-ca.key`. To trust the cluster CA on workstations copy `/etc/pve/pve-root-ca.pem` out of band; there is no API download.

ACME flow, one account per cluster. Use the Let's Encrypt staging directory first because of rate limits:

```
pvenode acme account register default mail@example.invalid
pvenode config set --acme domains=example.invalid
pvenode acme cert order
```

The built-in `standalone` plugin does http-01 validation on port 80, so port 80 must be reachable, nothing else may listen on it, and the name must resolve to the node. For dns-01 use a plugin based on acme.sh DNS APIs: `pvenode acme plugin add dns example_plugin --api ovh --data /path/to/api_token`, then `pvenode config set -acmedomain0 example.proxmox.com,plugin=example_plugin`. Plugin config is in `/etc/pve/priv/acme/plugins.cfg`. For alias mode, set a CNAME from `_acme-challenge.domain1` to `_acme-challenge.domain2` and the `alias` property on the acmedomain.

Changing an account's directory is unsupported; deactivate it (`pvenode acme account deactivate default`) and register a new one against the production endpoint. Renewal runs from `pve-daily-update.service` when the certificate is expired or expires within 30 days.

## Checked

2026-11-03. Commands, option names, defaults, limits and behaviour claims were compared with the official Proxmox VE documentation pages: https://pve.proxmox.com/pve-docs/chapter-sysadmin.html (plus the chapter-qm, qm.1, pct, pvecm, pvesm, vzdump, pvesr and sysadmin pages). Items shown as placeholder or example values (file names, VM IDs, device names) are illustrative. Figures that the pages did not state were removed or reworded.

Method: documentation only; no commands were run.
