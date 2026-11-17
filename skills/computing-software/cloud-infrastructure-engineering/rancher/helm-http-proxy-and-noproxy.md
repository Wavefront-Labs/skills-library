---
id: computing-software.cloud-infrastructure-engineering.rancher.helm-http-proxy-and-noproxy
name: helm-http-proxy-and-noproxy
category: computing-software
field: cloud-infrastructure-engineering
product: rancher
tags: [proxy, noproxy, https-proxy, extraenv, helm, secretkeyref]
level: advanced
status: docs-checked
description: "Configure Rancher behind an HTTP proxy: the proxy chart value, mandatory noProxy ranges, why extraEnv ignores noProxy, and keeping proxy credentials in a secret."
sources:
  - https://ranchermanager.docs.rancher.com/getting-started/installation-and-upgrade/installation-references/helm-chart-options
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Rancher needs internet access for some features, such as Helm charts. Point it at a proxy with the `proxy` chart value, or with `extraEnv` setting `HTTPS_PROXY`.

```plain
--set proxy="http://<proxy_url:proxy_port>/"
```

Exceptions go in the comma-separated `noProxy` value. The page says to make sure it includes the pod cluster IP range (default `10.42.0.0/16`), the service cluster IP range (default `10.43.0.0/16`), the internal cluster domains (default `.svc,.cluster.local`) and any worker cluster `controlplane` nodes. CIDR notation is supported.

A trap: **when you use `extraEnv`, the `noProxy` Helm option is ignored**, so `NO_PROXY` must also be set through `extraEnv`. Commas inside the value are escaped with a backslash on the `--set` line:

```plain
--set extraEnv[1].name=HTTPS_PROXY
--set extraEnv[1].value="http://<proxy_url>:<proxy_port>/"
--set extraEnv[2].name=NO_PROXY
--set extraEnv[2].value="127.0.0.0/8\,10.0.0.0/8\,172.16.0.0/12\,192.168.0.0/16\,.svc\,.cluster.local"
```

If the proxy URL contains credentials, do not put it in the chart value. Use `extraEnv` with `valueFrom.secretKeyRef.name` and `.key` so the secret is not exposed in Helm or the Rancher deployment; the page's example stores the URL under the key `https-proxy-url`.

If a TLS-intercepting proxy is in play, the chart's `additionalTrustedCAs` option covers its CA.

## Checked

2026-11-04. Checked against the Rancher Manager documentation pages: Rancher Helm Chart Options (HTTP Proxy, extraEnv, Additional Trusted CAs). Nothing removed.

Method: documentation only; no commands were run.
