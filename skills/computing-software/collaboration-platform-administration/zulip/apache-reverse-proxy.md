---
id: computing-software.collaboration-platform-administration.zulip.apache-reverse-proxy
name: apache-reverse-proxy
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [apache2, proxypass, a2enmod, use-x-forwarded-host]
level: advanced
status: docs-checked
description: "Front Zulip with Apache2: required modules, USE_X_FORWARDED_HOST, virtual host with ProxyPass timeout, RequestHeader X-Forwarded-Proto, TLS and HSTS settings."
sources: ["https://zulip.readthedocs.io/en/latest/production/reverse-proxies.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Apache2 in front of Zulip

Prerequisites: complete the proxy-trust configuration on the Zulip server, then set `USE_X_FORWARDED_HOST = True` in `/etc/zulip/settings.py` and restart Zulip. Enable modules:

```
a2enmod ssl proxy proxy_http headers rewrite
```

The backend must be addressed by hostname, not IP, if you use TLS to Zulip (the example uses `internal.zulip.hostname:443`).

Create `/etc/apache2/sites-available/zulip.example.com.conf` on Debian or Ubuntu, then run `a2ensite zulip.example.com && systemctl reload apache2`. The file contains:

- A port 80 virtual host that rewrites everything to `https://%{HTTP_HOST}%{REQUEST_URI}` with a 301.
- A port 443 virtual host with `ServerName`, `RequestHeader set "X-Forwarded-Proto" expr=%{REQUEST_SCHEME}`, and a `RewriteRule /(.*)` that proxies (`[P,L]`) to the internal Zulip URL.
- A `<Location />` block with `Require all granted` and `ProxyPass https://internal.zulip.hostname:443/ timeout=1200`.
- `SSLEngine on`, `SSLProxyEngine on`, and `SSLCertificateFile` and `SSLCertificateKeyFile` for your certificate.
- Hardening: `SSLProtocol all -SSLv3 -TLSv1 -TLSv1.1`, a modern ECDHE `SSLCipherSuite`, `SSLSessionTickets off`, and `Header set Strict-Transport-Security "max-age=31536000"`.

The DH parameters file can be copied from Zulip's nginx files. The 1200 second timeout is what keeps long-polling alive.

## Checked

2026-11-03: commands, paths, flags, settings and figures read against the Zulip documentation page production/reverse-proxies.html (zulip.readthedocs.io, latest). Removed: nothing.

Method: documentation only; no commands were run.
