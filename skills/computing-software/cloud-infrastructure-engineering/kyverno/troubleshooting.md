---
id: computing-software.cloud-infrastructure-engineering.kyverno.troubleshooting
name: troubleshooting
category: computing-software
field: cloud-infrastructure-engineering
product: kyverno
tags: [troubleshooting, webhook-recovery, clientratelimitqps, dumppayload, oomkilled, aks-enforcer, port-9443]
level: practitioner
status: docs-checked
description: "Troubleshoot Kyverno: recover a blocked API server, find why policies do not apply, OOMKills, throttling, verbose logs, GKE, EKS and AKS."
sources:
  - https://kyverno.io/docs/guides/troubleshooting/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
API server blocked (Kyverno down, fail-closed policies match Pods, system namespaces not excluded): delete `kubectl delete validatingwebhookconfiguration kyverno-resource-validating-webhook-cfg` and `mutatingwebhookconfiguration kyverno-resource-mutating-webhook-cfg`; they are recreated on recovery. Restart by scaling `kyverno-admission-controller` to 0 then 3. `kyverno` namespace is excluded by default.

Policies not applied: `kubectl -n kyverno get po`; `kubectl get cpol,pol -A` (READY must be True); compare webhook ages with pods; from a busybox pod run `wget --spider https://kyverno-svc.kyverno.svc:443/health/liveness`. Validate rules block only with `failureAction: Enforce` (samples default to Audit). Check ConfigMap `kyverno` keys `resourceFilters`, `excludeGroups`, `excludeUsernames`.

High resource use or OOMKills: avoid `"*"` match policies, find the loaded controller, size for peak, raise `resources.limits.memory`, and check `kubectl -n kyverno get updaterequests` for pending items (permissions, unlabelled clone sources).

Throttling ("Waited for <n>s due to client-side throttling"): raise `--clientRateLimitQPS` and `--clientRateLimitBurst` gradually. Admission reports piling up: check the reports controller, set both flags to 500; 1.10+ has cron jobs that prune reports.

Debugging: `-v` on the container args (max `-v=6`; `-v=4` and grep `variable` for variable issues), `dumpPayload=true` logs AdmissionReviews at a cost.

Platforms:
- AKS Admissions Enforcer loops on Kyverno webhooks; annotation `admissions.enforcer/disabled: true` via Helm `config.webhookAnnotations` (default since 1.12).
- GKE private clusters: firewall TCP 9443.
- EKS: custom CNI needs `hostNetwork: true`; `context deadline exceeded` means an old VPC CNI or a security group blocking 9443.

Background controller permission errors: `kubectl auth can-i create <plural> --as system:serviceaccount:kyverno:kyverno-background-controller`, fix with aggregation-labelled ClusterRoles using plural resource names.

## Checked

2026-11-08. Claims were read against: https://kyverno.io/docs/guides/troubleshooting/.

Method: documentation only; no commands were run.
