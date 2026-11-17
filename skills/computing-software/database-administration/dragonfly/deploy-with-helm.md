---
id: computing-software.database-administration.dragonfly.deploy-with-helm
name: deploy-with-helm
category: computing-software
field: database-administration
product: dragonfly
tags: [helm, helm-chart, kubernetes, servicemonitor, dragonfly]
level: practitioner
status: docs-checked
description: "Deploy Dragonfly on Kubernetes with the official OCI Helm chart, add snapshot storage and enable kube-prometheus monitoring."
sources:
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/getting-started/kubernetes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Needs a running Kubernetes cluster and Helm. Set `VERSION` to the Dragonfly version you want (chosen from the releases page).

Standalone instance:

```bash
helm upgrade --install dragonfly oci://ghcr.io/dragonflydb/dragonfly/helm/dragonfly --version $VERSION
```

## Snapshotting

Add to a values file:

```yml
storage:
  enabled: true
  requests: 128Mi # PVC size
extraArgs:
  - --dbfilename=my-dump-{timestamp} # filename only, no extension
  - --snapshot_cron=* * * * *        # a valid cron schedule
```

Then deploy with `helm upgrade -f values.yaml --install ...`. The docs example also sets `podSecurityContext.fsGroup`, a restrictive `securityContext` (non-root, read-only root filesystem, drop all capabilities).

## Monitoring with kube-prometheus

If Kube-Prometheus is installed, enable `serviceMonitor` and `prometheusRule` in values. The docs sample adds an alert on `absent(dragonfly_uptime_in_seconds) == 1`.

The full list of chart values is in the repository under `contrib/charts/dragonfly`.

## Checked

2026-11-04: confirmed against the Install on Kubernetes with Helm Chart page (chart URL, values, security context, kube-prometheus sample, values path). No unconfirmed claims found.
Method: documentation only; no commands were run.
