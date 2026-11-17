---
id: computing-software.collaboration-platform-administration.zulip.zulip-conf-network-proxy-gateway
name: zulip-conf-network-proxy-gateway
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [loadbalancer, http-proxy-settings, rejects-http-requests, email-gateway-listen]
level: advanced
status: docs-checked
description: "Reference for the zulip.conf [loadbalancer], [http_proxy], [email_gateway], [sentry] sections: ips, rejects_http_requests, allow/deny ranges and gateway listen address."
sources: ["https://zulip.readthedocs.io/en/latest/production/system-configuration.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Network-related zulip.conf sections

`[loadbalancer]`

- `ips`: comma-separated addresses or CIDR ranges of load balancers whose `X-Forwarded-For` and `X-Forwarded-Proto` headers Zulip honours.
- `rejects_http_requests`: treat requests from those IPs with no `X-Forwarded-Proto` as HTTPS. This is a security vulnerability unless the load balancer itself rejects unencrypted HTTP or answers it with 301. Zulip's HSTS headers do not help here, because API clients ignore them, so the balancer must never forward unencrypted requests.

`[http_proxy]` (Smokescreen and outgoing proxy)

- `host`: defaults to `localhost`.
- `port`: defaults to 4750.
- `listen_address`: where Smokescreen binds, default `127.0.0.1`.
- `enable_for_camo`: Camo normally needs no proxy because it denies private subnets; by default it uses the proxy only if it is not the local Smokescreen. Override with true or false.
- `allow_addresses`, `allow_ranges`, `deny_addresses`, `deny_ranges`: comma-separated IPs or CIDR rules. Private addresses such as 127.0.0.0/8 and 192.168.0.0/16 are denied by default, and allow rules override deny rules.

`[sentry]`: `organization` and `project` for the Sentry deploy hook.

`[email_gateway]`

- `listen`: bind address for the incoming email gateway's SMTP server, as a bare port or `address:port`, with IPv6 in brackets such as `[2001:db8::1]:25`. Default is port 25 on all IPv4 and IPv6 addresses. Applies to local delivery only, not polling.

Changes to `zulip.conf` generally take effect after running `zulip-puppet-apply` as root.

## Checked

2026-11-08. Checked: settings and defaults read against the Zulip system-configuration page (docs/production/system-configuration.md, read in full). Reworded the apply-changes line to match the page's 'generally take effect' wording.

Method: documentation only; no commands were run.
