---
id: computing-software.cloud-infrastructure-engineering.ansible.long-running-tasks-with-async-and-wait
name: long-running-tasks-with-async-and-wait
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, async-polling, async-long-running, async, poll]
level: practitioner
status: docs-checked
description: "Run long package upgrades, backups and builds with async and poll so SSH timeouts and dropped sessions do not kill them, choosing async limits and poll intervals."
sources: ["https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_async.html", "https://docs.ansible.com/ansible/latest/collections/ansible/builtin/async_status_module.html", "https://github.com/ansible/ansible-documentation", "https://github.com/ansible/ansible"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Long-running tasks with async

By default Ansible holds the connection to the remote node open until a task completes, so a task that outlasts the SSH session can time out. Async mode starts the action in the background on the target and checks on it by polling (or lets you check later).

```yaml
- name: Full OS upgrade (may take 40 minutes)
  ansible.builtin.dnf:
    name: "*"
    state: latest
  async: 3600        # maximum runtime in seconds; the job is terminated after this
  poll: 30           # check status every 30s (default comes from DEFAULT_POLL_INTERVAL, 15 s)
  become: true
```

## Choosing values
- `async`: set above the worst observed runtime; the task fails if it exceeds the limit. There is no default async limit: without `async` the task runs synchronously.
- `poll`: with `poll` greater than 0 Ansible still blocks the next task until the async task completes, fails or times out, and in most cases keeps the connection open between polls.
- `poll: 0` starts the task and moves on immediately; use `async_status` later if you need a synchronisation point.

## Start now, collect later
```yaml
- name: Kick off database backup
  ansible.builtin.command: /usr/local/bin/pg-backup.sh
  async: 7200
  poll: 0
  register: backup_job

- name: Other work meanwhile
  ansible.builtin.include_tasks: housekeeping.yml

- name: Wait for backup to finish
  ansible.builtin.async_status:
    jid: "{{ backup_job.ansible_job_id }}"
  register: backup_result
  until: backup_result.finished
  retries: 240
  delay: 30

- name: Remove the job cache file
  ansible.builtin.async_status:
    jid: "{{ backup_job.ansible_job_id }}"
    mode: cleanup
```

## Task timeout vs async
`timeout:` (task keyword, default from `TASK_TIMEOUT`, 0 = no limit) sets the maximum time for a task action; Ansible interrupts it when exceeded, per attempt. `async` is the background-execution limit with polling. Use `timeout` for hung tasks, async for legitimately long ones.

## Gotchas
- Async suits long shell commands and software upgrades; running `copy` asynchronously does not do a background file transfer.
- Async does not support check mode (since 2.3 it fails the task in check mode); skip such tasks when `ansible_check_mode` is true.
- Do not use `poll: 0` for operations that need exclusive locks (such as yum transactions) if later tasks use the same resources.
- With polling, the job cache file (by default under `~/.ansible_async/`) is removed automatically; with `poll: 0` it is not, so run `async_status` with `mode: cleanup`.
- Higher `--forks` starts async tasks faster and makes polling more efficient.
- Since ansible-core 2.19 `async_status` returns `finished` and `started` as booleans (earlier releases returned 1 and 0).

## Verify
- [ ] `backup_result.rc == 0` and `backup_result.finished` is true (1 on releases before ansible-core 2.19).

## Checked
Date: 2026-10-24. Documentation: Ansible playbook guide, Asynchronous actions and polling (playbooks_async.rst), async_status module docs, config/base.yml, devel.
Confirmed:
- poll greater than 0 blocks and usually keeps the connection open; poll 0 fires and forgets; no default async limit; DEFAULT_POLL_INTERVAL 15; async fails in check mode; cache file cleaned automatically only with polling, otherwise async_status mode cleanup.
- TASK_TIMEOUT semantics; async_status finished and started became booleans in 2.19.
- Removed the error-message text, polling-range advice, copy/template/include claims and the reboot claim.

Method: documentation only; no commands were run.
