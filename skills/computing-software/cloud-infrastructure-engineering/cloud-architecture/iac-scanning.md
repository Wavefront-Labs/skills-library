---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.iac-scanning
name: iac-scanning
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, infrastructure-protection, iac-scanning, checkov, trivy-config, tfsec, kics, shift-left-security, misconfiguration-scanning]
level: practitioner
status: verified
description: "Scan infrastructure-as-code for misconfigurations before deploy: Checkov/Trivy/KICS in pre-commit and CI, plan-based scanning, baselines, suppressions with reasons."
sources: ["https://www.checkov.io/1.Welcome/What%20is%20Checkov.html", "https://trivy.dev/latest/docs/scanner/misconfiguration/", "https://docs.kics.io/latest/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IaC security scanning

## Tools
- **Checkov**: Terraform (HCL and plan JSON), CloudFormation, Bicep/ARM, Kubernetes, Helm,
  Dockerfiles, Ansible and more (`checkov --help` lists the frameworks, including arm, bicep, cdk, ansible, helm); custom policies in Python/YAML (a YAML custom policy ran with `--external-checks-dir`).
- **Trivy** (`trivy config .`; tfsec's repo now says "Tfsec is now part of Trivy"): misconfig + vulnerabilities + secrets.
- **KICS**: broad IaC coverage with Rego queries (per its docs/creating-queries.md).

## Pipeline placement
1. Pre-commit hook for fast feedback.
2. CI on pull request: `checkov -d . --framework terraform --output sarif --output-file-path results/` and upload SARIF to the
   code-scanning UI. Without `--output-file-path`, SARIF goes to `results_sarif.sarif` in the working directory (checked, Checkov 3.3.30) while stdout shows the CLI report. Failing on HIGH/CRITICAL needs a platform API key: offline Checkov checks have no severity (`--check HIGH` only warns, `--hard-fail-on HIGH` still exited 0), so gate on check ids or `--soft-fail` plus review.
3. Plan scanning catches values resolved only at plan time:
   `terraform plan -out tf.plan && terraform show -json tf.plan > plan.json && checkov -f plan.json`.
4. Runtime CSPM still needed for console changes and drift.

## Managing findings
- Baseline existing findings (`--create-baseline`) to stop new ones without blocking on old debt.
- Inline suppressions with reason and ticket: `#checkov:skip=CKV_AWS_18:Access logs go to central bucket via org trail` (checked: reported as Skipped 1). `--create-baseline` writes `.checkov.baseline` for directory scans only.
- Custom checks for org standards (tags, allowed SKUs).

## Gotchas
- Scanning modules but not the composition; misconfig often appears in variable values.
- Hundreds of low-severity findings training people to ignore output; tune severity gates.

## Verify
- [ ] PR introducing a public bucket fails CI.
- [ ] Suppressions all have reasons; reviewed quarterly.
