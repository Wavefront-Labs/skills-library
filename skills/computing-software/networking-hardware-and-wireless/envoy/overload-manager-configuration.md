---
id: computing-software.networking-hardware-and-wireless.envoy.overload-manager-configuration
name: overload-manager-configuration
category: computing-software
field: networking-hardware-and-wireless
product: envoy
tags: [networking-hardware-and-wireless, envoy, overload-manager, resource-monitors, fixed-heap, overload-actions, load-shed-points, stop-accepting-requests, cgroup-memory]
level: practitioner
status: docs-checked
description: "Protect an Envoy proxy from memory or CPU pressure with overload manager resource monitors, triggered actions and load shed points."
sources:
  - https://github.com/envoyproxy/envoy/blob/main/docs/root/configuration/operations/overload_manager/overload_manager.rst
  - https://github.com/envoyproxy/envoy/blob/main/docs/root/intro/arch_overview/operations/overload_manager.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# overload manager configuration
The overload manager protects the Envoy server itself (distinct from circuit breaking, which protects upstreams). It polls the pressure (0 to 1) of resources through resource monitors, feeds that through triggers, and takes actions. Configure in bootstrap `overload_manager`:

```yaml
overload_manager:
  refresh_interval: 0.25s
  resource_monitors:
  - name: envoy.resource_monitors.fixed_heap
    typed_config:
      "@type": type.googleapis.com/envoy.extensions.resource_monitors.fixed_heap.v3.FixedHeapConfig
      max_heap_size_bytes: 2147483648
  actions:
  - name: envoy.overload_actions.disable_http_keepalive
    triggers: [ { name: envoy.resource_monitors.fixed_heap, threshold: { value: 0.92 } } ]
  - name: envoy.overload_actions.stop_accepting_requests
    triggers: [ { name: envoy.resource_monitors.fixed_heap, threshold: { value: 0.95 } } ]
  loadshed_points:
  - name: envoy.load_shed_points.tcp_listener_accept
    triggers: [ { name: envoy.resource_monitors.fixed_heap, threshold: { value: 0.95 } } ]
```
This drains HTTP keepalives at 92 percent heap, rejects new requests at 95 and stops accepting TCP connections at 95. A cgroup memory monitor (`envoy.resource_monitors.cgroup_memory`, cgroup v1 or v2) reports usage over the cgroup limit; with no limit set (-1 in v1, `max` in v2) pressure is 0; `max_memory_bytes` can only lower the effective limit.

Gotcha: action names cannot duplicate load shed point names, because both emit stats under the `overload.<name>` prefix.

## Checked
2026-11-03. Confirmed against overload_manager.rst, including the full example configuration and the cgroup memory monitor text. Removed or corrected: the unsupported 'keep in sync' gotcha and the /stats verify step.
Method: documentation only; no commands were run.
