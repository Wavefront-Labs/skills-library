---
id: computing-software.cloud-infrastructure-engineering.graylog.trusted-header-auth
name: trusted-header-auth
category: computing-software
field: cloud-infrastructure-engineering
product: graylog
tags: [trusted-header, sso-proxy, trusted-proxies, remote-user]
level: advanced
status: docs-checked
description: "Single sign-on through a reverse-proxy HTTP header: enable it, set the Username header and restrict trusted_proxies in CIDR form."
sources:
  - https://go2docs.graylog.org/current/setting_up_graylog/trusted_header_authentication.htm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# trusted header auth

Requirements: Graylog is accessed through a proxy (Apache, NGINX, HAProxy), the proxy sends the configured Username header, the proxy's source IPs are listed in `trusted_proxies` in `server.conf`, and the user must already exist in Graylog.

Enable (disabled by default): **System > Authentication > Authenticators > Edit Authenticators**, check Enable single sign-on via HTTP header, optionally set the Username header (default `Remote-User`), Update Config.

`trusted_proxies` takes comma-separated CIDR subnets. `/32` means a single address:

```
trusted_proxies = 127.0.0.1/32, 192.168.0.2/32, 192.168.0.3/32
```

The proxy must authenticate users and pass the header, and must not remove or unset session cookies. The REST API no longer allows user authentication via a trusted header.

## Checked

2026-11-04. Confirmed against the Trusted Header Authentication page (requirements, menu path, Remote-User default, trusted_proxies CIDR examples, cookie and REST API warnings). Replaced the unstated claim that Graylog rejects the header without a matching proxy IP with the page's cookie and REST API warnings.

Method: documentation only; no commands were run.
