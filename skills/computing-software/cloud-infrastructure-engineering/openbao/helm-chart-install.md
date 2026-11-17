---
id: computing-software.cloud-infrastructure-engineering.openbao.helm-chart-install
name: helm-chart-install
category: computing-software
field: cloud-infrastructure-engineering
product: openbao
tags: [openbao, helm, kubernetes, standalone, dry-run]
level: intro
status: docs-checked
description: "Install OpenBao on Kubernetes with the Helm chart: default standalone mode, Helm 3.6+ requirement and --dry-run before changes."
sources:
  - https://raw.githubusercontent.com/openbao/openbao/main/website/content/docs/platform/k8s/helm/index.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Helm chart install

```
helm install openbao openbao/openbao
```

Installs the latest release with pods prefixed `openbao`.

## Modes

The chart runs **standalone** by default: one server with a file storage backend, described as less secure and less resilient.

## Requirements and warnings

- Helm 3.6+; the chart is not compatible with Helm 2.
- The chart is new and under significant development: always run Helm with `--dry-run` before any install or upgrade.
- Standalone is not suitable for production. Use a securely configured Kubernetes cluster, review the configuration options and follow the production deployment checklist.

## Next

After install, initialize and unseal as in operator-quickstart, then pick an auth method such as kubernetes-auth.

## Checked

2026-11-04. Confirmed against the Helm chart overview page: helm install openbao openbao/openbao, Helm 3.6+, not compatible with Helm 2, --dry-run advice, and the standalone mode warning. Removed a sentence about dev and HA modes and example pages that the page does not state.

Method: documentation only; no commands were run.
