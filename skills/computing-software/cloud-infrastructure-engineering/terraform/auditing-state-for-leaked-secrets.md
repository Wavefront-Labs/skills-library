---
id: computing-software.cloud-infrastructure-engineering.terraform.auditing-state-for-leaked-secrets
name: auditing-state-for-leaked-secrets
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, state-secret-audit, sensitive-state, secrets, state-pull-jq, gitleaks]
level: practitioner
status: docs-checked
description: "Audit Terraform state for plaintext secrets: pull state, scan it with gitleaks, then remediate with ephemeral values and write-only arguments and secure the state."
sources: ["https://developer.hashicorp.com/terraform/language/state/sensitive-data", "https://github.com/gitleaks/gitleaks", "https://developer.hashicorp.com/terraform/language/resources/ephemeral", "https://developer.hashicorp.com/terraform/cli/commands/state/pull"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Auditing state for secrets

## Why state holds secrets
Terraform stores secret values you put in configuration in its state and plan files.
Local state is a plaintext file that includes those values. The `sensitive` argument on
variables and outputs only redacts values from CLI output and the HCP Terraform UI;
sensitive values are still stored in state and plan files, so anyone who can read those
files can read the values. `terraform output` with `-json` or `-raw` prints sensitive
values in plain text.

## 1. Pull the state
```bash
terraform state pull > /path/to/audit/state.json    # restricted location
```
`terraform state pull` downloads the state from its current location (remote or local),
upgrades the local copy to the latest compatible state file version and prints the raw
format to stdout; the docs suggest pairing it with `jq` to read values out of state.

## 2. Pattern scan
Gitleaks scans files and directories with its `dir` command:
```bash
gitleaks dir -v /path/to/audit/state.json
```
Since gitleaks v8.19.0 the older `detect` and `protect` commands are deprecated (still
available but hidden from `--help`). Gitleaks exits with code 1 by default when leaks are
found (`--exit-code`), and `--report-path` writes a report (`--report-format` accepts
json, csv, junit, sarif or template).

## Remediation
- Write-only arguments (names typically end in `_wo` with a matching `_wo_version`,
  for example `password_wo` on `aws_db_instance`) pass a temporary value to a resource
  without it being stored in state or plan files. Requires Terraform 1.11 or later;
  each provider defines which write-only arguments exist.
- Ephemeral resources (`ephemeral` blocks, Terraform 1.10 or later) and the `ephemeral`
  argument on variables and child module outputs keep values out of state and plan files.
  Because Terraform does not store them, capture any generated value you need in
  another resource or output.
- If you keep secrets in state, the docs recommend: store state remotely, encrypt it at
  rest, use access controls to limit who can read it, and use audit logs to track access.
  HCP Terraform encrypts state at rest; the S3 backend can encrypt at rest when the
  `encrypt` option is enabled; the GCS backend supports customer-supplied or
  customer-managed keys.

## Checked
Date: 2026-11-07

Read in full (stripped text): "Manage sensitive data in your configuration" (the old `state/sensitive-data` URL redirects there), "Ephemeral values in resources", `terraform state pull`, and, from the gitleaks README, only the usage, flags and commands sections (the rest of the README was not read and nothing is taken from it). Code tabs were not present in the stripped text.

Trimmed as unconfirmed: the `sensitive_attributes` jq inventory and the name-heuristic jq script (state JSON layout is not on these pages); trufflehog; the "typical findings" table (only `aws_db_instance` `password`/`password_wo` appears on the pages); `manage_master_user_password`; "generate secrets outside Terraform"; "old state versions still contain the secret / expire noncurrent versions"; "OpenTofu: enable state encryption"; both Verify steps. Replaced `gitleaks detect --no-git --source` with the current `gitleaks dir` form. Description changed to drop trufflehog.

Method: documentation only; no commands were run.
