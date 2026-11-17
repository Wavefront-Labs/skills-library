---
id: computing-software.cloud-infrastructure-engineering.apache-apisix.deploy-decoupled-mode
name: deploy-decoupled-mode
category: computing-software
field: cloud-infrastructure-engineering
product: apache-apisix
tags: [apache-apisix, apisix, deployment-modes, decoupled, data-plane, control-plane, etcd]
level: practitioner
status: docs-checked
description: "Split APISIX into data_plane and control_plane instances sharing etcd: the role and role_* config_provider blocks for each side and which ports they serve."
sources:
  - https://raw.githubusercontent.com/apache/apisix/master/docs/en/latest/deployment-modes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Decoupled deployment mode

Data plane (handles user requests only):

```yaml
deployment:
  role: data_plane
  role_data_plane:
    config_provider: etcd
  etcd:
    host:
      - https://${etcd_IP}:${etcd_Port}
```

Control plane (serves the Admin API on 9180):

```yaml
deployment:
  role: control_plane
  role_control_plane:
    config_provider: etcd
  etcd:
    host:
      - https://${etcd_IP}:${etcd_Port}
    prefix: /apisix
    timeout: 30
```

In the decoupled mode the data plane and control plane instances are deployed independently. Each role lists the etcd hosts it uses.

## Checked

2026-11-04: read the Deployment Modes page; both YAML blocks, the 9180 Admin API port and the etcd prefix and timeout match. Removed the unstated claim that both roles share one etcd cluster and that configuration reaches the data plane via etcd.

Method: documentation only; no commands were run.
