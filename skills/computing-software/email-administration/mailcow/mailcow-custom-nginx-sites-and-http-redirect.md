---
id: computing-software.email-administration.mailcow.mailcow-custom-nginx-sites-and-http-redirect
name: mailcow-custom-nginx-sites-and-http-redirect
category: computing-software
field: email-administration
product: mailcow
tags: [nginx-custom-site, webmail-redirect, http-redirect, additional-san-site, update-hooks]
level: advanced
status: docs-checked
description: "Host extra sites or a webmail subdomain on mailcow's Nginx, redirect HTTP to HTTPS and run scripts around update.sh."
sources: ["https://docs.mailcow.email/manual-guides/Nginx/u_e-nginx_custom/", "https://docs.mailcow.email/manual-guides/Nginx/u_e-nginx_webmail-site/", "https://docs.mailcow.email/manual-guides/u_e-80_to_443/", "https://docs.mailcow.email/manual-guides/u_e-update-hooks/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Custom Nginx sites, HTTP redirect and update hooks

Persistent extra sites go in `data/conf/nginx/*.conf`. The template includes the mailcow certificate (`/etc/ssl/mail/cert.pem` and `key.pem`), TLS 1.2 and 1.3 settings, `root /web;` (the `data/web` directory), the `listen_plain.active` and `listen_ssl.active` includes, a `server_name`, and a `/.well-known/acme-challenge/` location so ACME validation works with another web root. Do not set `ADDITIONAL_SERVER_NAMES` for a name that uses a different web root.

Webmail subdomain: create a `webmail.conf` whose server block returns `301 https://<MAILCOW_HOSTNAME>/SOGo`, restart Nginx, then add the new name to `ADDITIONAL_SAN` in `mailcow.conf` (no quotes) and apply with `docker compose up -d`. The webmail guide applies to non-SNI setups only; with SNI the certificate path must be adjusted (for example `/etc/ssl/mail/webmail.example.org/cert.pem`), and the certificate must exist before the site config is created or Nginx fails to start.

HTTP to HTTPS: leave `HTTP_BIND=` unset and, for version 2025-01a or newer, set `HTTP_REDIRECT=y`, then recreate containers. Behind a reverse proxy, use the proxy's redirect instead.

Update hooks: place `pre_update_hook.sh` (runs on every `update.sh` call) and `post_update_hook.sh` (runs only after a successful update) in the mailcow root. They run under bash, so no shebang or execute bit is required.

## Checked

2026-11-04. Confirmed on the Custom sites, webmail subdomain, HTTP to HTTPS and update-hooks pages: data/conf/nginx placement, template contents, acme-challenge location, the ADDITIONAL_SERVER_NAMES caution, webmail.conf redirect to /SOGo, ADDITIONAL_SAN without quotes, HTTP_BIND= and HTTP_REDIRECT=y for 2025-01a or newer, and the two hook scripts. Added the page's SNI caveat details.

Method: documentation only; no commands were run.
