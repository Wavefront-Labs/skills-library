---
id: computing-software.cloud-infrastructure-engineering.ansible.check-mode-drift-reports-and-git-triggered-reconciliation
name: check-mode-drift-reports-and-git-triggered-reconciliation
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, drift-detection, drift-report, gitops-eda, event-driven-ansible, gitops]
level: advanced
status: docs-checked
description: "Produce drift reports from scheduled check-mode runs (JSON callback output) and trigger a controller workflow from git pushes through an Event-Driven Ansible webhook source."
sources: ["https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_checkmode.html", "https://docs.ansible.com/ansible/latest/collections/ansible/posix/json_callback.html", "https://github.com/ansible/event-driven-ansible", "https://ansible.readthedocs.io/projects/rulebook/en/latest/sources.html", "https://ansible.readthedocs.io/projects/rulebook/en/latest/actions.html", "https://docs.ansible.com/ansible/latest/reference_appendices/config.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Check-mode drift reports and git-triggered reconciliation

## Drift report from check mode
```bash
ANSIBLE_STDOUT_CALLBACK=ansible.posix.json \
  ansible-playbook -i inventories/prod site.yml --check --diff > drift.json
```
- `ANSIBLE_STDOUT_CALLBACK` is the environment form of `stdout_callback` (default `default`); only one callback can own stdout.
- `ansible.posix.json` is in the `ansible.posix` collection (not ansible-core) and turns all events into JSON on stdout. `json_indent` (default 4; `<= 0` writes a single line) controls formatting.
- The docs name `.plays[].tasks[].task.id` and say strategies such as `free` or `host_pinned` repeat a task object once per host result, so parse by task id rather than assuming one object per task. Inspect a real `drift.json` to build your own report; this skill does not specify the rest of the schema.
- In check mode a module that supports it reports the changes it would make; a module that does not support check mode reports nothing and does nothing. Tasks with conditionals on registered results produce no output, so a clean report is evidence, not proof.
- Tasks with `check_mode: false` run for real even under `--check`: keep them read-only. `ansible_check_mode` is true during a check run and can skip or soften risky tasks.
- Publish the extracted per-host changed tasks as an artifact or post it to chat, and trend the counts over time.

## Git push to workflow with EDA
The `ansible.eda.webhook` source has moved to ansible-rulebook as a builtin: new rulebooks should use `eda.builtin.webhook` (the `ansible.eda` names remain mapped for compatibility but are no longer maintained there).
```yaml
# rulebooks/gitops.yml
- name: Reconcile on merge to main
  hosts: all
  sources:
    - eda.builtin.webhook:
        host: 0.0.0.0
        port: 5000
        hmac_secret: "{{ webhook_secret }}"
  rules:
    - name: Push to main
      condition: event.payload.ref == "refs/heads/main"
      action:
        run_workflow_template:
          name: Reconcile prod
          organization: Platform
          job_args:
            extra_vars:
              commit: "{{ event.payload.after }}"
```
- Webhook source options: `host` (default `0.0.0.0`), `port` (required), optional `token` (Bearer), optional `hmac_secret` with `hmac_algo` (default `sha256`), `hmac_header` (default `x-hub-signature-256`) and `hmac_format` (`hex` or `base64`, default `hex`), plus TLS `certfile`/`keyfile`/`cafile`. The body is placed under the `payload` key of the event.
- `run_workflow_template` takes `name` and `organization` (both required), `job_args` (survey answers and extra vars go in nested `extra_vars`; event data is added to `extra_vars` automatically), and `include_events` (default true; set it false if the workflow template has no Prompt on Launch for Extra Variables and no survey). It needs the `--controller-url` option plus `--controller-token` or `--controller-username`/`--controller-password` on ansible-rulebook.
- The payload field names (`ref`, `after`) come from your git provider's push payload; check that provider's webhook docs, they are not specified by Ansible's docs.
- Design the workflow to check first (report) and then run, but confirm the controller-side steps in your controller's own documentation.

## Pull vs push
A scheduled check run plus the webhook-triggered workflow covers both: changes apply on merge and drift made outside git is reported on a schedule.

## Gotchas
- Auto-remediating every drift can fight legitimate emergency changes; alert first, remediate selected roles.
- Verify webhook authenticity (`token` or HMAC) and do not run arbitrary refs from payloads without checks.

## Verify
- [ ] A manual change on a host appears in the next drift report; a merge triggers exactly one reconcile run.

## Checked
Date: 2026-11-07. Pages read in full: "Validating tasks: check mode and diff mode", the ansible.posix.json callback page, the ansible-rulebook sources page's `eda.builtin.webhook` section and the `run_workflow_template` section of the actions page (the rest of those two long pages was only searched), and the README of ansible/event-driven-ansible (plugin migration notes). The config page was searched only for `ANSIBLE_STDOUT_CALLBACK`/`stdout_callback` (default `default`, one stdout callback).
Corrected: the webhook source moved from `ansible.eda.webhook` to `eda.builtin.webhook` (README); the HMAC options are now documented instead of an undocumented "validate HMAC" remark.
Removed as not on a cited page: the `jq` one-liners and the `.plays[].tasks[].hosts`/`.stats` JSON shape, the AAP job_host_summaries API path, "check-type job template", "AAP event streams in 2.5", and the claim that commands without check support show as skipped (the docs say such modules report nothing).
Method: documentation only; no commands were run.
