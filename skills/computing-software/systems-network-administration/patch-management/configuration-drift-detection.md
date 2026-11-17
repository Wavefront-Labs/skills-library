---
id: computing-software.systems-network-administration.patch-management.configuration-drift-detection
name: configuration-drift-detection
category: computing-software
field: systems-network-administration
product: patch-management
tags: [drift-detection, configuration-drift, ansible-check-mode, test-dscconfiguration, puppet-noop, azure-machine-configuration, config-baselines]
level: practitioner
status: docs-checked
description: "Detect configuration drift from baselines with Ansible check mode, DSC Test-DscConfiguration and Azure Machine Configuration, then alert or auto-remediate."
sources:
  - https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_checkmode.html
  - https://learn.microsoft.com/en-us/powershell/module/psdesiredstateconfiguration/test-dscconfiguration
  - https://learn.microsoft.com/en-us/azure/governance/machine-configuration/overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Detecting configuration drift

**Goal:** know when a system no longer matches its baseline, and fix it before it causes an incident or audit finding.

## Ansible
```bash
ansible-playbook site.yml --check --diff --limit web
```
Tasks reporting `changed` in check mode are drift. Run on a schedule (AWX/AAP job template) and alert on any changed count above zero. Modules must support check mode. Use the per-task `check_mode` option to force a task to run (or not run) in check mode, and the `ansible_check_mode` variable to skip tasks or ignore errors under `--check`.

## PowerShell DSC
```powershell
Test-DscConfiguration -Detailed
```
`-Detailed` returns the overall state plus the resources in and not in the desired state, per computer. Use `-ComputerName` to test several nodes.

## Azure Machine Configuration (Azure and Arc servers)
Assign guest configuration policies (built-in security baselines or custom DSC packages) in the Audit mode (report only) or the Apply and Autocorrect mode (configuration is brought back into conformance if drift occurs); results show on the Guest assignments page and in Azure Policy compliance details.

## Alert vs auto-correct
- Auto-correct: security settings where any deviation is wrong (password policy, SMBv1 off).
- Alert only: settings where drift may indicate an authorised emergency change; investigate, then either update the baseline or revert.

## Gotchas
- Drift from emergency changes must be folded back into code, or auto-correct will undo the fix.
- Check mode runs can mask drift if roles skip tasks in check mode; test detection by introducing a known drift.

## Checked
2026-11-01. Confirmed: Ansible check mode options and `ansible_check_mode`; `Test-DscConfiguration -Detailed` and `-ComputerName`; Machine Configuration Audit and Apply and Autocorrect modes for Azure and Arc machines (Learn pages and Ansible check-mode guide). Removed: Puppet/Chef noop lines, LCM mode names, `ResourcesNotInDesiredState` property, command/shell changed_when advice.
Method: documentation only; no commands were run.

## Verify
Manually change a baselined setting on a test host; the next scheduled run reports (or fixes) it within the expected interval.
