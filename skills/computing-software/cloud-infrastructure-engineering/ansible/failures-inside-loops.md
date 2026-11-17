---
id: computing-software.cloud-infrastructure-engineering.ansible.failures-inside-loops
name: failures-inside-loops
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, error-handling, loop-failures, loops, ignore-errors]
level: practitioner
status: docs-checked
description: "Handle failures inside loops: one failed item fails the task after all items run, inspect per-item results, ignore_errors per loop, and fail on aggregate conditions."
sources: ["https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_error_handling.html", "https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_loops.html", "https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_loops.html#registering-variables-with-a-loop"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Failures inside loops

## Registering loop results
With `register` on a looped task, the variable has a `results` list with one entry per item
(each entry includes `item`). Ansible evaluates `changed_when`, `failed_when` and similar
conditionals per item, with the current item's result in the registered variable.

## Collect, then decide
```yaml
- name: Check endpoints
  ansible.builtin.uri:
    url: "https://{{ item }}/health"
  loop: "{{ endpoints }}"
  register: health
  ignore_errors: true

- name: Fail if more than one endpoint is down
  ansible.builtin.fail:
    msg: "Down: {{ health.results | selectattr('failed') | map(attribute='item') | list }}"
  when: (health.results | selectattr('failed') | list | length) > 1
```
`ignore_errors` only applies when the task runs and returns `failed`; it does not hide undefined
variable errors, connection failures or syntax errors.

## Per-item failed_when
```yaml
- ansible.builtin.command: "systemctl is-active {{ item }}"
  loop: [nginx, php-fpm]
  register: svc
  changed_when: false
  failed_when: svc.rc != 0 and item != 'php-fpm'     # php-fpm allowed to be down
```

## Stopping early
`loop_control` has `break_when` (added in ansible-core 2.18): a list or expression evaluated after
each item that exits the loop when true. Other options:
- A module that takes a list (packages) so the whole set is one task.
- `block`/`rescue` inside an included task file that is looped, for per-item handling.

## Gotchas
- `ignore_errors` on a looped task covers all items; always follow it with an explicit check.
- In `rescue`, `ansible_failed_result` is the failed task's captured result.
- `loop_control: label` keeps output readable for large dict items.

## Verify
- [ ] Simulate one bad item and confirm the aggregate check reports exactly that item.

## Checked
Checked 2026-10-23 against ansible-documentation (playbooks_loops.rst "Registering variables with a loop"
and `break_when`; playbooks_error_handling.rst). Fixed: the old claim "loops cannot break" is stale
(`break_when`, 2.18). Removed unconfirmed claims about default failure ordering across items, the
`ansible_failed_result.results` contents and an `any_errors_fatal` include recipe.
Method: documentation only; no commands were run.
