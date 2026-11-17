---
id: computing-software.cloud-infrastructure-engineering.crossplane.pods-reconcile-tuning
name: pods-reconcile-tuning
category: computing-software
field: cloud-infrastructure-engineering
product: crossplane
tags: [crossplane-pod, poll-interval, sync-interval, max-reconcile-rate, realtime-compositions]
level: advanced
status: docs-checked
description: "Tune Crossplane reconcile behaviour with poll-interval, sync-interval, max-reconcile-rate, leader election and real-time compositions."
sources:
  - https://docs.crossplane.io/latest/guides/pods/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Two pods are installed in `crossplane-system`: `crossplane` and `crossplane-rbac-manager`. An init container installs the core CRDs and webhooks first. The core container reconciles only core resources such as XRs; providers reconcile their MRs.

Arguments (edit with `kubectl edit deployment crossplane --namespace crossplane-system`, under `args` after `core` and `start`; editing restarts the pod):

- `--poll-interval`: default one minute, for objects without a watch. Lower values add load and API calls; higher ones delay drift detection.
- `--sync-interval`: full recheck of all resources, default one hour, for example `--sync-interval=30m`.
- `--max-reconcile-rate`: reconciles per second, default 10; it also sets how many resources reconcile at once. Providers have their own setting.
- `--enable-realtime-compositions`: beta; watches every composed resource, so poll-interval is not used.
- `--leader-election`: required when running more than one Crossplane or RBAC manager pod; multiple pods without it are unsupported.

MRs watch Kubernetes events but rely on polling to detect external changes. Use the `crossplane.io/poll-interval` annotation for per-resource overrides.

Environment variables read at startup can change defaults too. Helm values can set the same options before install.

## Checked

Pod layout, argument defaults, real-time compositions, leader election and the poll-interval annotation confirmed on the Crossplane Pods page.

Method: docs-checked 2026-11-09 against the raw Crossplane Pods page (docs repo, current content folder), read in full.
