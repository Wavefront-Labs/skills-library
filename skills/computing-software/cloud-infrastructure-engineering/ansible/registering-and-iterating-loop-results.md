---
id: computing-software.cloud-infrastructure-engineering.ansible.registering-and-iterating-loop-results
name: registering-and-iterating-loop-results
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, loops, loop-results, results-list, register, loop-control, selectattr]
level: practitioner
status: docs-checked
description: "Register a looped task, then filter and iterate its results list (item, rc, changed, failed) with selectattr/map, and keep output readable with loop_control label."
sources: ["https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_loops.html", "https://github.com/ansible/ansible-documentation", "https://github.com/ansible/ansible"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Registering and iterating loop results

```yaml
- name: Check each endpoint
  ansible.builtin.uri:
    url: "https://{{ item }}/health"
    status_code: [200, 503]
  loop: [api.example.com, auth.example.com, pay.example.com]
  register: health
```
`health` is:
```json
{"changed": false, "msg": "All items completed",
 "results": [{"item": "api.example.com", "status": 200, "changed": false, ...}, ...]}
```
The top-level `changed` and `failed` are true if at least one iteration changed or failed; `skipped` is true only if all iterations were skipped.

## Filtering results
```yaml
- name: List unhealthy endpoints
  ansible.builtin.set_fact:
    unhealthy: "{{ health.results | selectattr('status', 'ne', 200) | map(attribute='item') | list }}"

- name: Fail with a summary
  ansible.builtin.fail:
    msg: "Unhealthy: {{ unhealthy | join(', ') }}"
  when: unhealthy | length > 0
```
Useful expressions:
- items that changed: `results | selectattr('changed') | map(attribute='item')`
- failed (with `ignore_errors`): `results | selectattr('failed')`
- skipped: `results | selectattr('skipped', 'defined')`
- build a dict item→value: `results | items2dict(key_name='item', value_name='stdout')` (`items2dict` takes `key_name` and `value_name`)

## Iterating results in a follow-up task
```yaml
- ansible.builtin.command: "openssl x509 -enddate -noout -in {{ item }}"
  loop: "{{ cert_paths }}"
  register: certs
  changed_when: false

- name: Show expiry per cert
  ansible.builtin.debug:
    msg: "{{ item.item }} -> {{ item.stdout }}"
  loop: "{{ certs.results }}"
  loop_control:
    label: "{{ item.item }}"
```
`item.item` is the original loop item. When the original loop used `loop_var: cert`, the
original value is at `item.cert`; inside a task `ansible_loop_var` holds the name of the loop variable.

## Readable output
Each result line prints the whole item by default; for dicts that is noisy or leaks data:
```yaml
loop_control:
  label: "{{ item.name }}"
```
`label` only improves readability; it does not protect sensitive data. For secrets in items, set `no_log: true` on the task.

## Gotchas
- `results` exists only when the task looped; if the looping task may not have run, guard with `(health.results | default([]))`.
- With `until`, the registered result for each item includes `attempts`; `-vv` shows individual retries.
- Since 2.21 the implicit `_task` variable (`_task.result`, `_task.loop_result`) gives access to loop results without registering a variable.

## Verify
- [ ] `debug: msg="{{ health.results | map(attribute='item') | list }}"` matches the loop input.

## Checked
Date: 2026-10-24. Documentation: Ansible playbook guide, Loops (playbooks_loops.rst, shared_snippets/with2loop.txt), devel; lookup plugin sources; filters page.
Confirmed:
- results list structure; changed/failed true if any iteration did, skipped only if all did; item, ansible_loop_var, label and no_log note; until adds attempts.
- items2dict key_name and value_name; the _task variable since 2.21.
- Removed the unverified skipped-result shape and include-register claims.

Method: documentation only; no commands were run.
