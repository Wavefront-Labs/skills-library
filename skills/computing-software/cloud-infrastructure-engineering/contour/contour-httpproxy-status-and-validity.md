---
id: computing-software.cloud-infrastructure-engineering.contour.contour-httpproxy-status-and-validity
name: contour-httpproxy-status-and-validity
category: computing-software
field: cloud-infrastructure-engineering
product: contour
tags: [status, currentstatus, invalid, conditions, validation, 502, 503, kubectl]
level: practitioner
status: docs-checked
description: "Reading HTTPProxy status: valid/invalid currentStatus, common invalid causes, partial validity, and the 502 and 503 responses for missing includes or services."
sources: ["https://github.com/projectcontour/contour/blob/main/site/content/docs/main/config/fundamentals.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# HTTPProxy status and invalid configuration

Contour writes `status` on every HTTPProxy:

```yaml
status:
  currentStatus: valid
  description: valid HTTPProxy
```

Invalid objects show `currentStatus: invalid` with a `description`, e.g. `route '/foo': service 'home': weight must be greater than or equal to zero`. Inspect with `kubectl get httpproxy` and `kubectl describe httpproxy <name>`.

Contour processes valid parts of partly invalid config and ignores the invalid parts. Known invalid causes:
- negative weight; invalid service port.
- delegated prefix does not match the parent route's prefix.
- root created outside the allowed `--root-namespaces`.
- a route that both delegates and lists services.
- orphaned route; delegation cycle.
- root without `fqdn`.
- multiple prefixes in one set of conditions.
- several exact `header` conditions with the same key; contradictory header conditions such as `contains` plus `notcontains` on the same value.

Runtime effects for invalid routes: Envoy answers 502 Bad Gateway when an include refers to a nonexistent HTTPProxy, and 503 Service Unavailable when a route refers to a nonexistent Service. A proxy with one good route and one missing-service route reports `Valid=false` with `unresolved service reference: service "default/service-that-does-not-exist" not found`, yet the good route keeps serving.

HTTPProxy goals over Ingress: multi-team safety, cross-namespace inclusion, multiple weighted services per route, no annotations, creation-time validation.

## Checked

2026-11-08. Read the Contour main-branch config page fundamentals.md in full. Confirmed: the status block for valid and invalid objects, the negative weight example message, the list of invalid causes, partial processing of valid parts, the 502 and 503 responses, the missing-service example with `Valid=false`, the `kubectl` commands, and the listed HTTPProxy benefits. No claims removed.

Method: documentation only; no commands were run.
