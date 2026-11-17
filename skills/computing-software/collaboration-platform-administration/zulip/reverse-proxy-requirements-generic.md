---
id: computing-software.collaboration-platform-administration.zulip.reverse-proxy-requirements-generic
name: reverse-proxy-requirements-generic
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [other-proxies, x-forwarded-proto, long-polling]
level: advanced
status: docs-checked
description: "Checklist for any other reverse proxy in front of Zulip: X-Forwarded-For, overwritten X-Forwarded-Proto, Host header, long-polling timeouts and IPv4/IPv6 upstream pitfalls."
sources: ["https://zulip.readthedocs.io/en/latest/production/reverse-proxies.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Reverse proxy requirements for any implementation

If your proxy is not nginx, Apache or HAProxy, ensure these points:

1. **X-Forwarded-For** keeps the full chain of client addresses, and Zulip is told which proxy addresses to trust. Verify in `/var/log/zulip/server.log`: it must show real client IPs, not the proxy's.
2. **X-Forwarded-Proto** carries `https` or `http` for the browser-to-proxy connection. Django uses it for CSRF checks. The proxy must set the header, replacing any existing value, not add a second one. If your proxy cannot set it, do all HTTP-to-HTTPS redirection at the load balancer and set `loadbalancer.rejects_http_requests` in `zulip.conf`, noting the security caveats documented for that option.
3. **Host** header is the client's original, not the internal name. If impossible, set `USE_X_FORWARDED_HOST = True` in `/etc/zulip/settings.py` and send the original in `X-Forwarded-Host`.
4. **Long-polling** must not be interfered with. Use `proxy_read_timeout 1200;` (anything well above 60 seconds, applied to all endpoints, especially the events API) and `proxy_buffering off`, otherwise nginx may return sporadic 502 errors.
5. **IPv4/IPv6**: nginx can balance between both addresses of a hostname, causing mysterious errors. Declare the upstream so it cannot, for instance by naming a DNS entry that resolves to a single address.

## Checked

2026-11-03: commands, paths, flags, settings and figures read against the Zulip documentation page production/reverse-proxies.html (zulip.readthedocs.io, latest). Removed: nothing.

Method: documentation only; no commands were run.
