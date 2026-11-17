---
id: computing-software.cloud-infrastructure-engineering.portainer.use-your-own-ssl-certificate
name: use-your-own-ssl-certificate
category: computing-software
field: cloud-infrastructure-engineering
product: portainer
tags: [tls, ssl, certificates, pem, sslcert]
level: practitioner
status: docs-checked
description: "Replace Portainer's self-signed certificate with your own PEM certificate using the sslcert and sslkey flags or the UI."
sources:
  - https://github.com/portainer/portainer-docs/blob/HEAD/2.39-lts/advanced/ssl.md
  - https://github.com/portainer/portainer-docs/blob/HEAD/2.39-lts/admin/settings/general.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default Portainer serves the UI and API over HTTPS using a self-signed certificate generated at install. Replace it either after installation under Settings, SSL certificate, or at install time with flags.

Portainer expects PEM format. Include the full chain, intermediates included, in the file given to `--sslcert`; without it you may hit certificate validation problems. On Docker Standalone, upload the certificate and key to the host and mount them:

```
docker run -d -p 9443:9443 -p 8000:8000 \
  --name portainer --restart always \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v portainer_data:/data \
  -v /path/to/your/certs:/certs \
  portainer/portainer-ee:sts \
  --sslcert /certs/portainer.crt --sslkey /certs/portainer.key
```

The default paths are `/certs/portainer.crt` and `/certs/portainer.key` on Linux. The page also covers Swarm and Kubernetes.

Force HTTPS only is a UI setting, and `--http-disabled` serves HTTPS only; make sure any agents are configured for HTTPS first, or you can lock yourself out of the instance.

## Checked

2026-11-04. Checked against the Portainer 2.39 LTS documentation pages in `sources` (portainer-docs on GitHub, fetched this batch): commands, flags, ports, paths, defaults and UI steps. No wrong claims found; nothing removed.

Method: documentation only; no commands were run.
