---
id: computing-software.cybersecurity-defensive.cloud-security.checkov-iac-scanning
name: checkov-iac-scanning
category: computing-software
field: cybersecurity-defensive
product: cloud-security
tags: [checkov, iac-scanning, terraform-security, policy-as-code, shift-left, ci-security-gates, cspm]
level: practitioner
status: verified
description: "Scan infrastructure as code with Checkov: Terraform/CloudFormation/Kubernetes/Helm checks, plan scanning, suppressions with justification, custom policies and CI gating."
sources: ["https://www.checkov.io/1.Welcome/Quick%20Start.html", "https://www.checkov.io/2.Basics/Suppressing%20and%20Skipping%20Policies.html", "https://www.checkov.io/3.Custom%20Policies/YAML%20Custom%20Policies.html", "https://github.com/bridgecrewio/checkov"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Checkov

Static analysis of IaC for misconfigurations before deployment (public buckets, open security groups,
missing encryption, privileged pods).

## Run
```
pip install checkov
checkov -d infra/                           # directory, auto-detects frameworks
checkov -d infra/ --framework terraform --compact --quiet
# scan the resolved plan (variables, modules expanded):
terraform plan -out tf.plan && terraform show -json tf.plan > tf.json && checkov -f tf.json
checkov -d charts/ --framework helm               # needs the helm binary on PATH
checkov -d . -o sarif --output-file-path results/   # upload to GitHub code scanning
```

## Gate in CI
- Checkov exits 1 when any check fails. `--check CKV_AWS_24` selects checks by id, `--skip-check` excludes, `--soft-fail` forces exit 0.
- Severity does NOT work offline. Without a Prisma Cloud/Bridgecrew API key checks carry no severity: `--check HIGH` logs
  "Filtering checks by severity is only possible with an API key" and `--hard-fail-on HIGH` still exited 0 on a failing scan
  (Checkov 3.3.30). In open-source CI gate by check id (`--check` / `--skip-check` / `--hard-fail-on CKV_AWS_24,...`).
- Baseline existing findings: `checkov -d infra/ --create-baseline` writes `.checkov.baseline` (directory scans only, saved in the
  scanned directory, so `infra/.checkov.baseline` here); then `--baseline infra/.checkov.baseline` reports only new failures.

## Suppressions (in code, with reason)
```hcl
resource "aws_s3_bucket" "public_site" {
  # checkov:skip=CKV_AWS_20:Public static website, approved SEC-1234
  bucket = "www-example"
}
```
Review suppressions in PRs; report on them periodically.

## Custom policies (YAML)
```yaml
metadata: {id: CKV2_ORG_1, name: "S3 buckets must have data-classification tag", category: GENERAL_SECURITY}
definition:
  cond_type: attribute
  resource_types: [aws_s3_bucket]
  attribute: tags.data-classification
  operator: exists
```
`checkov -d infra/ --external-checks-dir policies/` (checked: the custom check ran and failed the untagged bucket as `CKV2_ORG_1`).
Plan scanning (`checkov -f tf.json`) reports under `terraform_plan` and shows `File: /tf.json:0-0` instead of source lines.

## Gotchas
- Scanning HCL only misses values from variables/modules; scan plans for accuracy.
- IaC scanning does not see console changes (drift); pair with runtime CSPM.
- Pin Checkov version in CI; new checks can break builds unexpectedly.

## Verify
- [ ] Pipeline fails on a test PR adding `0.0.0.0/0` SSH ingress.
- [ ] Suppressions all carry ticket references.
