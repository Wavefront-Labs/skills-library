---
id: computing-software.cloud-infrastructure-engineering.alertmanager.http-config-auth
name: http-config-auth
category: computing-software
field: cloud-infrastructure-engineering
product: alertmanager
tags: [alertmanager, http-config, basic-auth, authorization-header, proxy]
level: advanced
status: docs-checked
description: "The shared http_config for Alertmanager receivers: basic_auth, authorization, headers, proxy options, redirects and HTTP/2."
sources: ["https://prometheus.io/docs/alerting/latest/configuration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# http_config for HTTP-based receivers

`http_config` configures the HTTP client used to reach API services. It can be set globally (`global.http_config`) and overridden per integration.

```yaml
http_config:
  basic_auth:
    username: user
    password_file: /path/to/password
  follow_redirects: true
  enable_http2: true
  proxy_url: http://proxy.example.org:3128
```

Fields:
- `basic_auth` (`username`, `password`, `password_file`) and `authorization` are mutually exclusive. `password` and `password_file` are mutually exclusive.
- `authorization`: `type` defaults to `Bearer`; `credentials` or `credentials_file` (mutually exclusive).
- `oauth2`: cannot be combined with `basic_auth` or `authorization`.
- `enable_http2`: default `true`.
- `proxy_url`; `no_proxy` (comma-separated IPs, CIDRs, domain names, optionally with ports); `proxy_from_environment` (default `false`, uses `HTTP_PROXY` and similar variables); `proxy_connect_header` for headers sent during CONNECT.
- `follow_redirects`: default `true`.
- `tls_config`: the shared TLS settings block.
- `http_headers`: custom headers per request. Each header name maps to `values`, `secrets` (hidden in the configuration page) or `files`. Headers set by the client itself cannot be overwritten.

Some integrations require auth through this block: Webex uses it for the bot token, and Jira for the personal access token.

## Checked

2026-11-03. Confirmed against the Alertmanager Configuration page (prometheus.io/docs/alerting/latest/configuration): http_config, http_header, oauth2 fields and defaults, Webex and Jira auth notes. Removed: reference to another skill.

Method: documentation only; no commands were run.
