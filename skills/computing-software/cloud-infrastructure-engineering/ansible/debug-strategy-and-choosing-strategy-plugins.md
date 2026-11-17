---
id: computing-software.cloud-infrastructure-engineering.ansible.debug-strategy-and-choosing-strategy-plugins
name: debug-strategy-and-choosing-strategy-plugins
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, strategies-forks, debug-strategy, strategy-plugins, free-strategy]
level: practitioner
status: docs-checked
description: "Choose and configure strategy plugins (linear, free, host_pinned, debug) per play or in ansible.cfg, list them with ansible-doc, and use the debug strategy."
sources: ["https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_strategies.html", "https://docs.ansible.com/ansible/latest/plugins/strategy.html", "https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_debugger.html", "https://github.com/ansible/ansible-documentation", "https://github.com/ansible/ansible"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Strategy plugins and the debug strategy

```bash
ansible-doc -t strategy -l
# ansible.builtin.debug        Executes tasks in interactive debug session
# ansible.builtin.free         Executes tasks without waiting for all hosts
# ansible.builtin.host_pinned  Executes tasks on each host without interruption
# ansible.builtin.linear       Executes tasks in a linear fashion
```

## Setting a strategy
```yaml
- hosts: web
  strategy: free
```
```ini
[defaults]
strategy = linear          # global default (linear); ANSIBLE_STRATEGY env
```

| Strategy | Behaviour | Use for |
|---|---|---|
| linear | each task on all hosts (up to forks) before the next | default, predictable output |
| free | hosts do not wait for each other to finish the current task | independent hosts, mixed speeds |
| host_pinned | like free, but a host's play is not started unless it can finish without interruption by other hosts' tasks | many hosts, few forks, long plays |
| debug | linear, controlled by an interactive debug session | interactive troubleshooting |

## debug strategy
```yaml
- hosts: web01
  strategy: debug
```
On a failed task you get a `[web01] TASK: ... (debug)>` prompt: `p task.args`, `task.args['name'] = 'nginx'`, `redo` (or `r`), `continue` (or `c`). Preferred alternative: the `debugger` keyword (`always`, `never`, `on_failed`, `on_unreachable`, `on_skipped`) on a play, role, block or task, which works with any strategy; the strategy form is described as the legacy way.

## Gotchas
- `free` interleaves output by host, so logs are harder to read.
- `serial` still applies with free: tasks run as fast as possible per batch.
- With `free` and the debugger, Ansible queues nothing while the debugger is active, but tasks already queued run as soon as you exit it.

## Verify
```bash
ansible-doc -t strategy -l      # confirm which strategy plugins are installed
```

## Checked
Date: 2026-10-24. Documentation: Ansible playbook guide, Controlling playbook execution (playbooks_strategies.rst) and Error handling (playbooks_error_handling.rst), devel; ansible-core helpers.py, play.py, special_variables.rst; Debugging tasks page (playbooks_debugger.rst); strategy plugin sources.
Confirmed:
- Strategy plugin names and short descriptions; ANSIBLE_STRATEGY and [defaults] strategy.
- Debug prompt commands (p, redo/r, continue/c) and the debugger keyword values; the strategy form is described as the legacy way; free strategy and debugger interaction.
- Removed the Mitogen paragraph and the run_once-with-free claim.

Method: documentation only; no commands were run.
