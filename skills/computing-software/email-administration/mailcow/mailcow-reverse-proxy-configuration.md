---
id: computing-software.email-administration.mailcow.mailcow-reverse-proxy-configuration
name: mailcow-reverse-proxy-configuration
category: computing-software
field: email-administration
product: mailcow
tags: [reverse-proxy, http-bind, https-bind, enable-ssl-sni, post-hook, external-acme, additional-server-names]
level: advanced
status: docs-checked
description: "Run mailcow behind Nginx, Apache, HAProxy, Traefik, Caddy or Pangolin by rebinding HTTP ports to localhost and handling certificate reloads."
sources: ["https://docs.mailcow.email/post_installation/reverse-proxy/r_p/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Running mailcow behind a reverse proxy

The bundled Nginx site needs no changes. mailcow trusts the default gateway `172.22.1.1` as proxy. In `mailcow.conf` bind the web ports to a local address, for example `HTTP_BIND=127.0.0.1`, `HTTP_PORT=8080`, `HTTPS_BIND=127.0.0.1`, `HTTPS_PORT=8443`. This also changes the bindings inside the Nginx container. Do not use ports 8081, 9081 or 65510. Recreate containers after the change.

Run `generate_config.sh` before enabling any example site configuration, because it copies snake-oil certificates to the expected location so services can start. Documented examples exist for Apache 2.4, Nginx, HAProxy, Traefik v3, Caddy v2 and Pangolin.

If you enable `ENABLE_SSL_SNI`, certificate paths in the proxy must match the per-hostname directories under `data/assets/ssl/`.

The example configurations forward ACME requests to mailcow so acme-mailcow keeps managing certificates; the proxy must then be reloaded after a certificate changes (daily reload or a file watcher; logrotate often does this already). With a local certbot instead, use a post-hook that copies `fullchain.pem` and `privkey.pem` to `data/assets/ssl/cert.pem` and `key.pem` and restarts postfix-mailcow, dovecot-mailcow and nginx-mailcow.

To reach the UI under a name other than `MAILCOW_HOSTNAME`, list it in `ADDITIONAL_SERVER_NAMES` (comma separated, no spaces) first.

## Checked

2026-11-04. Confirmed on the Reverse proxy page: gateway 172.22.1.1 trusted as proxy, HTTP_BIND/HTTPS_BIND example with ports 8080/8443, the warning about ports 8081, 9081 and 65510, generate_config.sh snake-oil certificates, ENABLE_SSL_SNI path split, the listed proxies, ACME forwarding and reload note, the post-hook copy/restart steps, and ADDITIONAL_SERVER_NAMES (comma separated, no spaces). No changes needed.

Method: documentation only; no commands were run.
