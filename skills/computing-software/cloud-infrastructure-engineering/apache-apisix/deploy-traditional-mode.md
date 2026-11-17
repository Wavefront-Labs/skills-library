---
id: computing-software.cloud-infrastructure-engineering.apache-apisix.deploy-traditional-mode
name: deploy-traditional-mode
category: computing-software
field: cloud-infrastructure-engineering
product: apache-apisix
tags: [apache-apisix, apisix, deployment-modes, traditional, etcd, config-provider, admin-listen]
level: intro
status: docs-checked
description: "Run APISIX in traditional deployment mode with etcd: role traditional, config_provider etcd, ports 9080 and 9180, and the etcd host, prefix and timeout settings."
sources:
  - https://raw.githubusercontent.com/apache/apisix/master/docs/en/latest/deployment-modes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Traditional deployment mode

Data plane and control plane run in the same instance, with etcd as the config store.

```yaml
apisix:
  node_listen:
    - port: 9080
deployment:
  role: traditional
  role_traditional:
    config_provider: etcd
  admin:
    admin_listen:
      port: 9180
  etcd:
    host:
      - http://${etcd_IP}:${etcd_Port}
    prefix: /apisix
    timeout: 30
```

Result:
- User traffic is served on 9080.
- The Admin API is served on 9180.
- The page's mode table says the `enable_admin` attribute should be disabled manually in this mode.

Use the decoupled mode instead when data and control planes should run on separate instances.

## Checked

2026-11-04: read the Deployment Modes page (traditional section and mode table); the config block, ports 9080 and 9180 and etcd prefix and timeout match. Reworded the enable_admin line to what the page states.

Method: documentation only; no commands were run.
