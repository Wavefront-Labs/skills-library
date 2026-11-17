---
id: computing-software.cloud-infrastructure-engineering.infrastructure-as-code.scheduled-drift-detection-and-alerting
name: scheduled-drift-detection-and-alerting
category: computing-software
field: cloud-infrastructure-engineering
product: infrastructure-as-code
tags: [infrastructure-as-code, drift-detection, scheduled-plan, drift-cron, drift-alerts, detailed-exitcode, check-mode]
level: practitioner
status: docs-checked
description: "Detect drift on a schedule with terraform plan -detailed-exitcode, HCP Terraform health assessments and ansible --check runs."
sources:
  - https://developer.hashicorp.com/terraform/cli/commands/plan
  - https://developer.hashicorp.com/terraform/cloud-docs/workspaces/health
  - https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_checkmode.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scheduled drift detection and alerting

## Terraform CLI
`terraform plan -detailed-exitcode` changes the exit codes: 0 = succeeded with empty diff, 1 = error, 2 = succeeded with non-empty diff. A scheduled job (your CI scheduler of choice) can run it per root module and alert on 2, and on 1 separately.
```bash
terraform plan -input=false -detailed-exitcode
```
- `-input=false` avoids prompts for unassigned root variables in non-interactive automation.
- `-lock=false` skips the state lock; the docs call this dangerous if others might run commands against the same workspace concurrently.
- A normal plan mixes drift with unapplied code changes. `terraform plan -refresh-only` is the mode that only reconciles state and outputs with changes made outside Terraform.
- A plan saved with `-out` holds the full configuration and planned values; sensitive data is saved in cleartext even though terminal output obscures it, so treat saved plan files as sensitive artifacts.

## HCP Terraform health assessments
- Automatic health assessments in a workspace include drift detection (does real infrastructure match the configuration) and continuous validation (do custom conditions still pass).
- Requirements: Terraform 0.15.4+ for drift detection only, 1.3.0+ for drift plus continuous validation; remote or agent execution mode; the latest run must have succeeded, otherwise assessments pause until a successful apply. Available in the Standard and Premium editions.
- Each assessment is scheduled a set period after the more recent of last apply or last assessment. A new run cancels an assessment in progress, so workspaces with very frequent runs may rarely be assessed.
- Notifications follow the workspace notification settings. Drift detection finds configuration drift, not state drift.
- Resolve drift either by queueing a plan and apply to overwrite the drift, or by changing the configuration to include the change so the next apply does not revert it.
- Continuous validation evaluates preconditions, postconditions and `check` blocks; `check` blocks are recommended for post-apply monitoring. Because an assessment is a speculative plan, a data source whose queried values changed can cause false positives; use nested data sources that query actual resource configuration.

## Ansible
`ansible-playbook site.yml --check` runs without changing remote systems: modules that support check mode report what they would change; modules that do not support it report nothing and do nothing. Add `--diff` for before-and-after output (large; best on one host at a time).
- Check mode is a simulation and does not produce output for tasks using conditionals based on registered variables.
- `check_mode: false` on a task forces it to run for real even under `--check`; `check_mode: true` forces simulation always. The magic variable `ansible_check_mode` lets you skip a task or ignore its errors in check mode.
- `--diff` can reveal sensitive information; set `diff: false` on such tasks.

## Verify
- [ ] A manual change outside Terraform makes the scheduled job exit 2 (or HCP Terraform report drift) at the next run.

## Checked
Method: docs-checked 2026-11-09 against the HashiCorp "terraform plan command" and HCP Terraform "Health" pages and the Ansible "check mode and diff mode" page (full text read).
Removed: sample shell script, GitHub Actions cron, JSON callback jq parsing, ansible_check_mode_drift variable, AWX check job type, alert routing/dedup/severity advice, ignore_changes advice and credential gotchas (not on pages read).
