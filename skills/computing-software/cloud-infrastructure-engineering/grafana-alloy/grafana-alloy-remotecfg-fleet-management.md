---
id: computing-software.cloud-infrastructure-engineering.grafana-alloy.grafana-alloy-remotecfg-fleet-management
name: grafana-alloy-remotecfg-fleet-management
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-alloy
tags: [remotecfg, alloy-remote-config, fleet-management, attributes, alloy-seedjson, bearer-token-file]
level: advanced
status: docs-checked
description: "The remotecfg block: poll a remote configuration API with id and attributes, auth options, poll_frequency minimum, and 401, 404, 415 troubleshooting."
sources: ["https://github.com/grafana/alloy/blob/main/docs/sources/reference/config-blocks/remotecfg.md", "https://github.com/grafana/alloy/blob/main/docs/sources/configure/load-remote-configuration.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# remotecfg for remote configuration

`remotecfg` (unlabeled, once per config file) polls a server implementing the alloy-remote-config API. The collector sends its `id` and `attributes`, and the server decides what configuration to return. It is not for static files; use `import.http` for those.

```alloy
remotecfg {
  url            = "SERVICE_URL"
  id             = constants.hostname
  name           = "edge-collector-1"
  attributes     = {"cluster" = "dev", "namespace" = "otlp-dev"}
  poll_frequency = "5m"
  basic_auth {
    username      = "USERNAME"
    password_file = "PASSWORD_FILE"
  }
}
```

## Arguments
- `url`: without it the block has no effect.
- `poll_frequency`: default `1m`, minimum `10s`.
- `id`: if unset, Alloy generates a UUID and persists it in `alloy_seed.json` under the storage path.
- `attributes`: custom map; the `collector.` prefix is reserved for `collector.os` and `collector.version`.
- `name`: human-readable name.
- Auth, at most one of: `authorization`, `basic_auth`, `bearer_token_file`, `bearer_token`, `oauth2`; plus `tls_config`.
- Proxy: `proxy_url`, `no_proxy`, `proxy_from_environment`, `proxy_connect_header`. `enable_http2` and `follow_redirects` default `true`.

## Troubleshooting
- 401/403: check credentials.
- 404: the url is not an alloy-remote-config server (static HTTP servers cannot serve it).
- 415: the server returns an unexpected format or does not implement the API.
- Timeouts: check network, proxy and firewall.

## Checked
2026-11-04: confirmed against the remotecfg block reference and Load configuration from remote sources. Removed: the Fleet Management mention (not on the pages).
Method: documentation only; no commands were run.
