---
id: computing-software.cloud-infrastructure-engineering.ansible.serial-batches-with-failure-thresholds
name: serial-batches-with-failure-thresholds
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, strategies-forks, serial-failure-handling, max-fail-percentage, any-errors-fatal, rolling-update]
level: advanced
status: docs-checked
description: "Combine serial with max_fail_percentage and any_errors_fatal for safe rolling updates: how batch failures abort the play and how thresholds round."
sources: ["https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_strategies.html", "https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_error_handling.html", "https://github.com/ansible/ansible-documentation", "https://github.com/ansible/ansible"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# serial with failure thresholds

```yaml
- hosts: web
  serial: [1, "10%", "25%"]
  max_fail_percentage: 20
  tasks: [...]
```

## How it works
- `serial` splits the play into batches; each batch runs all tasks (and handlers) before the next.
- `max_fail_percentage` is checked **per batch**: if failed hosts in the batch exceed the percentage, the whole play aborts and later batches never start.
- The percentage must be exceeded, not equalled: with batch size 10 and `max_fail_percentage: 20`, 2 failures continue and 3 abort. Set `0` to abort on the first failure in any batch.
- `any_errors_fatal: true` (play or block level): when a task fails, Ansible finishes that task on all hosts in the current batch, then stops the play on all hosts. A `rescue` section can recover.

## Without thresholds
By default Ansible keeps executing as long as there are hosts that have not failed, and `serial` scopes failures to the batch. So with no `max_fail_percentage`, the play stops only when every host of a batch has failed; a bad change can roll across the fleet with one failure per batch.

## Canary pattern
```yaml
serial: [1, 5, "100%"]
max_fail_percentage: 0
```
First host alone, then 5, then the rest; any failure halts.

## Health gates between batches
Add post-task checks in the play (`uri` health endpoint with `until`) so "failure" means "unhealthy", not just "task error".

## Gotchas
- Percentages in `serial` truncate to a whole host count, minimum 1.
- `ignore_unreachable` and `max_fail_percentage` are the documented ways to change how batch-scoped failures behave.

## Verify
- [ ] Inject a failing task in staging and confirm the play aborts after the first batch.

## Checked
Date: 2026-10-24. Documentation: Ansible playbook guide, Controlling playbook execution (playbooks_strategies.rst) and Error handling (playbooks_error_handling.rst), devel; ansible-core helpers.py, play.py, special_variables.rst.
Confirmed:
- Per-batch max_fail_percentage, exceed-not-equal rule, any_errors_fatal behaviour and rescue recovery, default continue-while-hosts-remain behaviour.
- Removed the unreachable and ignore_errors counting claims and the retry-file advice (not documented).

Method: documentation only; no commands were run.
