---
id: computing-software.cloud-infrastructure-engineering.keda.cluster-http-client-settings
name: cluster-http-client-settings
category: computing-software
field: cloud-infrastructure-engineering
product: keda
tags: [keda-http-default-timeout, keda-http-disable-keep-alive, http-proxy, https-proxy, no-proxy, keda-http-min-tls-version]
level: advanced
status: docs-checked
description: "Set HTTP timeout, keep-alive, proxy and minimum TLS version for all KEDA scalers using operator and metrics server environment variables."
sources:
  - https://keda.sh/docs/2.17/operate/cluster/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
These settings apply to all scalers that issue HTTP requests to external servers, such as cloud services.
Scalers that call external servers each use their own HTTP client and connection pool. Global behaviour is set through environment variables:

- Timeout: each client times out after 3 seconds by default. Set `KEDA_HTTP_DEFAULT_TIMEOUT` on the operator deployment, in milliseconds. Some scalers allow a `timeout` parameter in trigger metadata that overrides the global value.
- Keep-alive: enabled by default, which may accumulate many connections (one per scaler). Add `KEDA_HTTP_DISABLE_KEEP_ALIVE: true` to both the Operator and Metrics Server deployments. It is global; per-scaler keep-alive is unsupported.
- Proxies: add `HTTP_PROXY`, `HTTPS_PROXY`, `NO_PROXY` and similar variables to both the Operator and Metrics Server:

```yaml
- env:
    HTTP_PROXY: http://proxy.server:port
    HTTPS_PROXY: http://proxy.server:port
    NO_PROXY: 10.0.0.0/8
```

- Minimum TLS version: default is TLS 1.2, the lowest version the page considers free of known vulnerabilities. Override with `KEDA_HTTP_MIN_TLS_VERSION`, allowed values `TLS13`, `TLS12`, `TLS11`, `TLS10`.

Example: `KEDA_HTTP_MIN_TLS_VERSION: TLS13`.

## Checked

2026-11-03. Confirmed on the 2.17 Operate Cluster page: 3 second default timeout and KEDA_HTTP_DEFAULT_TIMEOUT, keep-alive, proxy variables, KEDA_HTTP_MIN_TLS_VERSION values.

Method: documentation only; no commands were run.
