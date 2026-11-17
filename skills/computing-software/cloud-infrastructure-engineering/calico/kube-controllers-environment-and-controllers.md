---
id: computing-software.cloud-infrastructure-engineering.calico.kube-controllers-environment-and-controllers
name: kube-controllers-environment-and-controllers
category: computing-software
field: cloud-infrastructure-engineering
product: calico
tags: [kube-controllers, node-controller, policy-controller, enabled-controllers, host-endpoints, environment-variables]
level: practitioner
status: docs-checked
description: "Configure calico-kube-controllers: the five controllers, ENABLED_CONTROLLERS defaults, which ones apply to which datastore, AUTO_HOST_ENDPOINTS and SYNC_NODE_LABELS."
sources:
  - https://docs.tigera.io/calico/latest/reference/kube-controllers/configuration
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`calico-kube-controllers` runs five controllers in one pod: policy, namespace, serviceaccount, workloadendpoint and node. With the operator, configure it through the `KubeControllersConfiguration` resource; with manifests it is configured by environment variables, though the page prefers the API resource because some options are not available as variables.

| Variable | Default |
|---|---|
| `DATASTORE_TYPE` | `kubernetes` (or `etcdv3`) |
| `ENABLED_CONTROLLERS` | `policy,namespace,serviceaccount,workloadendpoint,node` |
| `LOG_LEVEL` | `info` |
| `SYNC_NODE_LABELS` | `true` |
| `AUTO_HOST_ENDPOINTS` | `disabled` |
| `COMPACTION_PERIOD` | `10m`, etcd compaction; `0` disables |

**Which controller works where.**

- Node controller: with either datastore it garbage collects IP addresses and can auto-provision host endpoints for Kubernetes nodes. With etcdv3 only, it also garbage collects v3 Node resources when the Kubernetes node is deleted and syncs labels (the Kubernetes value wins on conflict).
- Policy, workloadendpoint, namespace and serviceaccount controllers are valid only when etcd is the Calico datastore.
- The node controller is not on by default if `ENABLED_CONTROLLERS` is unset, but the Calico manifests set it explicitly.

**Enabling the node controller on etcdv3** takes two steps: add `node` to the enabled controllers, and give the node daemon set a Kubernetes node reference:

```yaml
- name: CALICO_K8S_NODE_REF
  valueFrom:
    fieldRef:
      fieldPath: spec.nodeName
```

With the `kubernetes` datastore, just enable `node` (for example `ENABLED_CONTROLLERS=node`).

## Checked

2026-11-04. Variables, defaults, per-datastore controller behaviour and the YAML snippet were confirmed on the kube-controllers configuration page.

Method: documentation only; no commands were run.
