---
id: computing-software.cloud-infrastructure-engineering.kubernetes.trivy-image-config-and-cluster-scans
name: trivy-image-config-and-cluster-scans
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, image-security, trivy-k8s, trivy, vulnerability-scanning, misconfiguration]
level: practitioner
status: docs-checked
description: "Use trivy image, trivy config and trivy k8s to find vulnerabilities, misconfigurations and exposed secrets in images, manifests and running clusters."
sources: ["https://trivy.dev/latest/docs/target/container_image/", "https://trivy.dev/latest/docs/target/kubernetes/", "https://trivy.dev/latest/docs/configuration/filtering/", "https://trivy.dev/latest/docs/references/configuration/cli/trivy_kubernetes/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# trivy image, config and k8s scans

## Images
```bash
trivy image --severity HIGH,CRITICAL --ignore-unfixed registry.internal/app:1.4.2
trivy image --exit-code 1 --severity CRITICAL --format sarif -o trivy.sarif registry.internal/app:1.4.2
trivy image --scanners vuln,secret --input app.tar          # image tarball from docker save
```
`--ignore-unfixed` skips vulnerabilities that have no fixed version, keeping CI focused on actionable items.
`.trivyignore` (and the structured `.trivyignore.yaml`, passed with `--ignorefile`) lists accepted IDs. By default
`trivy image` runs the vulnerability and secret scanners; `--scanners vuln` limits it.

## Manifests, Helm charts, Dockerfiles
```bash
trivy config ./k8s/                    # Kubernetes YAML, Helm charts, Terraform, CloudFormation, Dockerfile
trivy config --severity HIGH,CRITICAL ./k8s/
```
Checks map to IDs like `KSV001` (a program can elevate its own privileges) and `KSV012` (run as non-root).
In compliance specs they appear with an `AVD-` prefix, for example `AVD-KSV-0012`.

## Live cluster
```bash
trivy k8s --report summary                       # whole cluster, current context
trivy k8s --include-namespaces shop --report all
trivy k8s --scanners misconfig,rbac --report summary
trivy k8s --compliance k8s-cis-1.23 --report summary
```
`--scanners` accepts `vuln`, `misconfig`, `secret` and `rbac` (all four by default). The scan covers
workload images, workload configs, RBAC and node components (a node-collector job runs unless
`--disable-node-collector` is set). Scope with `--include-namespaces` or `--exclude-namespaces` (not both),
`--skip-images` or `--exclude-kinds`.

## Continuous
Trivy Operator runs scans in-cluster and writes `VulnerabilityReport` and
`ConfigAuditReport` CRs per workload (see the Trivy Operator skill).

## Verify
The pipeline fails (non-zero `--exit-code` when issues are found) on a deliberately vulnerable test image and
passes on the patched one.

## Checked

Checked on 2026-10-26 against `aquasecurity/trivy` docs (`docs/guide/target/container_image.md`, `target/kubernetes.md`, `configuration/filtering.md`, `configuration/reporting.md`, `compliance/compliance.md`, CLI reference `trivy_kubernetes.md`; latest release v0.76.1) and `aquasecurity/trivy-checks` (`avd_docs/kubernetes/general/KSV-0001`, `KSV-0012`).
Confirmed: `--severity`, `--ignore-unfixed`, `--scanners vuln,secret` and `--input`, `--format sarif` for image scans, `.trivyignore` and `.trivyignore.yaml`; `trivy k8s` flags `--report summary|all`, `--include-namespaces`, `--scanners` values including `rbac`, `--compliance` IDs `k8s-cis-1.23`; KSV001 and KSV012 meanings.
Removed as unconfirmed: stdin support for `trivy config -` and the `helm template` pipe.

Method: documentation only; no commands were run.
