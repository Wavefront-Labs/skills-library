---
id: computing-software.cloud-infrastructure-engineering.netdata.reverse-proxy-haproxy
name: reverse-proxy-haproxy
category: computing-software
field: cloud-infrastructure-engineering
product: netdata
tags: [netdata, reverse-proxy, haproxy, subpath]
level: practitioner
status: docs-checked
description: "Run Netdata behind HAProxy: HTTP mode, backend server line, subpath redirect and prefix strip, TLS bind with cert list and basic auth, with doc gotchas."
sources:
  - https://raw.githubusercontent.com/netdata/netdata/master/docs/netdata-agent/configuration/running-the-netdata-agent-behind-a-reverse-proxy/Running-behind-haproxy.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Directives from the docs (all examples assume `mode http` in `defaults`):

```
    bind :::80 v4v6
    server      netdata_local     127.0.0.1:19999
```

Subpath: the frontend redirect adds the trailing slash, and the backend strips the prefix. Both are needed.

```
    http-request redirect scheme https drop-query append-slash if is_netdata ! { path_beg /netdata/ }
    http-request set-path %[path,regsub(^/netdata/,/)]
```

TLS:

```
    bind :::443 v4v6 ssl crt-list /etc/letsencrypt/certslist.txt
    http-request add-header X-Forwarded-Proto https
```

The list maps `example.com /etc/letsencrypt/live/example.com/example.com.pem`.

Basic auth in the backend:

```
    acl devops-auth http_auth_group(basic-auth-list) is-admin
    http-request auth realm netdata_local unless devops-auth
```

Generate a hash instead of plaintext: `printf "YOUR_PASSWORD" | mkpasswd --stdin --method=sha-256`.

Gotchas:
- The page text says key before certificate, but its `cat` puts the certificate first; verify what your HAProxy version accepts.
- Backend examples set `Host` to `%[src]` (client IP); check this is what you want.
- `use_backend ... if is_example_host is_netdata` needs both conditions.
- With Netdata Cloud, bearer token protection avoids the userlist.

## Checked

2026-11-04. Confirmed against the Netdata Running behind HAProxy page: mode http in defaults, the bind and server lines, subpath redirect and set-path regsub, TLS crt-list bind and X-Forwarded-Proto, the cert list mapping, basic auth ACL and realm lines, the mkpasswd hash command, the key-then-certificate text versus the cat order, the Host %[src] header, the full example use_backend line, and the Cloud bearer token tip. Removed the advice to pair with [web] bind to, which this page does not give.

Method: documentation only; no commands were run.
