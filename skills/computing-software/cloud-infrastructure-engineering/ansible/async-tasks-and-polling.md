---
id: computing-software.cloud-infrastructure-engineering.ansible.async-tasks-and-polling
name: async-tasks-and-polling
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, async, poll, async-status, fire-and-forget, background-tasks, long-running-tasks, async-dir, timeouts, task-timeout, reboot-module, wait-for-connection, concurrency, parallel-tasks, async-cleanup]
level: practitioner
status: docs-checked
description: "Run long or parallel Ansible tasks with async/poll: fire-and-forget, poll later with async_status, run N jobs per host concurrently, set task timeouts, and clean up async job files."
sources: ["https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_async.html", "https://docs.ansible.com/ansible/latest/collections/ansible/builtin/async_status_module.html", "https://docs.ansible.com/ansible/latest/collections/ansible/builtin/reboot_module.html", "https://docs.ansible.com/ansible/latest/reference_appendices/config.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Async tasks and polling

**Goal:** a long upgrade, a reboot, or several independent jobs per host do not hold the SSH session
open and still report success or failure.

## 1. The two modes
```yaml
# A. Long task: keep waiting, but with a longer limit than the connection allows
- ansible.builtin.command: /opt/db/upgrade.sh
  async: 3600      # maximum runtime in seconds
  poll: 30         # check every 30 s; the task still blocks the play
```
```yaml
# B. Fire and forget, collect later
- ansible.builtin.command: /opt/app/reindex.sh
  async: 7200
  poll: 0
  register: reindex
- ansible.builtin.debug:
    msg: other tasks run here
- ansible.builtin.async_status:
    jid: "{{ reindex.ansible_job_id }}"
  register: job
  until: job is finished
  retries: 240
  delay: 30
```
- There is no default for `async`; without it the task runs synchronously. The default `poll`
  comes from the `DEFAULT_POLL_INTERVAL` setting (15 seconds, `poll_interval` in `[defaults]`).
- With `poll: 0` the task returns at once with `ansible_job_id`; the play ends without checking back.
- `async_status` has `mode: status` (default) and `mode: cleanup`. Its `started`/`finished` return
  values are booleans from ansible-core 2.19 (they were `1`/`0` before), so use `job is finished`.
- Async tasks always report changed; if the module needs `changed_when` or `creates`, put those on
  the `async_status` task.

## 2. Concurrency inside one host
Start several `poll: 0` tasks, then wait for all (full loop pattern in the async-in-loops skill):
```yaml
- ansible.builtin.command: "backup.sh {{ item }}"
  async: 1800
  poll: 0
  loop: "{{ databases }}"
  register: jobs
- ansible.builtin.async_status:
    jid: "{{ item.ansible_job_id }}"
  loop: "{{ jobs.results }}"
  loop_control:
    label: "{{ item.item }}"
  register: done
  until: done is finished
  retries: 60
  delay: 30
```
The docs also show limiting concurrency by looping over `list | batch(N) | list` with `include_tasks`.

## 3. Where the job lives
Job information is kept in the shell plugin option `async_dir` (default `~/.ansible_async`; set with
`ansible_async_dir`, `ANSIBLE_ASYNC_DIR` or `async_dir` in `[defaults]`) on the managed node.
With `poll > 0` the job file is removed automatically when the task completes; with `poll: 0` you
must remove it with `async_status` and `mode: cleanup`. If `async` is too low, the later
`async_status` task fails because the status file was never written or no longer exists.

## 4. Reboots
```yaml
- ansible.builtin.reboot:
    reboot_timeout: 600
```
`reboot` waits for the host to come back and runs a `test_command` (default `whoami`) before
continuing; `reboot_timeout` defaults to 600 seconds and applies separately to the reboot check and
the test command. Use it instead of `shell: reboot` plus a manual wait.

## 5. Timeouts
- When the `async` limit is exceeded the wrapper kills the job and reports `Timeout exceeded`.
- The task keyword `timeout` and the setting `task_timeout` in `[defaults]` (`ANSIBLE_TASK_TIMEOUT`,
  default 0 = none, added in 2.10) cap a task action's execution time per attempt.

## Gotchas
- Do not use `poll: 0` for operations that need exclusive locks (such as yum transactions) if later
  tasks use the same resources.
- Async is for long-running commands and upgrades; running `copy` asynchronously does not make a
  background file transfer.
- Async tasks do not support check mode and fail when run in it; skip them with `when: not ansible_check_mode`.
- A higher `--forks` starts async jobs faster and makes polling more efficient.

## Checked
Checked 2026-10-23 against the ansible-documentation playbook guide (playbooks_async.rst), the
ansible-core devel sources for `async_status`, `async_wrapper`, `reboot`, the shell option
fragment and `config/base.yml` (devel is 2.23 dev). Confirmed: `async`/`poll` semantics, default poll
interval 15, `async_dir` default and its variable/env/ini names, cleanup rules, boolean `finished`
since 2.19, `Timeout exceeded` message, `task_timeout` default and `version_added` 2.10, `reboot`
defaults (`reboot_timeout` 600, `test_command` `whoami`). Removed unconfirmed claims about process
survival across SSH loss and reboots, and `get_url` async behaviour.
Method: documentation only; no commands were run.
