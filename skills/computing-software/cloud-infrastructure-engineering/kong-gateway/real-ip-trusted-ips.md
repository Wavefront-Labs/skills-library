---
id: computing-software.cloud-infrastructure-engineering.kong-gateway.real-ip-trusted-ips
name: real-ip-trusted-ips
category: computing-software
field: cloud-infrastructure-engineering
product: kong-gateway
tags: [kong-gateway, kong, real-ip-header, trusted-ips, real-ip-recursive, kong-conf, client-ip]
level: practitioner
status: docs-checked
description: "Make Kong see the real client IP behind a load balancer with real_ip_header, real_ip_recursive and trusted_ips CIDR ranges in kong.conf."
sources:
  - https://raw.githubusercontent.com/Kong/kong/master/kong.conf.default
  - https://developer.konghq.com/plugins/request-transformer/
  - https://developer.konghq.com/plugins/rate-limiting/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# real_ip_header and trusted_ips

| Setting | Default | Meaning |
|---|---|---|
| `real_ip_header` | `X-Real-IP` | header used to determine the client address |
| `real_ip_recursive` | `off` | sets the Nginx `ngx_http_realip_module` directive of the same name |
| `trusted_ips` | empty | CIDR blocks whose `X-Forwarded-*` headers Kong trusts |

`trusted_ips` lists the IP blocks known to send correct `X-Forwarded-*` headers; the default is empty. Requests from trusted IPs make Kong forward their `X-Forwarded-*` headers upstream, while other requests make Kong insert its own. It also sets the Nginx `set_real_ip_from` directives, takes a comma-separated list of CIDR blocks, and `0.0.0.0/0,::/0` trusts all IPs. The special value `unix:` trusts all UNIX-domain sockets.

`real_ip_header` names the request header whose value replaces the client address; if it is `proxy_protocol`, at least one `proxy_listen` entry needs the `proxy_protocol` flag.

The rate-limiting plugin extracts the client IP from headers sent by downstream clients, typically `X-Real-IP` or `X-Forwarded-For`, when limiting by IP.

Note the request-transformer plugin cannot overwrite `X-Forwarded-*` headers.

## Checked

2026-11-04. Confirmed against kong.conf.default (all three settings, defaults, `trusted_ips` behaviour and special values, `proxy_protocol` rule), the Rate Limiting page (IP extraction) and the Request Transformer page (`X-Forwarded-*` limitation). Removed the load balancer set-up advice and the ip-restriction and logs claim, which these pages do not state.
Method: documentation only; no commands were run.
