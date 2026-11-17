---
id: computing-software.cloud-infrastructure-engineering.contour.contour-serve-flags-and-precedence
name: contour-serve-flags-and-precedence
category: computing-software
field: cloud-infrastructure-engineering
product: contour
tags: [serve-flags, config-path, precedence, leader-election, root-namespaces, watch-namespaces, ingress-class-name, disable-feature]
level: practitioner
status: docs-checked
description: "contour serve flags: config-path, namespace restriction, ingress class, leader election, disable-feature, and precedence between flags, env vars and the config file."
sources: ["https://github.com/projectcontour/contour/blob/main/site/content/docs/main/configuration.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Contour serve flags and configuration precedence

`contour serve` watches Kubernetes resources and streams Envoy config over xDS gRPC. Precedence: the config file is overridden by environment variables, which are overridden by CLI flags.

Common flags:
- `--config-path` base config file (normally a ConfigMap mounted into the pod); `--contour-config-name` selects a ContourConfiguration resource instead.
- `--xds-address` / `--xds-port` xDS gRPC listener; `--insecure` allows serving without TLS.
- `--contour-cafile`, `--contour-cert-file`, `--contour-key-file` secure the xDS gRPC with TLS (env `CONTOUR_CAFILE` etc).
- `--root-namespaces=ns,ns` limits where root HTTPProxies are accepted; `--watch-namespaces=ns,ns` limits all watched resources.
- `--ingress-class-name=a,b` comma-separated list of IngressClass names to serve.
- `--disable-feature=extensionservices|tlsroutes|grpcroutes` skips informers for those resources; repeat the flag for several.
- `--disable-leader-election` plus `--leader-election-lease-duration`, `--leader-election-renew-deadline`, `--leader-election-retry-period`, `--leader-election-resource-name`, `--leader-election-resource-namespace` tune the Lease used for election.
- `--use-proxy-protocol` enables PROXY protocol on all listeners.
- Observability: `-d/--debug`, `--log-format=text|json`, `--http-port` (metrics), `--health-port`, `--debug-http-port`, `--stats-port`.
- `--kubernetes-client-qps` and `--kubernetes-client-burst` throttle the API client.

The `CONTOUR_NAMESPACE` env var (set through the Downward API in the example manifests) supplies defaults for `contour bootstrap --namespace`, `certgen --namespace`, `serve --envoy-service-namespace` and `--leader-election-resource-namespace`.

## Checked

2026-11-04. Confirmed against the Contour Configuration Reference (configuration.md): the fields, defaults, flags and behaviours stated above. Removed: nothing.

Method: documentation only; no commands were run.
