---
id: computing-software.systems-network-administration.netbox.nginx-https-reverse-proxy
name: nginx-https-reverse-proxy
category: computing-software
field: systems-network-administration
product: netbox
tags: [nginx, ssl-certificate, reverse-proxy]
level: practitioner
status: docs-checked
description: "Install the shipped nginx config with a certificate and match it to your WSGI server."
sources: ["https://netboxlabs.com/docs/netbox/installation/5-http-server/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# nginx and HTTPS

Goal: serve NetBox over HTTPS with a WSGI backend.

nginx and Apache work; any HTTP server supporting WSGI should. The docs give Ubuntu 24.04 instructions.

**Certificate.** Use a commercial certificate or Let's Encrypt in production. For testing only, self-signed:
```
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/ssl/private/netbox.key \
  -out /etc/ssl/certs/netbox.crt
```
The prompts for certificate details are all optional.

**nginx**
```
sudo apt install -y nginx
sudo cp /opt/netbox/contrib/nginx.conf /etc/nginx/sites-available/netbox
```
- Replace `netbox.example.com` in the file with your domain or IP; this should match `ALLOWED_HOSTS`.
- The reference file assumes gunicorn. For uWSGI, remove the gunicorn-specific lines beginning with `proxy_pass` and `proxy_set_header` and uncomment the uWSGI section.
- Then remove the default site and enable the NetBox site, as the page continues.

The reference file is `contrib/nginx.conf` in the NetBox tree and is copied, not linked. A trusted certificate matters because browsers and API clients will otherwise warn on self-signed certificates.

**Checklist**

1. Real certificate in production.
2. server_name matches ALLOWED_HOSTS.
3. Config matches gunicorn or uWSGI.

## Checked

2026-11-03: confirmed against the cited NetBox documentation: HTTP server page: nginx/Apache with WSGI, self-signed openssl command, contrib/nginx.conf copy, server_name vs ALLOWED_HOSTS, uWSGI proxy lines. Removed: Nothing.

Method: documentation only; no commands were run.
