---
id: computing-software.cloud-infrastructure-engineering.ansible.forks-and-control-node-capacity
name: forks-and-control-node-capacity
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, strategies-forks, forks-memory, forks, performance]
level: practitioner
status: docs-checked
description: "Size forks against control node memory, CPU and SSH limits: measure per-fork cost, avoid OOM kills, and tune MaxStartups on bastions for high parallelism."
sources: ["https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_strategies.html#setting-the-number-of-forks", "https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_delegation.html", "https://github.com/ansible-collections/ansible.posix/blob/main/plugins/callback/cgroup_perf_recap.py", "https://github.com/openssh/openssh-portable/blob/master/sshd_config.5"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Forks vs control node capacity

`forks` (default 5) is the maximum number of forks Ansible uses to run tasks on target hosts in parallel (`ansible.cfg` `forks`, `ANSIBLE_FORKS`, `-f`). The docs' example raises it to 30 when processing power allows.

## Measure the cost
The `ansible.posix.cgroup_perf_recap` callback profiles CPU, memory and PID use of the whole run and of each task. It must be enabled (`callbacks_enabled`), needs cgroups, and requires Ansible to run inside a dedicated control group named by `CGROUP_CONTROL_GROUP` (the plugin notes show `cgexec -g cpuacct,memory,pids:ansible_profile ansible-playbook ...`). Measure peak memory at a few fork counts on your largest inventory rather than relying on a per-fork rule of thumb.

## Sizing
- Raise `forks` in steps from the default 5 and measure control-node memory and CPU at each step; stop before the node swaps.
- Automation controller derives job capacity from instance resources; check its documentation rather than these notes (not confirmed here).

## SSH side limits
- Through a bastion, many forks open many connections at once. OpenSSH `sshd_config` `MaxStartups` limits concurrent unauthenticated connections (default `10:30:100`: random early drop starts at 10, refuses all at 100); extra connections are dropped, which can surface as `UNREACHABLE`. Raising it on the bastion is a local policy decision (for example `200:30:400`). `MaxSessions` (default 10) limits open sessions per network connection, which matters for multiplexed connections.

## Where forks do not help
- `serial: 5` completes the play on 5 hosts at a time, so at most 5 run in parallel whatever `forks` says.
- `throttle` limits the workers for a task or block; it can only lower the effective parallelism, not raise it above `forks` or `serial`.
- A task delegated to one host still runs in parallel forks for all hosts and can overwrite its own results (for example editing one file); use `run_once` or a loop, or `throttle: 1`.

## Gotchas

## Verify
- [ ] Peak RSS and swap stay within limits at the chosen forks on the largest inventory.

## Checked
Checked 2026-10-25 against ansible-documentation devel (commit of 2026-10-21) playbook_guide/playbooks_strategies.rst and playbooks_delegation.rst, ansible-core `config/base.yml` (DEFAULT_FORKS default 5), the ansible.posix `cgroup_perf_recap` callback source, and the OpenSSH `sshd_config(5)` source from openssh-portable (MaxStartups default 10:30:100, MaxSessions default 10 per network connection). Confirmed: forks default and settings, `serial` and `throttle` semantics, cgroup callback requirements, sshd limits. Corrected the claim that delegated and run_once tasks serialise on the controller (delegated tasks still run in parallel forks). Removed unconfirmed per-fork memory figures, vCPU ratios, controller capacity settings, `ulimit`, OOM and cache advice.
Method: documentation only; no commands were run.
