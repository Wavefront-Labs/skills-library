---
id: computing-software.devops-ci-cd.semaphore-ui.reverse-proxy-apache
name: reverse-proxy-apache
category: computing-software
field: devops-ci-cd
product: semaphore-ui
tags: [apache, httpd, reverse-proxy, proxy-wstunnel, websocket, semaphore-ui]
level: practitioner
status: docs-checked
description: "Enable the Apache proxy modules and configure a virtual host that proxies Semaphore including websockets."
sources:
  - https://semaphoreui.com/docs/admin-guide/reverse-proxy/apache
  - https://semaphoreui.com/docs/admin-guide/reverse-proxy
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Apache in front of Semaphore

Goal: serve Semaphore through Apache httpd over TLS.

Enable the modules first:

```bash
sudo a2enmod proxy
sudo a2enmod proxy_http
sudo a2enmod proxy_wstunnel
```

Virtual host:

```
<VirtualHost *:443>
    ServerName example.com
    ServerAdmin webmaster@localhost
    SSLEngine on
    SSLCertificateFile /path/to/example.com.crt
    SSLCertificateKeyFile /path/to/example.com.key
    ProxyPreserveHost On

    <Location />
        ProxyPass http://127.0.0.1:3000/
        ProxyPassReverse http://127.0.0.1:3000/
    </Location>

    <Location /api/ws>
        RewriteCond %{HTTP:Connection} Upgrade [NC]
        RewriteCond %{HTTP:Upgrade} websocket [NC]
        ProxyPass ws://127.0.0.1:3000/api/ws/
        ProxyPassReverse ws://127.0.0.1:3000/api/ws/
    </Location>
</VirtualHost>
```

Notes:
- `/api/ws` is the websocket route. Task logs stream over a websocket, and without the upgrade handling the log window stays empty while the task runs; the Apache page lists `proxy_wstunnel` among the modules to enable.
- Set `web_host` in Semaphore to the public URL; Semaphore builds redirect URLs, sets the cookie `Secure` flag and checks the request origin from it, so sign-in fails if it does not match what the browser used.

Verify: open a running task in the browser and confirm its log fills while it runs.

## Checked

2026-11-07. Read in full, from markdown sources in the semaphore-docs repository (no snippet files included): admin-guide/reverse-proxy/apache.md and admin-guide/reverse-proxy/README.md. Confirmed: the three a2enmod commands, the virtual host (copied from the page), the websocket route and the three requirements every proxy must meet. Removed: the claim that ProxyPreserveHost matters for OIDC, the claim tying a missing proxy_wstunnel to real-time UI updates, and the configtest Verify step.
Method: documentation only; no commands were run.
