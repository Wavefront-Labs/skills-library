---
id: computing-software.cloud-infrastructure-engineering.ansible.delegate-to-and-run-once-on-blocks
name: delegate-to-and-run-once-on-blocks
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, blocks, block-delegate, delegation, run-once]
level: practitioner
status: docs-checked
description: "Put delegate_to, run_once and become on a block so a group of tasks runs on one host or a remote API host, and handle register and failure semantics."
sources: ["https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_delegation.html", "https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_strategies.html#running-on-a-single-machine-with-run-once", "https://github.com/ansible/ansible/blob/devel/lib/ansible/playbook/block.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# delegate_to and run_once on blocks

```yaml
- name: Load balancer maintenance for this host
  delegate_to: "{{ groups['lb'] | first }}"
  become: true
  block:
    - name: Drain backend
      ansible.builtin.command: "haproxyctl disable server web/{{ inventory_hostname }}"
    - name: Wait for sessions to drain
      ansible.builtin.wait_for:
        timeout: 30
```
`Block` accepts `delegate_to` (it is one of its delegation keywords), and tasks inherit block
keywords. As always with delegation, the action runs on the delegated host but the information is
still that of the original host in the task, so `inventory_hostname` remains the web node.

## run_once on a block
```yaml
- name: One-time cluster bootstrap
  run_once: true
  block:
    - ansible.builtin.command: /opt/app/bin/schema-init
    - ansible.builtin.command: /opt/app/bin/seed-data
```
`run_once` runs a task on the first host in the current batch and applies all results and facts to
all hosts in that batch. Used with `serial`, `run_once` tasks run on one host in each serial batch; to
run once regardless of `serial`, use `when: inventory_hostname == ansible_play_hosts_all[0]`.
Any `when` on a `run_once` task is evaluated with the first host's variables only.

## Combined: once, on another host
```yaml
- name: Create DNS records via API
  run_once: true
  delegate_to: localhost
  become: false
  block:
    - ansible.builtin.uri:
        url: "{{ dns_api }}/records"
        method: POST
```
To run on a specific host instead of the first in the batch, delegate the `run_once` task.

## Semantics to know
- Results and facts of a `run_once` task are applied to all hosts in the batch; set
  `delegate_facts: true` on the task or block to avoid setting facts for all hosts.
- Connection variables come from the delegated host (`ansible_host` and the other connection
  variables reflect the host the task is delegated to), and `become` plugin options are templated from the delegated host too.

## Gotchas
- A play-level `become: true` also applies to a block delegated to localhost: set `become: false` on the block.
- Delegation does not change parallelism: forks writing to the same delegated file can overwrite each
  other; `run_once` with a loop, `serial: 1` or `throttle: 1` are the documented fixes.

## Verify
- [ ] Run with `-vv` and confirm each task's output shows the delegation target.

## Checked
Checked 2026-10-23 against ansible-documentation (playbooks_delegation.rst, playbooks_strategies.rst "Running on a
single machine with run_once") and ansible-core devel `playbook/block.py` (`Delegatable`). Removed unconfirmed
claims about run_once failures failing the batch, `rescue` inheriting `delegate_to`, and
`delegate_facts` inheritance on blocks in older cores.
Method: documentation only; no commands were run.
