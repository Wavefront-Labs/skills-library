---
id: computing-software.cloud-infrastructure-engineering.datadog.agent-proxy
name: agent-proxy
category: computing-software
field: cloud-infrastructure-engineering
product: datadog
tags: [datadog, agent-proxy, http-proxy, firewall, intake-endpoints]
level: practitioner
status: docs-checked
description: "Configure the Agent to reach Datadog through an HTTP(S) proxy and know which outbound destinations, ports and IP ranges to allow."
sources: ["https://docs.datadoghq.com/agent/configuration/proxy/", "https://docs.datadoghq.com/agent/configuration/network/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Agent behind a proxy or firewall
Goal: send data from restricted networks.

```yaml
# datadog.yaml (restart the Agent afterwards)
proxy:
  http: http://<USER>:<PASSWORD>@<PROXY_HOST>:<PROXY_PORT>
  https: http://<USER>:<PASSWORD>@<PROXY_HOST>:<PROXY_PORT>
  no_proxy:
    - <HOST_TO_BYPASS_1>
    - <HOST_TO_BYPASS_2>
no_proxy_nonexact_match: true
logs_config:
  force_use_http: true
```

```bash
# Environment variables (override the config file; no_proxy is space separated)
DD_PROXY_HTTP="http://<USER>:<PASSWORD>@<PROXY_HOST>:<PROXY_PORT>"
DD_PROXY_HTTPS="http://<USER>:<PASSWORD>@<PROXY_HOST>:<PROXY_PORT>"
DD_PROXY_NO_PROXY="<HOST_TO_BYPASS_1> <HOST_TO_BYPASS_2>"
DD_NO_PROXY_NONEXACT_MATCH=true
```

- Username and password are optional. Most Datadog traffic uses HTTPS. On Kubernetes the proxy can also be set through Helm or the Datadog Operator.
- By default `no_proxy` must match endpoints exactly; the docs recommend `no_proxy_nonexact_match: true` so it uses the same matching rules as Agent integrations. `no_proxy` entries can be hosts or CIDR ranges.
- The docs recommend `logs_config.force_use_http: true` when logs are enabled and a proxy is in use.
- Traffic is always initiated by the Agent and sent over SSL. Most Agent data uses outbound TCP 443.
- Destinations depend on your Datadog site. Allow `*.agent.<DD_SITE>` in the firewall; those domains are CNAMEs to static IPs listed at `https://ip-ranges.<DD_SITE>` (separate JSON files exist per product, for example `logs.json` and `apm.json`); allow all ranges listed, since only a subset is active at a time.
- Installation needs `install.datadoghq.com`, `yum.datadoghq.com`, `keys.datadoghq.com`, `apt.datadoghq.com` and `windows-agent.datadoghq.com` reachable.

```
sudo datadog-agent diagnose
```

## Verify
- `diagnose` reports connectivity success, and the Forwarder section of `datadog-agent status` shows no growing Errors.

## Checked
2026-11-03. Confirmed against the Agent Proxy and Agent Network Traffic pages. Removed: `skip_ssl_validation` and TLS-inspection CA advice, the legacy TCP logs port 10516 and the logs intake hostname (not found on the pages read), the `no_proxy: 169.254.169.254` example, and the `status | grep` pipeline.
Method: documentation only; no commands were run.
