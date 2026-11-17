---
id: computing-software.cloud-infrastructure-engineering.longhorn.taint-toleration
name: taint-toleration
category: computing-software
field: cloud-infrastructure-engineering
product: longhorn
tags: [taints, tolerations, taint-toleration, helm, scheduling]
level: advanced
status: docs-checked
description: "Run Longhorn on tainted nodes: the taintToleration setting, Helm toleration keys per component and the detach-first procedure after install."
sources:
  - https://longhorn.io/docs/1.13.0/advanced-resources/deploy/taint-toleration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: let Longhorn components tolerate node taints.

Setting: `taintToleration` in `defaultSettings` at install time, or Settings, Kubernetes Taint Toleration in the UI afterwards. Example value `key=value:NoSchedule`.

User-deployed components use standard tolerations:

```yaml
tolerations:
- key: "key"
  operator: "Equal"
  value: "value"
  effect: "NoSchedule"
```

Helm keys (set before install, `helm upgrade` afterwards): `global.tolerations`, `longhornManager.tolerations`, `longhornGlobalManager.tolerations`, `longhornUI.tolerations`, `longhornDriver.tolerations`. Per-component keys override `global.tolerations`.

kubectl install: edit the tolerations section for Longhorn Manager, Longhorn Global Manager, Longhorn UI and Longhorn Driver Deployer in the deployment YAML and apply. Rancher: Edit as YAML and set `global.tolerations`.

After install:
1. Stop all workloads and detach all Longhorn volumes.
2. Update tolerations for user-deployed components (Helm, kubectl or Rancher).
3. Set `taintToleration` in the UI.

If volumes stay attached, the setting is applied to the Instance Manager only when no engines or replica instances are running; reconfigure after detaching the rest or wait for the next setting synchronization, which occurs in an hour. All components restart, so Longhorn is temporarily unavailable. A toleration does not stop a workload being scheduled onto nodes that have no matching taint.

## Checked

2026-11-08. Confirmed against: https://longhorn.io/docs/1.13.0/advanced-resources/deploy/taint-toleration/. The taintToleration default setting and example value, the UI settings path, the toleration YAML, the Helm keys and override rule, kubectl and Rancher instructions, the after-install warning and one-hour sync.

Removed or reworded: The remark about kubectl taint (not about the product).

Method: documentation only; no commands were run.
