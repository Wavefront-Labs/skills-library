---
id: computing-software.collaboration-platform-administration.zulip.self-signed-certificate
name: self-signed-certificate
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [self-signed-cert, generate-self-signed-cert, nginx-reload]
level: intro
status: docs-checked
description: "Generate a self-signed certificate for Zulip with --self-signed-cert or generate-self-signed-cert, when it is acceptable, and why apps will refuse to connect."
sources: ["https://zulip.readthedocs.io/en/latest/production/ssl-certificates.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Self-signed certificates for Zulip

A self-signed certificate is convenient for testing but insecure for production, and the Zulip desktop and mobile apps will not connect to a server whose certificate they cannot validate. Desktop apps can be configured with a custom certificate authority to trust an internal certificate. It is acceptable for production only when the server is behind a reverse proxy.

At install time, pass `--self-signed-cert` to the installer script.

On an existing server, as root:

```
~zulip/deployments/current/scripts/setup/generate-self-signed-cert HOSTNAME
```

Here HOSTNAME is the domain name, or an IP address, to put on the generated certificate.

After replacing certificates you must reload nginx, as root:

```
service nginx reload
```

Use cases where it makes sense:

- Test installations.
- Servers behind a reverse proxy (installing with `--self-signed-cert` rather than `--certbot` is recommended when the server is not on the public Internet).

Do not use it for servers that mobile users reach directly. Switch to Certbot or a manually installed certificate before onboarding real users.

## Checked

2026-11-03: commands, paths, flags, settings and figures read against the Zulip documentation page production/ssl-certificates.html (zulip.readthedocs.io, latest). Removed: unsupported use-case wording (no-DNS testing, proxy presents public certificate).

Method: documentation only; no commands were run.
