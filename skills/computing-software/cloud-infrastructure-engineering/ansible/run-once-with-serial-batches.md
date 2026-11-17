---
id: computing-software.cloud-infrastructure-engineering.ansible.run-once-with-serial-batches
name: run-once-with-serial-batches
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, delegation, run-once-serial, run-once, serial, rolling-update]
level: advanced
status: docs-checked
description: "Understand that run_once runs once per serial batch, and make a task truly once per play with a guard on ansible_play_hosts_all or a separate play."
sources: ["https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_strategies.html", "https://github.com/ansible/ansible-documentation", "https://github.com/ansible/ansible"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# run_once with serial batches

`run_once: true` runs the task on the first host of the **current batch** and applies the result
to all hosts in that batch. With `serial`, each batch is a mini-play, so the task runs once
**per batch**.

```yaml
- hosts: web            # 10 hosts
  serial: 2             # 5 batches
  tasks:
    - name: Run DB migration
      ansible.builtin.command: /opt/app/bin/migrate
      run_once: true    # runs 5 times!
```

## Truly once per play
Option 1 — guard on the first host of the whole play:
```yaml
- name: Run DB migration once
  ansible.builtin.command: /opt/app/bin/migrate
  when: inventory_hostname == ansible_play_hosts_all[0]
```
`ansible_play_hosts_all` is the full list regardless of batch. Note it only fires in the batch that
contains that host (the first batch with default ordering) — usually what you want for "before
rollout". For "after rollout", compare with `ansible_play_hosts_all[-1]`.

Option 2 — separate play (clearest):
```yaml
- hosts: db_migrator[0]     # or web[0]
  tasks:
    - ansible.builtin.command: /opt/app/bin/migrate

- hosts: web
  serial: 2
  tasks: ...
```

Option 3 — idempotent task: if the migration tool is a no-op when up to date, running it per
batch is harmless; still wasteful.

## Run once per batch on purpose
Per-batch actions where run_once is exactly right: take the batch out of the LB in one API call,
post a "starting batch N" message, warm a cache shared by the batch.
```yaml
- name: Announce batch
  ansible.builtin.debug:
    msg: "Deploying to {{ ansible_play_batch | join(', ') }}"
  run_once: true
```

## Gotchas
- `run_once` + `delegate_to` runs on the delegate once per batch.
- Conditions (`when`) on a `run_once` task are evaluated with the variables of the first host only.
- `delegate_facts: true` stops the result facts being set on every host of the batch.
- `run_once` applies all results and facts to every host in the same batch.

## Verify
- [ ] The run output shows the run-once task once per batch, or exactly once with the `ansible_play_hosts_all[0]` guard.

## Checked
Date: 2026-10-24. Documentation: Ansible playbook guide, Controlling playbook execution (playbooks_strategies.rst) and Error handling (playbooks_error_handling.rst), devel; ansible-core helpers.py, play.py, special_variables.rst.
Confirmed:
- run_once runs on the first host of each serial batch and applies results and facts to the batch; the ansible_play_hosts_all[0] guard is the documented once-per-play form; when uses the first host's variables; delegate_facts.
- Removed the claims about picking the next active host after a failure and free-strategy ordering.

Method: documentation only; no commands were run.
