---
id: computing-software.networking-hardware-and-wireless.envoy.xds-dynamic-configuration-overview
name: xds-dynamic-configuration-overview
category: computing-software
field: networking-hardware-and-wireless
product: envoy
tags: [networking-hardware-and-wireless, envoy, xds, cds, eds, rds, lds, sds, vhds, srds, dynamic-configuration, static-config]
level: practitioner
status: docs-checked
description: "Choose between fully static Envoy config and the xDS APIs (EDS, CDS, RDS, VHDS, SRDS, LDS, SDS) and know which changes need a hot restart."
sources:
  - https://github.com/envoyproxy/envoy/blob/main/docs/root/intro/arch_overview/operations/dynamic_configuration.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# xds dynamic configuration overview
Envoy supports a range of config-management styles. Fully static: listeners, filter chains and clusters are in the file; only DNS-based discovery is dynamic and config reloads use hot restart. Dynamic config is layered on incrementally through the xDS APIs, each served by a gRPC or REST management server:
- EDS: cluster endpoints. Preferred, because host add/remove leaves existing hosts untouched.
- CDS: whole clusters. A changed cluster definition is graceful but drains and reconnects all its connection pools, so keep endpoints in EDS.
- RDS: the whole route configuration of an HCM, swapped in without affecting in-flight requests.
- VHDS: virtual hosts fetched on demand when a route config has very many.
- SRDS: splits a route table into scoped pieces for massive route tables.
- LDS: whole listeners including filter stacks and HTTP filters with RDS references.
- SDS: certificates, keys, session ticket keys and validation context.

With everything dynamic, hot restart should be needed only for very rare changes (admin, tracing driver, etc.) and binary updates.

```yaml
dynamic_resources:
  cds_config:
    resource_api_version: V3
    api_config_source: { api_type: GRPC, transport_api_version: V3,
      grpc_services: [ { envoy_grpc: { cluster_name: xds_cluster } } ] }
```
Gotcha: the `xds_cluster` itself must be a static cluster. Verify with `GET /config_dump` (shows static and dynamic sections with `version_info`) and the `cluster_manager.cds.*` stats.

## Checked

2026-11-03. Confirmed against: dynamic_configuration.rst (EDS, CDS, RDS, VHDS, SRDS, LDS, SDS roles, hot restart note) and admin.rst (/config_dump). Removed or corrected: nothing.

Method: documentation only; no commands were run.
