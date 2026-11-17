---
id: computing-software.cloud-infrastructure-engineering.ansible.background-ad-hoc-commands-with-async
name: background-ad-hoc-commands-with-async
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, ad-hoc, ad-hoc-background, ad-hoc-async, async-status]
level: practitioner
status: docs-checked
description: "Run long ad hoc commands in the background with -B and -P, check them later with async_status, and avoid SSH timeouts on long jobs."
sources: ["https://docs.ansible.com/ansible/latest/command_guide/intro_adhoc.html", "https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_async.html", "https://docs.ansible.com/ansible/latest/collections/ansible/builtin/async_status_module.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Background ad hoc commands

## Poll until done
```bash
ansible db -b -B 3600 -P 30 -m ansible.builtin.dnf -a 'name=* state=latest'
```
`-B 3600` is the maximum runtime in seconds (the process on the remote node is terminated when it
runs out); `-P 30` polls for status every 30 seconds. Poll mode starts all jobs before polling any
machine, so use a high enough `--forks` to start them quickly.

## Fire and forget, check later
```bash
ansible db -b -B 7200 -P 0 -m ansible.builtin.command -a '/usr/local/bin/reindex.sh'

ansible db01 -b -m ansible.builtin.async_status -a 'jid=<job id from the output>'
ansible db01 -b -m ansible.builtin.async_status -a 'jid=<job id from the output> mode=cleanup'
```
The first command returns an `ansible_job_id` per host (and `started`, `results_file`); job ids
differ per host.

## Rules
- Run `async_status` as the same user as the job: the default job directory `~/.ansible_async` is
  expanded for the user running the task (set `ansible_async_dir` to use a fixed path).
- If the job exceeds `-B`, it is killed and the result is `"msg": "Timeout exceeded"`.
- `async_status` is also supported for Windows targets.

## Gotchas
- `-P 0` jobs leave their job files behind; remove them with `mode=cleanup`. (With polling, the
  file is removed automatically when the job completes.)
- Async mode suits long-running shell commands and upgrades; running `copy` asynchronously does not
  do a background file transfer.
- The default poll interval, used when no poll is given, comes from `DEFAULT_POLL_INTERVAL`
  (15 seconds).

## Verify
- [ ] `async_status` reports finished (a boolean from ansible-core 2.19, `1` before) and the module's `rc`.

## Checked
Checked 2026-10-23 against ansible-documentation (playbooks_async.rst) and ansible-core devel sources
(`async_status`, `async_wrapper`, config `DEFAULT_POLL_INTERVAL`). Confirmed: `-B`/`-P` meaning, the
documented `ansible all -B 3600 -P 0` form, cleanup rules, `Timeout exceeded`, Windows support, 15 second
default. Removed unconfirmed claims about network connection plugins, `ansible.windows.async_status`
and a reboot killing jobs.
Method: documentation only; no commands were run.
