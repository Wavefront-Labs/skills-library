---
id: computing-software.cloud-infrastructure-engineering.ansible.handlers-with-run-once-and-delegate-to
name: handlers-with-run-once-and-delegate-to
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, handlers, handler-run-once, handler-delegate, delegation, run-once]
level: advanced
status: docs-checked
description: "Use run_once and delegate_to on handlers, e.g. reload a load balancer once when any backend changed, and avoid the per-host notification pitfalls."
sources: ["https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_handlers.html", "https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_delegation.html", "https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_strategies.html#running-on-a-single-machine-with-run-once", "https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_error_handling.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Handlers with run_once and delegate_to

Handlers are per host: they run on each host that was notified. Both keywords work on handlers
like on tasks.

## Reload a shared service once
```yaml
handlers:
  - name: Reload haproxy
    ansible.builtin.service: {name: haproxy, state: reloaded}
    delegate_to: "{{ item }}"
    loop: "{{ groups['lb'] }}"
    run_once: true

tasks:
  - name: Register backend in haproxy map
    ansible.builtin.lineinfile:
      path: /etc/haproxy/backends.map
      line: "{{ inventory_hostname }} {{ ansible_host }}"
    delegate_to: "{{ groups['lb'][0] }}"
    notify: Reload haproxy
```
If 5 web hosts notify, `run_once` makes the handler execute once (the linear strategy queues it for the first notified host and then clears the other notified hosts), reloading each lb once, not 5 times.

## Semantics to remember
- `run_once` on a handler runs it once among the hosts **that notified it** in that flush; if only web3 notified, it runs in web3's context.
- Under delegation, `inventory_hostname` stays the original host; other variables, including connection, become and shell plugin options, come from the delegate host.
- With `serial`, `run_once` runs once in *each* batch, so the lb reloads per batch (use `when: inventory_hostname == ansible_play_hosts_all[0]` for once per play); usually desirable for rolling deploys.
- Notification is per host: a task delegated to the lb but run for web1 is still information about web1, so the handler is notified for **web1**, not for the lb.
- `run_once` and `delegate_to` are task keywords and `Handler` extends `Task`; `include_role` and `import_role` do not work in handlers.

## Alternative without delegation
Put the lb work in its own play after the web play:
```yaml
- hosts: lb
  tasks:
    - ansible.builtin.service: {name: haproxy, state: reloaded}
```
Clearer to read, but the reload then happens after all batches and is unconditional unless you add your own `when` based on a variable the web play sets.

## Gotchas
- With `run_once`, a handler that delegates to a single host (no loop over `groups['lb']`) reloads only that host.
- If a task fails later in the play, notified handlers do not run on that host by default; `force_handlers: True` (play), `--force-handlers` or `force_handlers = True` in ansible.cfg runs all notified handlers even on hosts with failed tasks, except for errors such as an unreachable host. Consider it here.

## Verify
- [ ] Change two backends in one run: handler output appears once per lb, not once per backend.

## Checked
Checked 2026-10-25 against ansible-documentation devel (commit of 2026-10-21) playbook_guide/playbooks_strategies.rst (run_once with serial), playbooks_delegation.rst, playbooks_handlers.rst, playbooks_error_handling.rst (force_handlers), and the ansible-core devel `plugins/strategy/linear.py` (handlers queued for the first host and notified hosts cleared when run_once) and `playbook/handler.py` (`Handler` extends `Task`). Confirmed: once-per-batch behaviour with serial, delegation variable rules, per-host notification, force_handlers options and limits. Removed an unverified hostvars-based when expression.
Method: documentation only; no commands were run.
