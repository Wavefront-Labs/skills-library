---
id: computing-software.collaboration-platform-administration.zulip.certbot-lets-encrypt-automation
name: certbot-lets-encrypt-automation
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [certbot, lets-encrypt, setup-certbot, certificate-renewal]
level: practitioner
status: docs-checked
description: "Use Zulip's Certbot automation: the --certbot installer flag, setup-certbot for existing servers and multiple hostnames, 90-day renewal timer and renewal debugging."
sources: ["https://zulip.readthedocs.io/en/latest/production/ssl-certificates.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Certbot and Let's Encrypt in Zulip

Recommended for most servers. Skip it if you have your own certificate workflow, need wildcard certificates, or the server is not on the public Internet (Certbot can still be used manually, but ignore Zulip's automation then).

At install time pass `--certbot` together with the required `--hostname` and `--email`. The hostname must be a real DNS name and the machine reachable from the public Internet by that name.

On an installed server, as root:

```
~zulip/deployments/current/scripts/setup/setup-certbot --email=EMAIL HOSTNAME [HOSTNAME2...]
```

Extra hostnames produce one multi-domain certificate. The first run creates a Let's Encrypt account, requests a certificate and proves control of the website.

Let's Encrypt certificates last 90 days. The `certbot` package installs a systemd timer that repeats the proof of control, installs the new certificate and reloads nginx, so no ongoing work is needed.

If a certificate expires, the usual cause is a firewall blocking the renewal process, which behaves like the original request. Debug interactively as root by running `/usr/bin/certbot renew`.

## Checked

2026-11-03: commands, paths, flags, settings and figures read against the Zulip documentation page production/ssl-certificates.html (zulip.readthedocs.io, latest). Removed: the line about where certificate files end up.

Method: documentation only; no commands were run.
