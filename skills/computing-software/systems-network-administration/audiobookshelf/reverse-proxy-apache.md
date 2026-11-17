---
id: computing-software.systems-network-administration.audiobookshelf.reverse-proxy-apache
name: reverse-proxy-apache
category: computing-software
field: systems-network-administration
product: audiobookshelf
tags: [reverse-proxy, apache, a2enmod, websocket, mod-proxy, rewrite]
level: practitioner
status: docs-checked
description: "Configure Apache httpd as an Audiobookshelf reverse proxy, including the modules to enable and the 2.4.47 upgrade=websocket form."
sources:
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/install/reverse-proxy/3.apache-proxy-setup.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Enable at least these modules with `a2enmod`: `ssl`, `proxy`, `proxy_http`, `proxy_balancer`, `proxy_wstunnel`, `rewrite`.

Classic virtual host with a rewrite for websockets:

```apache
<IfModule mod_ssl.c>
<VirtualHost *:443>
    ServerName <sub>.<domain>.<tld>
    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined

    ProxyPreserveHost On
    ProxyPass / http://localhost:<audiobookshelf_port>/
    RewriteEngine on
    RewriteCond %{HTTP:Upgrade} websocket [NC]
    RewriteCond %{HTTP:Connection} upgrade [NC]
    RewriteRule ^/?(.*) "ws://localhost:<audiobookshelf_port>/$1" [P,L]

    SSLCertificateFile /path/to/cert/file
    SSLCertificateKeyFile /path/to/key/file
</VirtualHost>
</IfModule>
```

On Apache 2.4.47 or newer you can drop the `RewriteEngine` lines and use:

```apache
<Location /audiobookshelf>
    ProxyPreserveHost on
    ProxyPass http://localhost:<audiobookshelf_port>/audiobookshelf upgrade=websocket
    ProxyPassReverse http://localhost:<audiobookshelf_port>/audiobookshelf
</Location>
```

Let's Encrypt: certificates needing ACME validation require `/.well-known` to be served directly. Add `DocumentRoot /path/to/local/directory` and put `ProxyPass /.well-known !` before `ProxyPass / http://localhost:<audiobookshelf_port>/` inside the VirtualHost so the challenge is not proxied.

## Checked

2026-11-04. Confirmed against the Audiobookshelf docs: Apache reverse proxy page.

Method: documentation only; no commands were run.
