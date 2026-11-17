---
id: computing-software.networking-hardware-and-wireless.caddy.client-ip-remote-ip-not
name: client-ip-remote-ip-not
category: computing-software
field: networking-hardware-and-wireless
product: caddy
tags: [client-ip, remote-ip, private-ranges, trusted-proxies, not-matcher, cidr, caddyfile]
level: practitioner
status: docs-checked
description: "Restrict by network with client_ip and remote_ip, the private_ranges shortcut, trusted_proxies dependence and inverting with the not matcher."
sources:
  - https://caddyserver.com/docs/caddyfile/matchers
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: allow or block by address.

`remote_ip <ranges...>` matches the immediate peer (or the address set via PROXY protocol). `client_ip <ranges...>` matches the real client IP; it only differs from remote_ip when the `trusted_proxies` global option is configured, because only requests from trusted proxies have their client IP parsed from headers. Both accept exact IPs or CIDRs, support IPv6 zones, and merge multiple matchers by OR. `private_ranges` expands to `192.168.0.0/16 172.16.0.0/12 10.0.0.0/8 127.0.0.1/8 fd00::/8 ::1`. CEL forms: `client_ip('12.23.34.45', '23.34.45.56')`, `remote_ip(...)`.

`not <matcher>` negates one matcher; `not { <matchers...> }` negates the AND of several. `@not-assets { not path /css/* /js/* }` matches paths under neither prefix. Two separate `not` lines mean "neither": `not path /api/*` and `not method POST`. One `not` block with both means "not both". CEL uses `!`, e.g. `!(path('/api*') || method('POST'))`.

Private-network-only site: `@denied not client_ip private_ranges`, `abort @denied`, `respond "Hello, you must be from a private network!"`. The same example with `remote_ip` works without trusted proxies. The `abort` directive closes the connection without a response.

## Checked

2026-11-03: read caddyfile/matchers against this skill. Confirmed: remote_ip and client_ip semantics with trusted_proxies, private_ranges expansion, not forms, CEL forms and the private-network abort example.
Removed: nothing; no claim failed the check.
Method: documentation only; no commands were run.
