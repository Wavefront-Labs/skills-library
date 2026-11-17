---
id: computing-software.cloud-infrastructure-engineering.ansible.linear-strategy-forks-and-poll-interval
name: linear-strategy-forks-and-poll-interval
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, strategies-forks, performance-tuning, linear-strategy, forks-sizing, internal-poll-interval, forks]
level: advanced
status: docs-checked
description: "Understand the linear strategy's lockstep per task, size forks against controller CPU, memory and target load, and tune internal_poll_interval for many-host runs."
sources: ["https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_strategies.html", "https://docs.ansible.com/ansible/latest/reference_appendices/config.html", "https://docs.ansible.com/ansible/latest/tips_tricks/ansible_tips_tricks.html", "https://github.com/ansible/ansible-documentation", "https://github.com/ansible/ansible"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Linear strategy, forks and internal_poll_interval

## Linear: task-by-task lockstep
Default strategy `linear`: task 1 runs on all hosts (up to `forks` in parallel), Ansible waits for
**every** host to finish it, then task 2 starts. One slow host holds everybody at each task.
Alternatives: `strategy: free` (a slow host does not hold up the others), `host_pinned` (like free, but a play is started for a host only if it can finish without interruption, so active hosts never exceed forks), `debug`.

## Forks
`forks` (default **5**) = max parallel worker processes on the controller.
```ini
[defaults]
forks = 50
```
`-f 50` on the CLI, or `ANSIBLE_FORKS`.

Sizing:
- Each fork is a worker process on the controller, so memory and CPU on the controller bound it; measure rather than guess.
- Targets: forks also bound concurrent connections to targets, so mind sshd connection limits on bastions and API rate limits for cloud or network modules (use `throttle:` per task, which can only lower parallelism).

Measure: run with several fork counts and `callbacks_enabled = ansible.posix.profile_tasks` (`callbacks_enabled` is the option name from 2.11); stop raising forks when wall time stops dropping.

## internal_poll_interval
`[defaults] internal_poll_interval` (float, default 0.001 s, added in 2.2) sets how often Ansible's internal processes poll each other. Lower values improve performance with large playbooks at the cost of extra CPU load; higher values suit automation scenarios where UI responsiveness is not needed but CPU usage is a concern. Leave the default unless profiling shows controller CPU contention.

Different setting: `poll` on async tasks (seconds between job status checks on targets).

## Other levers
- `pipelining = True` (under `[defaults]` or `[connection]`; default False): fewer network operations per module. It conflicts with `become` when sudo requires a tty (`requiretty`).
- The ssh plugin default `ssh_args` already include `ControlMaster=auto` and `ControlPersist=60s`.
- `gather_facts: false` or a smaller `gather_subset`; fact caching.

## Gotchas
- `serial` smaller than `forks` caps parallelism at the batch size.
- With `strategy: free`, hosts do not wait for each other, so do not assume all hosts finished task X.

## Verify
- [ ] `profile_tasks` (enabled via `callbacks_enabled`) before and after shows lower total time, and controller load stays acceptable during the run.

## Checked
Date: 2026-10-24. Documentation: Ansible playbook guide, Controlling playbook execution (playbooks_strategies.rst) and Error handling (playbooks_error_handling.rst), devel; ansible-core helpers.py, play.py, special_variables.rst; ansible-core config/base.yml, strategy plugin sources, ssh connection plugin.
Confirmed:
- Default forks 5 and strategy linear; internal_poll_interval default 0.001, float, added 2.2, behaviour description.
- free and host_pinned semantics (strategy plugin docs); pipelining default False with ini sections defaults and connection; ssh_args default includes ControlMaster=auto and ControlPersist=60s; callbacks_enabled added 2.11.
- Removed RAM-per-fork, MaxStartups, time-model and Mitogen statements that no Ansible doc covers.

Method: documentation only; no commands were run.
