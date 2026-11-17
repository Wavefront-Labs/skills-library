---
id: computing-software.cloud-infrastructure-engineering.graylog.http-proxy-configuration
name: http-proxy-configuration
category: computing-software
field: cloud-infrastructure-engineering
product: graylog
tags: [http-proxy, non-proxy-hosts, server-conf, proxy-tls]
level: practitioner
status: docs-checked
description: "Route Graylog outbound traffic through an HTTP proxy with http_proxy_uri and exclude MongoDB and OpenSearch via http_non_proxy_hosts."
sources:
  - https://go2docs.graylog.org/current/setting_up_graylog/configure_graylog_to_use_an_http_proxy.htm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# http proxy configuration

In `/etc/graylog/server/server.conf` (or the container equivalent):

```
http_proxy_uri = https://hostname.domain.tld:3129
http_non_proxy_hosts = 192.168.*,*.domain.tld,127.*
```

- `http_proxy_uri`: full URI of the proxy.
- `http_non_proxy_hosts`: comma-separated host or domain patterns that bypass the proxy. This is critical for internal traffic such as MongoDB and OpenSearch connections. If internal services are addressed by hostname, include those patterns too.

Only one `*` is allowed per entry: `192.168.*` is valid, `192.168.*.*` is not. Restart graylog-server after changing these settings.

If the proxy uses HTTPS with a private or internally issued certificate, Graylog must trust its CA; see the TLS guide for the truststore setup.

Requirements: administrative access to the host and permission to edit configuration.

## Checked

2026-11-04. Confirmed against the HTTP proxy page. Added the single-wildcard rule and the restart requirement.

Method: documentation only; no commands were run.
