---
id: computing-software.cloud-infrastructure-engineering.infrastructure-as-code.checkov-configuration-skips-baselines-and-custom-policies
name: checkov-configuration-skips-baselines-and-custom-policies
category: computing-software
field: cloud-infrastructure-engineering
product: infrastructure-as-code
tags: [infrastructure-as-code, security-scanning, checkov, checkov-config, checkov-skip, scan-baseline, suppressions, custom-checkov-policy, checkov-yaml-policy]
level: practitioner
status: verified
description: "Run Checkov on IaC with a .checkov.yaml config, justified inline skips, a baseline for legacy findings, and custom YAML policies for organisation rules."
sources: ["Checkov documentation - CLI command reference and config file (https://www.checkov.io/2.Basics/CLI%20Command%20Reference.html)", "Checkov - Suppressing and skipping policies (https://www.checkov.io/2.Basics/Suppressing%20and%20Skipping%20Policies.html)", "Checkov - Custom policies in YAML (https://www.checkov.io/3.Custom%20Policies/YAML%20Custom%20Policies.html)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Checkov: configuration, skips, baselines and custom policies

## Config file
```yaml
# .checkov.yaml at repo root (auto-loaded; or --config-file)
directory: [terraform, k8s]
framework: [terraform, kubernetes, github_actions, dockerfile]
skip-path: [terraform/.terraform, examples/]
skip-check: [CKV_AWS_144]            # org-wide accepted risk, documented in README
soft-fail-on: [LOW]
hard-fail-on: [HIGH, CRITICAL]       # severities require a Prisma API key; otherwise use check ids
download-external-modules: true      # scan module sources too
external-checks-dir: [policies/checkov]   # singular: `external-checks-dirs` fails with "unrecognized arguments" (Checkov 3.3.30)
output: [cli, sarif]
output-file-path: console,results
compact: true
```
Run: `checkov --config-file .checkov.yaml`; a `.checkov.yaml` in the working directory is also picked up with plain `checkov` (checked). `output-file-path: console,results` wrote the SARIF into `results/`. Terraform plan scans catch
computed values: `terraform show -json tfplan > plan.json && checkov -f plan.json --framework terraform_plan` (ran on a hand-written plan JSON).

## Inline skips (with a reason)
```hcl
resource "aws_s3_bucket" "public_site" {
  # checkov:skip=CKV_AWS_20:Public website bucket, approved in SEC-123
  bucket = "www-example"
}
```
Kubernetes: annotation `checkov.io/skip1: CKV_K8S_20=reason` (checked: skipped 1 and the check dropped from the failures). Every skip should name a ticket.

## Baselines for legacy code
```bash
checkov -d terraform --create-baseline           # writes terraform/.checkov.baseline (inside the scanned dir; directory scans only)
checkov -d terraform --baseline terraform/.checkov.baseline   # only NEW findings fail (a wrong path raises FileNotFoundError)
```
Commit the baseline; shrink it over time (re-create after fixes). Review baseline diffs in PRs —
growing baselines mean someone is hiding findings.

## Custom YAML policy
```yaml
# policies/checkov/require_owner_tag.yaml
metadata:
  id: CKV2_ORG_1
  name: All taggable resources must have an owner tag
  category: GENERAL_SECURITY
  severity: MEDIUM
definition:
  and:
    - cond_type: attribute
      resource_types: [aws_instance, aws_s3_bucket, aws_db_instance]
      attribute: tags.owner
      operator: exists
    - cond_type: attribute
      resource_types: [aws_instance, aws_s3_bucket, aws_db_instance]
      attribute: tags.owner
      operator: regex_match
      value: '^[a-z]+@example\.com$'
```
The policy above ran: `aws_instance.b` (owner `bob@example.com`) passed, an untagged instance and one with owner `bad` failed. Connection-type conditions (`cond_type: connection`) express "every SG is attached to …".
Python custom checks (subclass `BaseResourceCheck`) for logic YAML cannot express.

## Gotchas
- Without `download-external-modules`, resources inside registry modules are not scanned.
- Variables without defaults are unknown at static scan time — the plan-JSON scan is more accurate.
- Check IDs are stable but new checks arrive with each release; pin the Checkov version in CI and upgrade deliberately.

## Verify
- [ ] `checkov -d . --external-checks-dir policies/checkov --framework terraform -c CKV2_ORG_1 --compact` reports the custom check (note `checkov --list` does NOT list external checks; it printed 0 matches).
- [ ] A PR adding an untagged instance fails; a baseline-listed legacy finding does not.
