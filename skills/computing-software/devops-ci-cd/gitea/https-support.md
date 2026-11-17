---
id: computing-software.devops-ci-cd.gitea.https-support
name: https-support
category: computing-software
field: devops-ci-cd
product: gitea
tags: [gitea-lets-encrypt, gitea, acme, acme-directory, redirect-other-port, cert-file, tls-alpn-01, http-01]
level: practitioner
status: docs-checked
description: "Enable HTTPS in Gitea: CERT_FILE/KEY_FILE chain order, HTTP redirect port, built-in ACME with Let's Encrypt or smallstep, and the ACME_DIRECTORY volume trap."
sources: ["https://docs.gitea.com/administration/https-setup/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# HTTPS for Gitea

## Built-in server
```ini
[server]
PROTOCOL  = https
ROOT_URL  = https://git.example.com:3000/
HTTP_PORT = 3000
CERT_FILE = cert.pem
KEY_FILE  = key.pem
```
`gitea cert --host [HOST]` makes a self-signed pair for testing. For a CA-signed cert, `cert.pem` must hold the server certificate first, then intermediates in order; the root is not needed. Relative `CERT_FILE`/`KEY_FILE` paths resolve against `GITEA_CUSTOM`; absolute paths work.
Gitea listens on one port, so to redirect plain HTTP:
```ini
[server]
REDIRECT_OTHER_PORT = true
PORT_TO_REDIRECT = 3080
```
In Docker, publish that port too.

## ACME (Let's Encrypt by default)
Only `HTTP-01` (port 80) and `TLS-ALPN-01` (port 443) challenges are implemented, so external traffic on those ports must reach Gitea (port forwards and the redirect service may be needed). You must accept the CA terms.
```ini
[server]
PROTOCOL=https
DOMAIN=git.example.com
ENABLE_ACME=true
ACME_ACCEPTTOS=true
ACME_DIRECTORY=https
ACME_EMAIL=email@example.com   ; may be given at first run, then cached
```
For a smallstep (or other ACME) CA add `ACME_URL=https://ca.example.com/acme/acme/directory` and optionally `ACME_CA_ROOT=/path/to/root_ca.crt` (omit to use system trust).

### Trap: ACME_DIRECTORY in containers
`ACME_DIRECTORY` caches the account key and certificates; the default `https` is relative to the process working directory, which in the official rootful image is `/app/gitea`, inside the container and not in the `/data` volume. Each recreated container then requests fresh certificates, and Let's Encrypt allows 5 certificates per week for the same domains, after which you have no valid cert until the limit expires. Set `ACME_DIRECTORY=/data/gitea/https`. The rootless image keeps its working directory (`/var/lib/gitea`) in a volume, so it only suffers when that volume is not persisted.

## Alternative
Terminate TLS at a reverse proxy (see `gitea-reverse-proxy-nginx`); fine on one machine or a private network. Use the built-in HTTPS if the proxy-to-Gitea hop crosses a public network.

## Checked

2026-11-03: read https://docs.gitea.com/administration/https-setup/ line by line; the commands, options, defaults and values stated above match those pages.
Removed: nothing; every claim was confirmed.
Method: documentation only; no commands were run.
