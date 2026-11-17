---
id: computing-software.cloud-infrastructure-engineering.contour.contour-global-header-policy-config
name: contour-global-header-policy-config
category: computing-software
field: cloud-infrastructure-engineering
product: contour
tags: [policy-config, request-headers, response-headers, applytoingress, header-policy, envoy-variables]
level: practitioner
status: docs-checked
description: "Contour config policy block: default request and response header set/remove across all routes, applyToIngress, and Envoy variable placeholders."
sources: ["https://github.com/projectcontour/contour/blob/main/site/content/docs/main/configuration.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Contour global header policy

The config file `policy` block sets default headers on every service route unless an HTTPProxy overrides them.

```yaml
policy:
  request-headers:
    set:
      X-Envoy-Hostname: "%HOSTNAME%"
      l5d-dst-override: "%CONTOUR_SERVICE_NAME%.%CONTOUR_NAMESPACE%.svc.cluster.local:%CONTOUR_SERVICE_PORT%"
    remove: [X-Debug]
  response-headers:
    set:
      X-Envoy-Response-Flags: "%RESPONSE_FLAGS%"
  applyToIngress: true
```

- `set` is a map of header to value; it creates the header but does not overwrite an existing value.
- `remove` is a list of header names to strip.
- `applyToIngress` (default false) decides whether the policy also applies to Ingress objects, not just HTTPProxy.
- HTTPProxy objects may override the value of a `set` or `remove` entry, but cannot delete the global entry itself.
- The reference example uses the placeholders `%HOSTNAME%`, `%RESPONSE_FLAGS%`, `%CONTOUR_SERVICE_NAME%`, `%CONTOUR_NAMESPACE%` and `%CONTOUR_SERVICE_PORT%` in these values.

Use it for cross-cutting needs such as service-mesh routing hints (the Linkerd `l5d-dst-override` example) or exposing Envoy response flags to clients while debugging.

## Checked

2026-11-08: read the Contour docs configuration (Policy Configuration, HeaderPolicy and the configuration example). Confirmed: request-headers and response-headers with set and remove, applyToIngress default false, set not overwriting an existing header, HTTPProxy overriding but not removing entries, and the example placeholders. Removed: the claim about when placeholders are expanded.

Method: documentation only; no commands were run.
