---
id: computing-software.cloud-infrastructure-engineering.infrastructure-as-code.drift-detection-tools-driftctl-and-cloud-native
name: drift-detection-tools-driftctl-and-cloud-native
category: computing-software
field: cloud-infrastructure-engineering
product: infrastructure-as-code
tags: [infrastructure-as-code, iac, drift-detection, driftctl, snyk-iac-drift, aws-config, cloudformation-drift, azure-resource-graph, unmanaged-resources]
level: advanced
status: draft
description: "Find drift and unmanaged resources beyond terraform plan: driftctl/Snyk IaC describe, CloudFormation drift detection, AWS Config and Azure Resource Graph queries, and what each misses."
sources: ["driftctl documentation (https://docs.driftctl.com/) and Snyk IaC describe documentation (https://docs.snyk.io/scan-with-snyk/snyk-iac/iac-describe)", "AWS CloudFormation User Guide - Detecting unmanaged configuration changes (drift detection)", "Microsoft Learn - Azure Resource Graph query language"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Drift detection tools: driftctl and cloud-native

Goal: catch two different problems — **drift** (managed resources changed outside code) and
**unmanaged resources** (things created in the console that no code knows about). `terraform plan`
only sees the first, and only for resources in its state.

## driftctl / Snyk IaC describe
driftctl compared cloud APIs with Terraform state files and reported managed, unmanaged and
missing resources. The open-source project is in maintenance mode; its engine lives on as
`snyk iac describe`. Usage pattern (both):
```bash
# driftctl (pinned old release)
driftctl scan --from tfstate+s3://acme-tfstate/**/*.tfstate --to aws+tf --output json://drift.json
# Snyk
snyk iac describe --from="tfstate+s3://acme-tfstate/**/*.tfstate" --json > drift.json
```
- `--from` accepts many state files (glob over the whole bucket) so coverage is account-wide.
- `.driftignore` / `.snyk` policy excludes known noise (`aws_iam_policy_attachment.*`, default VPC, resources owned by other tools).
- Output: coverage % (managed / total) — a great IaC-adoption metric.
Requires read-only credentials to the account and to the state backend.

## Cloud-native options
| Tool | What it finds |
|---|---|
| CloudFormation drift detection (`aws cloudformation detect-stack-drift`, `describe-stack-resource-drifts`) | Property drift on CFN-managed resources only |
| AWS Config (+ advanced queries) | Inventory and change history of everything; query for resources missing an `iac-managed`/`terraform` tag |
| Azure Resource Graph | Same, Azure: `resources | where tags['managed-by'] != 'terraform'` |
| GCP Cloud Asset Inventory | Export all assets; diff with state |
| CloudTrail / Activity log | *Who* made the out-of-band change — needed to fix the cause |

Tag-based unmanaged detection: tag every resource from code (`default_tags { managed-by = "terraform", repo = ... }`),
then any resource without the tag is unmanaged by definition.

## Plan-based drift (the baseline)
`terraform plan -refresh-only -detailed-exitcode` per state on a schedule (exit 2 = drift) —
covered in the scheduled drift detection skill; use the tools above in addition, not instead.

## Triage loop
1. Drift on managed resource → revert by apply, or codify the change (if it was a valid hotfix).
2. Unmanaged resource → import it, delete it, or add to ignore list with an owner and reason.
3. Find the actor in audit logs; remove their write path (permission, pipeline gap).

## Gotchas
- Resources created by other automation (Kubernetes controllers creating ELBs, autoscaling ENIs) show as unmanaged; ignore them by tag or type, not one by one.
- Snyk describe and driftctl need state access, which contains secrets; run from a locked-down job.
- CFN drift detection doesn't cover all resource types or properties; read the supported list.

## Verify
- [ ] Weekly report with coverage %, unmanaged count and drift count per account, with owners.
- [ ] A console-created test bucket shows up as unmanaged in the next run.
