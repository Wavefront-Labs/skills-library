---
id: computing-software.networking-hardware-and-wireless.caddy.automatic-https-activation
name: automatic-https-activation
category: computing-software
field: networking-hardware-and-wireless
product: caddy
tags: [automatic-https, activation, http-redirect, site-address, ports-80-443, tailscale, caddyfile]
level: intro
status: docs-checked
description: "Know when Caddy's automatic HTTPS turns on or off, what it does (certificates plus HTTP redirects), prerequisites for public names and the .ts.net special case."
sources:
  - https://caddyserver.com/docs/automatic-https
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: predict whether a site gets HTTPS without extra config.

Caddy serves every site over HTTPS by default. IP addresses and local hostnames (`localhost`, `127.0.0.1`) get self-signed certificates that are trusted locally where permitted; public DNS names (`example.com`, `*.example.com`) get certificates from an ACME CA such as Let's Encrypt or ZeroSSL. Certificates are renewed automatically and HTTP (port 80) redirects to HTTPS (443).

For public names the prerequisites are: A/AAAA records pointing at the server, ports 80 and 443 open externally, Caddy able to bind them (or forwarded), a writable and persistent data directory, and the domain appearing in the config. Set DNS before starting Caddy.

Activation happens when Caddy knows a hostname or IP: a Caddyfile site address, a top-level host matcher in JSON routes, CLI flags such as `--domain` or `--from`, or the `automate` certificate loader. It is prevented (wholly or partly) by explicitly disabling it (in a Caddyfile, through global options), giving no hostnames or IPs, listening only on the HTTP port, prefixing the site address with `http://`, or manually loading certificates unless `ignore_loaded_certificates` is set.

Special case: names ending `.ts.net` are not managed by Caddy; it tries to fetch them at handshake time from the local Tailscale instance, which needs HTTPS enabled in the Tailscale account and Caddy running as root or permitted by `tailscaled`.

Effects never override explicit configuration. Existing HTTP-port servers get redirect routes inserted after host-matched routes but before a user catch-all.

## Checked

2026-11-03: read automatic-https against this skill. Confirmed: default behaviour for local versus public names, prerequisites, activation triggers, ways to prevent it, ignore_loaded_certificates, .ts.net Tailscale case, redirect route placement.
Removed or reworded: the literal names of the JSON and Caddyfile disable switches (the page only says to disable it via global options).
Method: documentation only; no commands were run.
