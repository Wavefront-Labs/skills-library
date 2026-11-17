---
id: computing-software.cloud-infrastructure-engineering.ansible.job-template-run-options-check-type-limit-forks-verbosity
name: job-template-run-options-check-type-limit-forks-verbosity
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, job-templates, job-type-check, jt-limit, jt-forks, check-mode]
level: intro
status: docs-checked
description: "Configure job template run options: job type run vs check, limit, forks, verbosity, diff mode, timeout and their prompt-on-launch toggles."
sources: ["https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/html-single/using_automation_execution/", "https://github.com/redhat-cop/infra.aap_configuration"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Job template run options

```yaml
controller_templates:          # infra.aap_configuration controller_job_templates role input
  - name: Patch web (check)
    job_type: check            # run | check
    inventory: Production
    project: infra-ansible
    playbook: playbooks/patch.yml
    limit: web
    forks: 20                  # 0 = the Ansible default
    verbosity: 1               # 0 normal .. 4 debug, 5 WinRM debug
    diff_mode: true
    timeout: 3600              # seconds
    ask_limit_on_launch: true
    ask_job_type_on_launch: true
    ask_verbosity_on_launch: true
```

## Job type
- `check` = `ansible-playbook --check`: dry run for approvals or drift reports. Same check-mode caveats (skipped commands).
- A common pattern: two templates (check and run) or one template with `ask_job_type_on_launch`, and a workflow approval between them.

## Limit
- Same syntax as `--limit` (`web:&prod`, `web01,web02`).
- Workflow nodes and schedules can override when the template prompts for it.

## Forks
- Per-job parallelism, bounded by the instance group's capacity; a 200-fork job reserves that much capacity and may wait in Pending.

## Verbosity
- Level 3+ dramatically increases job event volume (DB growth, slow UI); use temporarily.
- Level 4 shows SSH commands; 5 adds WinRM debug.

## Others worth setting
`diff_mode`, `job_tags`/`skip_tags`, `job_slice_count`, `allow_simultaneous`, `use_fact_cache`, `execution_environment`, `instance_groups`, `scm_branch` (when project allows override), `extra_vars`.

## Gotchas
- Values for fields the template does not prompt for are not applied — the job runs with template
defaults (documented for extra_vars: only survey variables or `ask_variables_on_launch` are honoured).

## Verify
- [ ] Extra vars you pass are honoured (survey or prompt on launch) and dropped otherwise.

## Checked

- 2026-10-31: job type Run/Check, forks (0 uses the Ansible default), limit patterns, verbosity
  (0 through 5, Normal through WinRM Debug), timeout in seconds, Show changes, job/skip tags,
  job slicing and the prompt-on-launch fields confirmed in AAP 2.5 Using automation execution
  (job templates fields table and job object reference). `controller_job_templates` role and the
  `controller_templates` input form confirmed in the redhat-cop collection README/roles listing.
- Removed: the `ansible.controller.job_template` module example (module docs on console.redhat.com
  are not fetchable; replaced with the confirmed role input form) and the "(5)" default-forks figure.
Method: documentation only; no commands were run.
