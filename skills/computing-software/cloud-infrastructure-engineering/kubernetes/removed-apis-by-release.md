---
id: computing-software.cloud-infrastructure-engineering.kubernetes.removed-apis-by-release
name: removed-apis-by-release
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, api-deprecation, removed-apis, deprecated-apis, kubectl-convert, pluto, mapkubeapis]
level: practitioner
status: docs-checked
description: "Know which API versions were removed in which Kubernetes release (1.16 to 1.32), their replacements, and how to find and migrate manifests before upgrading."
sources: ["https://kubernetes.io/docs/reference/using-api/deprecation-guide/", "https://kubernetes.io/docs/reference/using-api/deprecation-guide/#what-to-do"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Removed APIs by release

From the official deprecation guide (most-hit entries):
| Release | Removed | Use instead |
|---|---|---|
| 1.16 | `extensions/v1beta1` and `apps/v1beta1/2` Deployments, DaemonSets, ReplicaSets; `extensions/v1beta1` NetworkPolicy, PodSecurityPolicy | `apps/v1`, `networking.k8s.io/v1`, `policy/v1beta1` |
| 1.22 | `extensions/v1beta1` and `networking.k8s.io/v1beta1` Ingress/IngressClass; `apiextensions.k8s.io/v1beta1` CRD; `admissionregistration.k8s.io/v1beta1` webhooks; `certificates.k8s.io/v1beta1` CSR; `rbac.authorization.k8s.io/v1beta1` | `networking.k8s.io/v1` etc. (`v1`) |
| 1.25 | `batch/v1beta1` CronJob; `policy/v1beta1` PodDisruptionBudget and PodSecurityPolicy (PSP removed entirely); `discovery.k8s.io/v1beta1` EndpointSlice; `autoscaling/v2beta1` HPA; `events.k8s.io/v1beta1` | `batch/v1`, `policy/v1`, Pod Security Admission, `discovery.k8s.io/v1`, `autoscaling/v2` |
| 1.26 | `autoscaling/v2beta2` HPA; `flowcontrol.apiserver.k8s.io/v1beta1` | `autoscaling/v2` (since 1.23), `flowcontrol.apiserver.k8s.io/v1beta2` (itself removed in 1.29) |
| 1.27 | `storage.k8s.io/v1beta1` CSIStorageCapacity | `storage.k8s.io/v1` |
| 1.29 | `flowcontrol.apiserver.k8s.io/v1beta2` | `flowcontrol.apiserver.k8s.io/v1` (since 1.29) or `v1beta3` (since 1.26) |
| 1.32 | `flowcontrol.apiserver.k8s.io/v1beta3` | `flowcontrol.apiserver.k8s.io/v1` |
The deprecation guide lists no removals after v1.32 as of this check (Kubernetes docs for
v1.37). Always read the guide for the exact target release; field-level changes accompany some
moves (Ingress `serviceName/servicePort` to `service.name`/`service.port.number`, `pathType`
now required, the policy/v1 PDB empty selector selecting all pods, v1 webhook and CRD
default changes).

## Find usage
- Test with an API server started with `--runtime-config=<group>/<version>=false`.
- Use client warnings, metrics and audit information (available in 1.19+). The API server metric
  `apiserver_requested_deprecated_apis` (stable) is a gauge broken out by group, version,
  resource, subresource and `removed_release`.
- Third-party scanners: Pluto checks static manifests, Helm charts and live Helm releases
  (for example `pluto detect-files -d <dir>`); kubent (kube-no-trouble) checks a cluster,
  including Helm v3 release data. See their READMEs for subcommands and flags.
Stored objects are accessible through the new API versions (the guide says so for each
removal); the usual problems are manifests, Helm release history and clients.

## Migrate
```bash
kubectl convert -f old-ingress.yaml --output-version networking.k8s.io/v1 > ingress.yaml   # kubectl-convert plugin, not installed by default
```
The Helm `mapkubeapis` plugin updates Helm release metadata that references removed APIs (see
the Helm docs page on Kubernetes APIs). `kubectl convert` may choose non-ideal default values;
check the API reference for the resource.

## Checked
Date: 2026-10-27. Documentation: Kubernetes website "Deprecated API Migration Guide" (current
docs; latest release v1.37.1), apiserver metrics source, the Helm docs page on Kubernetes APIs, and the
Pluto and kubent READMEs. Confirmed: every row in the table (sections v1.16, v1.22, v1.25, v1.26,
v1.27, v1.29, v1.32), `kubectl convert` usage and status, the metric name and stability,
`--runtime-config` testing, `mapkubeapis`. Corrected the 1.26 flowcontrol replacement to
`v1beta2`; removed unconfirmed Pluto flags and the `kubectl get --raw` grep.
Method: documentation only; no commands were run.
