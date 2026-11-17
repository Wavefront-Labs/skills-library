---
id: computing-software.systems-network-administration.jellyfin.https-and-certificates
name: https-and-certificates
category: computing-software
field: systems-network-administration
product: jellyfin
tags: [jellyfin, https, ssl, certificate, pfx, lets-encrypt, ssllabs]
level: practitioner
status: docs-checked
description: "Decide how to provide HTTPS for Jellyfin, preferring a trusted certificate and TLS termination on a reverse proxy."
sources: ["https://jellyfin.org/docs/general/post-install/networking/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# HTTPS for Jellyfin

HTTPS is recommended. It is disabled by default because it needs an SSL certificate. A certificate is issued by a third party and ties the server to a URL, so use a trusted certificate authority such as Let's Encrypt. The docs strongly discourage self-signed certificates because of security and compatibility problems.

Jellyfin supports HTTPS itself (default port 8920/TCP, unused until HTTPS is enabled), but the docs strongly recommend handling HTTPS termination separately on a reverse proxy.

If you expose the service to the internet, the docs strongly recommend testing SSL strength and server security with SSLLabs.

See `computing-software.systems-network-administration.jellyfin.reverse-proxy-requirements` for the proxy requirements, and `computing-software.systems-network-administration.jellyfin.basic-network-troubleshooting` for HTTPS faults.

## Checked

2026-11-08. Confirmed against the Jellyfin Networking page: HTTPS recommended, disabled by default, trusted CA such as Let's Encrypt, self-signed discouraged, reverse proxy termination recommended, SSLLabs advice, 8920/TCP default. Removed: the PFX and Networking page setup, the certificate-first-suspect line and the certbot, port 80/443 and UDP 443 details, none of which are on this page. Page read in full.

Method: documentation only; no commands were run.
