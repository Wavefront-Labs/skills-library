---
id: computing-software.cybersecurity-defensive.trivy.first-steps-trivy-command-pattern
name: first-steps-trivy-command-pattern
category: computing-software
field: cybersecurity-defensive
product: trivy
tags: [trivy-cli, targets, scanners, trivy-image, trivy-fs, trivy-k8s, quick-start]
level: intro
status: docs-checked
description: "Understand Trivy's command shape of target plus scanners plus subject, with first commands for an image, a project directory and a Kubernetes cluster."
sources:
  - https://trivy.dev/latest/docs/getting-started/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Trivy's CLI follows its two main concepts: targets (what you scan) and scanners (what you scan for). The documented pattern is:

```bash
trivy <target> [--scanners <scanner1,scanner2>] <subject>
```

Examples from the first-steps page:
- Container image with the default scanner, which is the vulnerability scanner: `trivy image python:3.4-alpine`
- Local code repository for vulnerabilities, exposed secrets and misconfigurations: `trivy fs --scanners vuln,secret,misconfig /path/to/myproject`
- Kubernetes cluster with all available scanners and a summary report: `trivy k8s --report summary cluster`

Targets covered in the user guide are container image, filesystem, rootfs, code repository, virtual machine image, Kubernetes and SBOM. Scanner names used in `--scanners` include `vuln`, `secret`, `misconfig` and `license`.

Getting Trivy: `brew install trivy` on macOS, `docker run aquasec/trivy`, or a binary from the GitHub release page. The page points to integrations such as GitHub Actions, the Kubernetes operator and a VS Code plugin, all listed under the Ecosystem section of the docs.

## Checked

2026-11-03. Read and confirmed against the First steps page and the License Scanning page on trivy.dev: the commands, flags, field names, defaults and behaviours stated above. Removed: the product names trivy-action and trivy-operator, which the page does not give.

Method: documentation only; no commands were run.
