---
id: computing-software.cybersecurity-defensive.trivy.compliance-reports-with-compliance-flag
name: compliance-reports-with-compliance-flag
category: computing-software
field: cybersecurity-defensive
product: trivy
tags: [compliance, cis, nsa, pss, k8s-nsa, report-summary, trivy-k8s]
level: practitioner
status: docs-checked
description: "Generate built-in compliance reports with --compliance for trivy image and trivy k8s, and pick summary or full detail in table or JSON form."
sources:
  - https://trivy.dev/latest/docs/guide/compliance/compliance/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The compliance flag curates a set of checks into a report, such as an industry set like CIS, a vendor guideline or your own organisational policy. Reports are defined as simple YAML documents that select checks. The feature is experimental.

It is supported by `trivy image` and `trivy k8s`. Add `--compliance` with the report ID:

```
trivy k8s cluster --compliance k8s-nsa
```

Built-in reports are selected by ID: `trivy --compliance <compliance_id>`. Docker reports are listed with container image scanning and Kubernetes reports with Kubernetes scanning.

Compatible flags that shape output:

| Flag | Effect |
| --- | --- |
| `--report summary` | summary showing the number of failed checks for every control |
| `--report all` | fully detailed results showing where and why each control failed |
| `--format table` | textual table, good for humans |
| `--format json` | JSON, good for machines |

IDs follow the convention `{platform}-{type}-{version}`, as in `k8s-cis-1.23`. Supported platforms are k8s, eks, aks, gke, rke2, ocp, docker and aws. Types are cis, nsa and pss.

## Checked

2026-11-03. Read and confirmed against the Built-in Compliance Reports page on trivy.dev: the commands, flags, field names, defaults and behaviours stated above. Removed: nothing.

Method: documentation only; no commands were run.
