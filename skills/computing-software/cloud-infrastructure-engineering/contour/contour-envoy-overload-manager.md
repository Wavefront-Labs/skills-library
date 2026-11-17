---
id: computing-software.cloud-infrastructure-engineering.contour.contour-envoy-overload-manager
name: contour-envoy-overload-manager
category: computing-software
field: cloud-infrastructure-engineering
product: contour
tags: [overload-manager, overload-max-heap, shrink-heap, 503, envoy-overloaded, readiness, oom]
level: advanced
status: docs-checked
description: "Envoy overload manager in Contour: enabling with contour bootstrap --overload-max-heap, 95% shrink and 98% reject thresholds, 503 body, readiness side effects."
sources: ["https://github.com/projectcontour/contour/blob/main/site/content/docs/main/config/overload-manager.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Envoy overload manager

Without protection, Envoy is killed abruptly when it exhausts memory or hits the container limit. The overload manager caps heap use. It is off by default and is enabled in the Envoy pod's init container, `contour bootstrap`:

```
--overload-max-heap=2147483648
```
(2 GiB shown; choose per system.)

Once enabled, two actions apply:
- Shrink heap at 95% of the maximum heap size (tries to free unused memory).
- Stop accepting requests at 98%; clients get `503 Service Unavailable` with body `envoy overloaded`.

Side effects and risks:
- Envoy also denies the `/ready` and `/stats` endpoints, because Contour exposes only selected admin endpoints by proxying them. The readiness probe fails, removing the overloaded pod from Service endpoints until memory is freed.
- A max heap set too low can leave Envoy unable to free enough memory and never ready again.

The flag is passed to the `contour bootstrap` command, which runs in the init container of the Envoy pod and generates Envoy's initial configuration; edit the deployment manifest to add it.

## Checked

2026-11-08. Read the Contour main-branch config page overload-manager.md in full. Confirmed: default off, `--overload-max-heap` on `contour bootstrap`, the 2 GiB example, 95% shrink and 98% stop thresholds, the 503 and `envoy overloaded` body, the `/ready` and `/stats` side effect, and the too-low heap risk. Removed the unsourced `--overload-downstream-max-conn` and `omEnforcedHealthListener` notes and the memory limit advice.

Method: documentation only; no commands were run.
