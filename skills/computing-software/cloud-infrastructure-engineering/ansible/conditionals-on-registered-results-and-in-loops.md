---
id: computing-software.cloud-infrastructure-engineering.ansible.conditionals-on-registered-results-and-in-loops
name: conditionals-on-registered-results-and-in-loops
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, conditionals, registered-conditionals, rc-check, when-in-loop, conditional-loop, status-tests]
level: practitioner
status: docs-checked
description: "Write when conditions on registered results (rc, stdout, status tests) and inside loops, where when is evaluated per item, and skip a whole loop correctly."
sources: ["https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_conditionals.html#conditions-based-on-registered-variables", "https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_conditionals.html#using-conditionals-in-loops", "https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_tests.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Conditionals on registered results and in loops

## On registered results
```yaml
- name: Probe for existing cluster
  ansible.builtin.command: pcs status
  register: pcs
  failed_when: false
  changed_when: false

- name: Bootstrap cluster
  ansible.builtin.command: pcs cluster setup ...
  when: pcs.rc != 0

- name: Note degraded nodes
  ansible.builtin.debug:
    msg: degraded
  when: "'OFFLINE' in pcs.stdout"

- name: Show first line
  ansible.builtin.debug:
    msg: "first line {{ pcs.stdout_lines[0] }}"
  when: pcs.stdout_lines | length > 0
```
A registered variable always holds the task's status and any output. Documented status tests:
```yaml
when: result is failed      # also: succeeded (older names success / fail still valid), skipped, changed
when: result is not changed
```
To condition on a failure, let the task fail softly with `ignore_errors: true` or `failed_when: false`;
otherwise Ansible stops the host before your `when` runs. Empty output is checked with
`when: contents.stdout == ""`. If a registered result is a list you can loop over it; otherwise use
`stdout_lines` or `stdout.split()`.

## In loops: evaluated per item
```yaml
- name: Install only packages not marked absent
  ansible.builtin.package:
    name: "{{ item.name }}"
  loop: "{{ packages }}"
  when: item.state | default('present') == 'present'
```
Ansible processes the condition separately for each item, so the task runs for some items and is
skipped for others.

To skip the whole task when the loop variable is undefined, give the loop an empty default:
```yaml
  loop: "{{ mylist | default([]) }}"
# for a dict
  loop: "{{ query('dict', mydict | default({})) }}"
```

## Conditions on a registered loop
```yaml
- ansible.builtin.command: "systemctl is-enabled {{ item }}"
  loop: [nginx, redis]
  register: enabled
  failed_when: false
  changed_when: false
- ansible.builtin.service:
    name: "{{ item.item }}"
    enabled: true
  loop: "{{ enabled.results }}"
  when: item.rc != 0
```

## Gotchas
- Ansible registers something for every host even when the task failed or was skipped. To run a
  follow-up on such hosts, test `is skipped` (not "undefined" or "default"), and in conditions that read
  `r.rc` guard with `r is not skipped`.
- Non-boolean variables such as strings like `"yes"` need `| bool` in conditions (see the booleans skill).
- `when` is a raw Jinja2 expression: do not wrap it in `{{ }}`.

## Verify
- [ ] Run once with the condition true and once false (`-e`), then compare skip and changed counts in the recap.

## Checked
Checked 2026-10-23 against ansible-documentation (playbooks_conditionals.rst: registered variables, loops and
conditionals; playbooks_tests.rst). Confirmed status tests, per-item evaluation, the `default([])` idiom and the
`is skipped` advice. Removed unconfirmed claims: grep return-code meaning, the exact missing-attribute error text and
that `when` cannot guard a `loop` expression.
Method: documentation only; no commands were run.
