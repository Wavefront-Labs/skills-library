---
id: computing-software.cloud-infrastructure-engineering.grafana-mimir.grafana-mimir-reverse-proxy-ip-logging
name: grafana-mimir-reverse-proxy-ip-logging
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-mimir
tags: [reverse-proxy, ip-logging, x-forwarded-for, troubleshooting, logging]
level: intro
status: docs-checked
description: "Lists the Mimir server flags that log source IP addresses passed by a reverse proxy in headers such as X-Forwarded-For."
sources: ["https://grafana.com/docs/mimir/latest/configure/about-ip-address-logging/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Source IP logging behind a reverse proxy

When a reverse proxy fronts Mimir, error troubleshooting is harder because the connection IP is the proxy. These flags log the IP carried in forwarding headers.

- `-server.log-source-ips-enabled`: set `true` to add a `sourceIPs` field to error logs when data is pushed. Used when a `Forwarded`, `X-Real-IP` or `X-Forwarded-For` header is present.
- `-server.log-source-ips-header`: the header holding the source IPs. Used only when logging is enabled and a regex is set. If unset, the default headers listed above are used.
- `-server.log-source-ips-regex`: a regular expression matching the source IPs. It must contain at least one capturing group; the first is returned. Used only when logging is enabled.
- `-server.log-source-ips-full`: set `true` to log all source IPs listed in the headers, not only the originating one.

Example flags:

```text
-server.log-source-ips-enabled=true
-server.log-source-ips-full=true
```

Trust only headers your proxy sets; clients can forge forwarding headers if the proxy passes them through.

## Checked

Confirmed against the page: the four `-server.log-source-ips-*` flags, the `sourceIPs` field, default headers, regex capturing-group rule. The closing forged-header caution is general advice, not from the page.

Method: docs-checked 2026-11-09 against the raw markdown of the Mimir about-ip-address-logging page (grafana/mimir main), read in full.
