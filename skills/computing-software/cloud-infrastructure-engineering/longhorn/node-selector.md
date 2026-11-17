---
id: computing-software.cloud-infrastructure-engineering.longhorn.node-selector
name: node-selector
category: computing-software
field: cloud-infrastructure-engineering
product: longhorn
tags: [node-selector, system-managed-components, helm, labels, scheduling]
level: advanced
status: docs-checked
description: "Restrict Longhorn components to labelled nodes with Helm nodeSelector values and the system-managed-components-node-selector setting."
sources:
  - https://longhorn.io/docs/1.13.0/advanced-resources/deploy/node-selector/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: keep Longhorn off nodes it should not use, such as Windows nodes in a mixed cluster (available since v1.1.1).

Two component groups need selectors:
- User-deployed: Longhorn Manager, Driver, UI, Global Manager, Driver Deployer.
- System-managed: Instance Manager, Backing Image Manager, Share Manager, CSI Driver, Engine Image.

Install time:
- Helm values: `global.nodeSelector`, `longhornManager.nodeSelector`, `longhornGlobalManager.nodeSelector`, `longhornUI.nodeSelector`, `longhornDriver.nodeSelector`; per-component values override `global`. The page contradicts itself on the driver key: the install-time section says `longhornDriver.nodeSelector`, the after-install section says `longhornDriverDeployer.nodeSelector`; check the chart's values.yaml.
- Rancher: Edit as YAML, `global: nodeSelector: label-key1: "label-value1"`.
- kubectl: edit the node selector sections in the deployment YAML and apply.
- System-managed: the default setting `system-managed-components-node-selector`, for example `"label-key1:label-value1"`.

Changing after install restarts all Longhorn components, so Longhorn is briefly unavailable; do not operate it meanwhile.
1. Stop workloads and detach all Longhorn volumes.
2. Update user-deployed values (Helm: `helm upgrade`; kubectl: reapply).
3. Set Settings, System Managed Components Node Selector in the UI.
4. If the new selector excludes nodes where Longhorn runs, they become `down`; verify no replicas remain, disable scheduling and delete them in the UI.

If volumes remain attached, the setting reaches the Instance Manager only when no engine or replica instances run; reconfigure after detaching or wait for the next sync (about one hour).

## Checked

2026-11-04: read the source page(s) in full against every claim above: https://longhorn.io/docs/1.13.0/advanced-resources/deploy/node-selector/

Added page conflict: install-time section says longhornDriver.nodeSelector, after-install section says longhornDriverDeployer.nodeSelector.

Method: documentation only; no commands were run.
