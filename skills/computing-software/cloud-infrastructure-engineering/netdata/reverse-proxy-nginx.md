---
id: computing-software.cloud-infrastructure-engineering.netdata.reverse-proxy-nginx
name: reverse-proxy-nginx
category: computing-software
field: cloud-infrastructure-engineering
product: netdata
tags: [netdata, reverse-proxy, nginx, basic-auth]
level: practitioner
status: docs-checked
description: "Publish a Netdata Agent behind Nginx: upstream keepalive, subfolder path, TLS to Netdata, basic auth, locking down direct access and SELinux 502s."
sources:
  - https://raw.githubusercontent.com/netdata/netdata/master/docs/netdata-agent/configuration/running-the-netdata-agent-behind-a-reverse-proxy/Running-behind-nginx.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Building blocks from the docs:
- Upstream: `server 127.0.0.1:19999;` with `keepalive 1024;` in an `upstream` block (64 in the subfolder examples). Keepalive needs `proxy_http_version 1.1;` and the `Connection "keep-alive"` header.
- Subfolder: `location = /netdata` returns `301 /netdata/;` and a regex location forwards with `proxy_pass http://netdata/$ndpath$is_args$args;`.
- Netdata over TLS: add `proxy_set_header X-Forwarded-Proto https;` and `proxy_pass https://localhost:19999;`.
- Basic auth:

```
printf "yourusername:$(openssl passwd -apr1)" > /etc/nginx/passwords
```

then `auth_basic "Protected";` and `auth_basic_user_file passwords;` in the server block.

Lock down direct access in `netdata.conf` `[web]`: `bind to = 127.0.0.1 ::1`, or `bind to = unix:/var/run/netdata/netdata.sock`, or for a remote Nginx `bind to = *` with `allow connections from = IP_OF_NGINX_SERVER`. Avoid duplicate logs with `[logs] access = off`. To avoid double compression set `enable gzip compression = no` under `[web]` when Nginx gzips.

Gotchas:
- Subfolder URLs need the trailing slash.
- TLS Netdata behind plain HTTP proxy gives `SSL_ERROR_RX_RECORD_TOO_LONG`.
- A "Permission denied" connect error suggests SELinux: `setsebool -P httpd_can_network_connect true`.
- Run `nginx -t` before restarting.
- With Netdata Cloud, bearer token protection is simpler than htpasswd.

## Checked

2026-11-04. Confirmed against the Netdata Running behind Nginx page: upstream keepalive values, the subfolder redirect and proxy_pass form, TLS proxy lines and the SSL_ERROR_RX_RECORD_TOO_LONG error, the openssl passwd command and auth_basic lines, all three direct-access lockdown options, [logs] access = off, gzip handling, the SELinux fix, nginx -t, and the Cloud bearer token tip. Nothing removed.

Method: documentation only; no commands were run.
