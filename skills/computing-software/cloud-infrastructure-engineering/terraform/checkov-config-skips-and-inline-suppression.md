---
id: computing-software.cloud-infrastructure-engineering.terraform.checkov-config-skips-and-inline-suppression
name: checkov-config-skips-and-inline-suppression
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, checkov, checkov-config, checkov-skip, inline-suppression, iac-scanning, static-analysis]
level: practitioner
status: docs-checked
description: "Run checkov on Terraform code and plans with a config file, skip checks globally or inline with justification, and manage suppressions across tools."
sources: ["https://www.checkov.io/2.Basics/CLI%20Command%20Reference.html", "https://www.checkov.io/2.Basics/Suppressing%20and%20Skipping%20Policies.html", "https://www.checkov.io/7.Scan%20Examples/Terraform%20Plan%20Scanning.html", "https://aquasecurity.github.io/trivy/latest/docs/scanner/misconfiguration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# checkov config, skips and inline suppression

## Running
```bash
checkov -d . --framework terraform --compact --quiet
checkov -d . --download-external-modules true       # scan module sources too
terraform show -json tfplan > plan.json && checkov -f plan.json --framework terraform_plan
checkov -d . -o sarif --output-file-path results/    # upload to code scanning
```
Plan scanning gives Checkov additional dependencies and context, and a plan can contain
secrets, so run it in a secure CI/CD setting. `--repo-root-for-plan-enrichment <dir>` (with
`-f`) takes code blocks and resource IDs from the Terraform files and respects skip comments
in them during a plan scan.

## Config file
Pass a YAML config with `--config-file <path>`. `--create-config <path>` writes your current
command-line arguments to a config file, and `--show-config` prints every setting and where
it came from (command line, config file, environment variable or default). Related flags:
`--skip-path` (regular expression, repeatable), `--skip-check` / `--check` (check IDs or
wildcards), `--soft-fail` and `--soft-fail-on`, `--baseline` / `--create-baseline` (writes
`.checkov.baseline`, only with `--directory`). Checks removed with `--skip-check` do not run
and do not appear in the output.

## Inline suppression (per resource)
```hcl
resource "aws_s3_bucket" "public_site" {
  #checkov:skip=CKV_AWS_20:Public website bucket by design (ticket SEC-142)
  bucket = "acme-www"
}
```
Format: `checkov:skip=<check_id>:<suppression_comment>` inside the resource or block. The
comment is optional in Checkov, but always include a reason and a ticket; reviewers should
treat new skips like code. The output then shows a SKIPPED result for that resource.

## Other scanners' inline syntax (same resource)
| Tool | Comment |
|---|---|
| trivy | `#trivy:ignore:AVD-AWS-0107` |
| tfsec (legacy) | `#tfsec:ignore:AWS006` |
Mixing tools means multiple comments; standardise on one scanner where possible.

## Gotchas
- Global `skip-check` hides the issue for every resource — prefer inline skips for exceptions.
- Graph checks (IDs like `CKV2_...`) evaluate connections between resources; related
  resources must be in the same scan.
- `--download-external-modules` downloads external modules from public git repositories and
  the Terraform registry so they can be scanned.
- Plan scans ignore a few checks that depend on the `lifecycle` block, which is not stored in
  the plan file (CKV_AWS_217, CKV_AWS_233, CKV_AWS_237, CKV_GCP_82).

## Verify
- [ ] `checkov -d .` exits 0 in CI, and inline skips show as SKIPPED with their reasons.
- [ ] Every `checkov:skip` comment in review carries a reason.

## Checked
- 2026-10-28. Confirmed against the Checkov CLI reference (`-d`, `-f`, `--framework` incl. `terraform` and `terraform_plan`, `--compact`, `--quiet`, `-o sarif`, `--output-file-path`, `--download-external-modules`, `--skip-path`, `--soft-fail`, `--config-file`, `--create-config`, `--show-config`, `--baseline`, `--repo-root-for-plan-enrichment`), the "Suppressing and Skipping Policies" page (comment form, optional reason, SKIPPED output, `--skip-check` behaviour), the "Terraform Plan Scanning" page (context, secrets caution, enrichment, ignored checks), the Trivy migration material and the pre-commit-terraform README (trivy and tfsec ignore comment forms).
- Removed: the `.checkov.yaml` auto-discovery and key list, the KICS and tflint comment syntax, CKV_AWS_144 and CKV2_AWS_6 examples, and the speed and credentials claims (not in the fetched pages).
Method: documentation only; no commands were run.
