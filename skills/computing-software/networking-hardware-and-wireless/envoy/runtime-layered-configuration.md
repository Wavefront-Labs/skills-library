---
id: computing-software.networking-hardware-and-wireless.envoy.runtime-layered-configuration
name: runtime-layered-configuration
category: computing-software
field: networking-hardware-and-wireless
product: envoy
tags: [networking-hardware-and-wireless, envoy, runtime, layered-runtime, rtds, disk-layer, admin-layer, runtime-modify, feature-flags]
level: practitioner
status: docs-checked
description: "Define Envoy layered runtime (static, disk, RTDS, admin layers), override keys, and use runtime guards to kill risky new behaviour without a redeploy."
sources:
  - https://github.com/envoyproxy/envoy/blob/main/docs/root/configuration/operations/runtime.rst
  - https://github.com/envoyproxy/envoy/blob/main/docs/root/intro/arch_overview/operations/runtime.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# runtime layered configuration
Runtime is a virtual filesystem of reloadable settings, assembled from layers where later layers override earlier ones. Bootstrap `layered_runtime`:

```yaml
layered_runtime:
  layers:
  - name: static_layer_0
    static_layer:
      health_check: { min_interval: 5 }
  - name: disk_layer_0
    disk_layer: { symlink_root: /srv/runtime/current, subdirectory: envoy }
  - name: disk_layer_1
    disk_layer: { symlink_root: /srv/runtime/current, subdirectory: envoy_override, append_service_cluster: true }
  - name: admin_layer_0
    admin_layer: {}
```
Layer types in the docs: static bootstrap, local disk (a symlink swap triggers reload), RTDS (runtime discovery service), and the admin layer, modifiable with `POST /runtime_modify?key=value` and inspected with `GET /runtime`. Do not rely on the deprecated implicit layering.

Uses: feature percentages (`runtime_fraction`), circuit breaker overrides, and runtime guards. New or risky behaviour ships behind a temporary guard named in the release notes, for example `envoy.reloadable_features.*`; keep an RTDS or disk layer ready so a guard can be flipped without reverting the binary.

Gotchas: if a non-empty `layered_runtime` has no `admin_layer`, mutating admin actions get a 503; a symlink swap on a disk layer triggers a reload. Verify with `curl localhost:9901/runtime`.

## Checked

2026-11-03. Confirmed against: runtime.rst, admin.rst (/runtime, /runtime_modify, 503 without admin layer) and bootstrap.proto (layered_runtime). Removed or corrected: the not-persisted-on-restart claim.

Method: documentation only; no commands were run.
