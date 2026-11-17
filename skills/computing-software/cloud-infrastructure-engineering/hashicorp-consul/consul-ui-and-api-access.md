---
id: computing-software.cloud-infrastructure-engineering.hashicorp-consul.consul-ui-and-api-access
name: consul-ui-and-api-access
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-consul
tags: [consul, consul-ui, consul-api, ui-config]
level: practitioner
status: docs-checked
description: "Enable the Consul UI behind TLS and ACLs, and use API tokens in headers, not URLs."
sources: ["https://developer.hashicorp.com/consul/docs/agent/config/config-files", "https://developer.hashicorp.com/consul/docs/security/acl"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`ui_config.enabled` serves the web UI from the agent (default false).

```hcl
ui_config { enabled = true }
```

```sh
curl -s -H "X-Consul-Token: $CONSUL_HTTP_TOKEN" \
  https://consul.example.com:8501/v1/catalog/services
```

Gotchas: pass tokens in the `X-Consul-Token` header or the Bearer scheme of the `Authorization` header; the `token` query parameter is deprecated and will be removed. The UI is served at `/ui/` by default (`ui_config.content_path`). Blocking queries wait 5 minutes by default (maximum 10), which matters for proxy idle timeouts.

Verify: the authorised `curl` returns the service list.

## Checked

2026-11-03. Confirmed against the UI options page (ui_config.enabled default false, content_path default /ui/), the ACL token page and version-specific upgrade notes (X-Consul-Token header, Bearer scheme, token query parameter deprecated) and the Blocking Queries page (5 and 10 minute wait). Removed: the anonymous-token behaviour, the 403 check, the reverse-proxy and read-only token advice, which the pages do not state.

Method: documentation only; no commands were run.
