---
id: computing-software.cloud-infrastructure-engineering.rancher.helm-chart-common-and-advanced-options
name: helm-chart-common-and-advanced-options
category: computing-software
field: cloud-infrastructure-engineering
product: rancher
tags: [helm, values, replicas, antiaffinity, systemdefaultregistry, addlocal, extraenv]
level: advanced
status: docs-checked
description: "Reference for key Rancher chart values: hostname, tls source, replicas (-1 auto), antiAffinity, extraEnv, addLocal, systemDefaultRegistry, ingress.enabled and extraAnnotations."
sources:
  - https://ranchermanager.docs.rancher.com/getting-started/installation-and-upgrade/installation-references/helm-chart-options
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Common options in the chart reference: `hostname` (FQDN of the server), `bootstrapPassword`, `ingress.tls.source` (`rancher`, `letsEncrypt` or `secret`; default `rancher`), `letsEncrypt.email`, `letsEncrypt.environment` (`staging` or `production`) and `privateCA`.

Advanced options worth knowing:

- `replicas` defaults to 3. Setting `-1` makes the chart choose 1, 2 or 3 from the number of available nodes.
- `antiAffinity` is the AntiAffinity rule for Rancher pods: `preferred` (default) or `required`.
- `extraEnv` passes extra environment variables into the Rancher container, using any key valid in a Kubernetes container env entry. The page's example sets `CATTLE_TLS_MIN_VERSION`. Credentials should come from a secret reference (`valueFrom.secretKeyRef`), not a literal value.
- `addLocal` controls whether Rancher imports the cluster it runs on. It only has effect on the initial install, and the page warns that turning it off breaks most v2.5 features, including the EKS provisioner. Anyone with access to `local` is effectively root on every managed cluster.
- `systemDefaultRegistry` and `useBundledSystemChart` support air gap installs.
- `ingress.enabled=false` skips the Rancher ingress so you can deploy your own; `ingress.extraAnnotations` customises the one Rancher creates.
- `debug`, `resources` and `imagePullSecrets` are also listed.

Audit logging via `auditLog.enabled` and `auditLog.level` creates a `rancher-audit-log` sidecar streaming to stdout by default.

## Checked

2026-11-04. Checked against the Rancher Manager documentation pages: Rancher Helm Chart Options. Removed the claim about what antiAffinity required does beyond the documented values.

Method: documentation only; no commands were run.
