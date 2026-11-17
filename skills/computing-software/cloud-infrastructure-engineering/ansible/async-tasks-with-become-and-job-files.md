---
id: computing-software.cloud-infrastructure-engineering.ansible.async-tasks-with-become-and-job-files
name: async-tasks-with-become-and-job-files
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, async-polling, async-become, async-status, async-dir, job-cleanup]
level: advanced
status: docs-checked
description: "Run async tasks under become and later check them with async_status as the same user, set async_dir, and clean up job files so status checks do not fail."
sources: ["https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_async.html", "https://docs.ansible.com/ansible/latest/collections/ansible/builtin/async_status_module.html", "https://github.com/ansible/ansible/blob/devel/lib/ansible/plugins/doc_fragments/shell_common.py", "https://github.com/ansible/ansible/blob/devel/lib/ansible/plugins/action/async_status.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Async tasks with become and job files

Async jobs write status files to `async_dir` (default `~/.ansible_async`). The `async_status`
action plugin expands that path on the managed node for the user the `async_status` task runs as,
so a status task that does not use the same become setting as the launch task looks in a different
home directory.

## Fire-and-forget, check later
```yaml
- name: Start long backup as root
  ansible.builtin.command: /usr/local/bin/full-backup
  async: 7200
  poll: 0
  become: true
  register: backup_job

- name: Do other work
  ansible.builtin.debug:
    msg: working

- name: Wait for backup
  ansible.builtin.async_status:
    jid: "{{ backup_job.ansible_job_id }}"
  become: true                    # same user as the launch task
  register: job
  until: job is finished
  retries: 240
  delay: 30

- name: Clean up job file
  ansible.builtin.async_status:
    jid: "{{ backup_job.ansible_job_id }}"
    mode: cleanup
  become: true
```
Mismatch symptom: the module fails with `could not find job` because the status file is not in the
directory that `async_status` looked in.

## Setting async_dir
`async_dir` is a shell plugin option, set with the variable `ansible_async_dir`, the environment
variable `ANSIBLE_ASYNC_DIR`, or `async_dir` in `[defaults]`:
```yaml
vars:
  ansible_async_dir: /var/tmp/ansible_async
```
A fixed path makes launch and status tasks agree regardless of which user they run as.

## Gotchas
- `poll: 0` jobs are not cleaned up automatically (use `mode: cleanup`); with `poll > 0` the file is
  removed when the task completes.
- The `async` value is a time limit: the job is killed after it, reported as `Timeout exceeded`. If it is too low, the
  later status task fails because the status file was never written or no longer exists.
- Async tasks do not support check mode and fail when run in it.

## Checked
Checked 2026-10-23 against ansible-documentation (playbooks_async.rst) and ansible-core devel sources
(`async_status` action plugin and module, `async_wrapper`, shell option fragment). Confirmed: `async_dir`
default and its variable, env and ini names, `_remote_expand_user` expansion of the path, `could not find
job` failure, cleanup behaviour, `Timeout exceeded`. Removed unconfirmed claims about unprivileged-user
ACLs, `become_method: su`, NFS home directories, and what happens to jobs on reboot.
Method: documentation only; no commands were run.
