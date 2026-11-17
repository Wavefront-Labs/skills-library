---
id: computing-software.cloud-infrastructure-engineering.longhorn.priority-class
name: priority-class
category: computing-software
field: cloud-infrastructure-engineering
product: longhorn
tags: [priority-class, longhorn-critical, setting, preemption, restart]
level: practitioner
status: docs-checked
description: "Set the Longhorn priority-class setting, default longhorn-critical, and the effects, ordering and warnings when changing or removing it."
sources:
  - https://longhorn.io/docs/1.13.0/advanced-resources/deploy/priority-class/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: give Longhorn pods a Kubernetes Priority Class.

Setting: `priority-class` (UI: Settings, Priority Class). If not configured, Longhorn creates and uses the `longhorn-critical` Priority Class for user-deployed and system-managed components. Available since v1.0.1.

Install time:
1. System-managed components: set `priority-class` through the customizing default settings procedure.
2. User-deployed components (Manager, Driver, UI): modify the Helm chart or deployment YAML. The page lists no Helm keys.

After install:
1. System-managed: change it in the UI.
2. User-deployed: modify the Helm chart or deployment YAML.

Effects of a change:
- Changing or removing it recreates all Longhorn system components; Longhorn is briefly unavailable.
- Stop workloads and detach all volumes first.
- With all volumes detached it applies immediately to system-managed components; otherwise to the Instance Manager only once no engine or replica instances run. Reconfigure later or wait for the next sync (about one hour).
- The setting rejects values that appear to be invalid Priority Classes.
- Do not delete a Priority Class Longhorn is using; new workloads may fail to start.

If Longhorn will not start because the class does not exist, check with `kubectl -n longhorn-system describe daemonset.apps/longhorn-manager`; the remedy is to uninstall and reinstall Longhorn.

## Checked

2026-11-04: read the source page(s) in full against every claim above: https://longhorn.io/docs/1.13.0/advanced-resources/deploy/priority-class/

No claim needed changing.

Method: documentation only; no commands were run.
