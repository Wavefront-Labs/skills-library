---
id: computing-software.cloud-infrastructure-engineering.terraform.trivy-config-scanning-and-tfsec-migration
name: trivy-config-scanning-and-tfsec-migration
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, trivy, trivy-config, trivy-misconfig, tfsec-migration, tfsec, iac-scanning]
level: practitioner
status: docs-checked
description: "Scan Terraform with trivy config (severity, tfvars, plan JSON, ignores, custom checks) and migrate from tfsec: mapping IDs, ignore comments and CI flags."
sources: ["https://aquasecurity.github.io/trivy/latest/docs/scanner/misconfiguration/", "https://aquasecurity.github.io/trivy/latest/docs/coverage/iac/terraform/", "https://github.com/aquasecurity/tfsec/blob/master/tfsec-to-trivy-migration-guide.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# trivy config, and migrating from tfsec

tfsec has joined the Trivy family; Trivy's misconfiguration scanner (`trivy config`) is the
replacement. Trivy scans Terraform HCL, plan snapshots and plan JSON.

## Running trivy on Terraform
```bash
trivy config .                                        # HCL scan
trivy config --severity HIGH,CRITICAL --exit-code 1 .
trivy config --tf-vars dev.terraform.tfvars .         # override default values with a tfvars file
terraform show -json tfplan > tfplan.json && trivy config tfplan.json   # plan JSON scan
trivy config --tf-exclude-downloaded-modules .        # downloaded modules are scanned by default
trivy config --format sarif -o trivy.sarif .
```

## trivy.yaml
```yaml
severity: [HIGH, CRITICAL]
exit-code: 1
misconfiguration:
  scanners: [terraform]
  terraform:
    exclude-downloaded-modules: false
scan:
  skip-dirs: [examples, tests]
```

## Ignoring
```hcl
#trivy:ignore:AVD-AWS-0107
resource "aws_security_group_rule" "example" { /* ... */ }
```
Or a `.trivyignore` file (IDs, optionally with an `exp:YYYY-MM-DD` expiry) or a
`.trivyignore.yaml` (per-ID `paths` and `expired_at` date), selected with `--ignorefile`.

## tfsec → trivy migration
| tfsec | trivy |
|---|---|
| `tfsec <dir>` | `trivy config <dir>` |
| `tfsec <dir> --tf-vars-file <vars>` | `trivy config --tf-vars <vars> <dir>` |
| `tfsec <dir> --format <type>` | `trivy config --format <type> <dir>` |
| skip directories or files | `--skip-dirs`, `--skip-files` |
| `#tfsec:ignore:AWS006` | `#trivy:ignore:AVD-AWS-0107` |
| custom checks | Rego checks via `--config-check <path>` |
| CI | `aquasecurity/trivy-action` (the official Trivy action) |
Trivy keeps its misconfiguration checks up to date by pulling from a container registry and
uses the embedded checks only if it cannot pull. Reports can be table, JSON, SARIF, template
or SBOM; one report per scan.

## Gotchas
- Trivy pulls updated checks at runtime; `--skip-check-update` skips fetching Rego check updates
  (for air-gapped CI, rely on the embedded checks or supply your own with `--config-check`).
- Plan JSON scans cannot always resolve references in expressions that use `each` or `count`,
  so some resource relationships are missed.
- Trivy can scan a plan snapshot (`terraform plan --out tfplan; trivy config tfplan`) or its JSON.

## Verify
- [ ] CI fails on a HIGH finding and passes after fix or justified ignore.
- [ ] No workflow still calls `tfsec` after migration.

## Checked
- 2026-10-28. Confirmed against the Trivy CLI reference for `trivy config` (`--severity`, `--exit-code`, `--format`, `-o`, `--tf-vars`, `--tf-exclude-downloaded-modules`, `--skip-dirs`, `--skip-files`, `--config-check`, `--skip-check-update`, `--ignorefile`), the Trivy config-file reference (`severity`, `exit-code`, `misconfiguration.scanners`, `terraform.exclude-downloaded-modules`, `scan.skip-dirs`), the Trivy Terraform coverage page (HCL, plan snapshot, plan JSON, value overrides, plan JSON limitation), the Trivy filtering page (`.trivyignore`, `exp:`, `.trivyignore.yaml` with `paths` and `expired_at`), the Trivy CI/CD page (`trivy-action`), the tfsec-to-Trivy migration guide, and the pre-commit-terraform README (`#tfsec:ignore:` and `#trivy:ignore:` comment forms).
- Removed: `--minimum-severity`, `--soft-fail` mapping, tfsec ignore comments being honoured by Trivy, inline `:exp:` expiry, `scan-type: config`, the AVD ID mapping claim and the severity-after-evaluation claim (not in the fetched pages).
Method: documentation only; no commands were run.
