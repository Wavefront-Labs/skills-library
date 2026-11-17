---
id: computing-software.cloud-infrastructure-engineering.kubernetes.continuous-compliance-reporting-trivy
name: continuous-compliance-reporting-trivy
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, cis-benchmark, compliance-report, trivy-operator, clustercompliancereport, nsa-hardening]
level: practitioner
status: docs-checked
description: "Produce scheduled CIS, NSA and Pod Security compliance reports with trivy k8s --compliance and Trivy Operator ClusterComplianceReports, and track drift over time."
sources: ["https://trivy.dev/latest/docs/compliance/compliance/", "https://trivy.dev/latest/docs/target/kubernetes/", "https://aquasecurity.github.io/trivy-operator/latest/docs/compliance/compliance/", "https://aquasecurity.github.io/trivy-operator/latest/docs/crds/clustercompliance-report/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Continuous compliance reporting with Trivy

## One-off report
```bash
trivy k8s --compliance=k8s-cis-1.23 --report summary
trivy k8s --compliance=k8s-nsa-1.0 --report all --format json -o nsa.json
trivy k8s --compliance=k8s-pss-restricted-0.1 --report summary
```
Built-in Kubernetes specs include `k8s-nsa-1.0`, `k8s-cis-1.23`, `rke2-cis-1.24`, `eks-cis-1.4`,
`k8s-pss-baseline-0.1` and `k8s-pss-restricted-0.1`. `--report summary` shows the number of failed checks per control;
`--report all` shows where each failed and why; `--format table` or `json` selects the output.

## Scheduled in-cluster
Trivy Operator creates cluster-scoped `ClusterComplianceReport` objects (`aquasecurity.github.io/v1alpha1`)
whose `spec` carries `cron` (report interval), `reportType` (`summary` or `all`) and the control checks.
Enable and tune them in the Helm chart:
```yaml
operator:
  clusterComplianceEnabled: true      # chart default true
  metricsClusterComplianceInfo: false # set true for compliance metrics
compliance:
  cron: "0 */6 * * *"                 # chart default
  reportType: summary
  specs:                              # e.g. k8s-cis-1.23, k8s-nsa-1.0, k8s-pss-baseline-0.1
  - k8s-cis-1.23
```
```bash
kubectl get compliance
kubectl get compliance <name> -o jsonpath='{.status}'
```
Set `operator.metricsClusterComplianceInfo` for compliance metrics to chart in Grafana.

## Making it useful
- Export JSON to object storage per run; auditors want history, not a live screen.
- Track a fail count per control; alert when it rises, not on every existing failure.
- Record accepted exceptions (control ID, reason, owner, expiry) next to the report.

## Verify
A deliberately non-compliant test Deployment (privileged) increases the failing count in the
next scheduled report and disappears after removal.

## Checked

Checked on 2026-10-26 against `aquasecurity/trivy` docs (`compliance/compliance.md`, `target/kubernetes.md`) and `aquasecurity/trivy-operator` (chart `values.yaml`, docs `compliance/compliance.md`, `crds/clustercompliance-report.md`).
Confirmed: built-in spec IDs and the `--report`/`--format` options; `ClusterComplianceReport` with `cron` and `reportType`; chart values `clusterComplianceEnabled`, `metricsClusterComplianceInfo`, `compliance.cron` (default `0 */6 * * *`), `compliance.reportType` and `compliance.specs`; `kubectl get compliance`.
Wrong in the draft: the `compliance: {...}` field inside the report spec and the guessed metrics value name. Removed as unconfirmed: the kube-bench pairing advice.

Method: documentation only; no commands were run.
