---
id: computing-software.collaboration-platform-administration.zulip.reverse-proxy-http-and-trusted-ips
name: reverse-proxy-http-and-trusted-ips
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [reverse-proxy, http-only, loadbalancer-ips, x-forwarded-for]
level: advanced
status: docs-checked
description: "Prepare Zulip for a reverse proxy: http_only in zulip.conf, loadbalancer ips, X-Forwarded headers, zulip-puppet-apply and restart-server to avoid redirect loops."
sources: ["https://zulip.readthedocs.io/en/latest/production/reverse-proxies.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Reverse proxy: HTTP mode and trusted proxies

If the server is not on the public Internet, install with `--self-signed-cert` rather than `--certbot`, since Certbot needs public reachability.

Zulip needs HTTPS to clients, but a proxy may terminate TLS and speak HTTP to Zulip, which is safe when Zulip is not directly exposed. To enable it, add to `/etc/zulip/zulip.conf`:

```
[application_server]
http_only = true
```

Then run `~zulip/deployments/current/scripts/zulip-puppet-apply` as root and restart with `~zulip/deployments/current/scripts/restart-server`.

Zulip must also know which proxies to trust. It does not trust `X-Forwarded-*` headers by default, because then clients could forge IP addresses or claim a connection was secure. Find the proxy addresses as Zulip sees them (CIDR ranges allowed; they may differ from public addresses), and add:

```
[loadbalancer]
ips = 192.168.0.100
```

Comma separate several. Apply with `zulip-puppet-apply` and restart. This makes nginx accept `X-Forwarded-For` only from those addresses, giving correct client IPs in logs and notification emails.

With `http_only` on, an untrusted or missing `X-Forwarded-Proto` produces infinite redirects, so configure the trust step correctly. Docker deployments use the `LOADBALANCER_IPS` and `TRUST_GATEWAY_IP` mechanism instead.

## Checked

2026-11-03: commands, paths, flags, settings and figures read against the Zulip documentation page production/reverse-proxies.html (zulip.readthedocs.io, latest). Removed: nothing.

Method: documentation only; no commands were run.
