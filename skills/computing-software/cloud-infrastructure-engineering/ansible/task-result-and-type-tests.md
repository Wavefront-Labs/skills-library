---
id: computing-software.cloud-infrastructure-engineering.ansible.task-result-and-type-tests
name: task-result-and-type-tests
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, tests, task-result-tests, type-tests, jinja-tests]
level: practitioner
status: docs-checked
description: "Test registered results with succeeded, failed, changed, skipped and finished, and check value types with string, number, mapping, sequence, iterable and boolean tests."
sources: ["https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_tests.html", "https://jinja.palletsprojects.com/en/stable/templates/", "https://github.com/ansible/ansible-documentation", "https://github.com/ansible/ansible"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Task result and type tests

## Result tests
```yaml
- ansible.builtin.command: /opt/app/bin/health
  register: health
  ignore_errors: true
  changed_when: false

- ansible.builtin.debug: {msg: "healthy"}
  when: health is succeeded           # alias: is success
- ansible.builtin.include_tasks: recover.yml
  when: health is failed
- ansible.builtin.debug: {msg: "was skipped"}
  when: health is skipped
- ansible.builtin.debug: {msg: "changed"}
  when: health is changed
```
- The documented result tests are `failed`, `changed`, `succeeded` (alias `success`) and `skipped`; the core test plugin also provides `reachable`, `unreachable`, `started`, `finished` and `timedout`.
- Aliases in the plugin: `failure`, `successful`, `change`, `skip`.
- Prefer these tests to reading raw fields such as `result.failed`.

## Type tests
```yaml
- ansible.builtin.assert:
    that:
      - app_ports is sequence and app_ports is not string
      - app_config is mapping
      - replicas is number
      - enable_tls is boolean
      - admin_email is string
    fail_msg: "Invalid variable types supplied"
```
| Test | True for |
|---|---|
| `string` | str |
| `number` / `integer` / `float` | numeric types |
| `boolean` | true/false (not "true") |
| `mapping` | dict |
| `sequence` | list, dict and string |
| `iterable` | list, dict, string, generator |
| `none` | None |
| `callable` | functions |

A string is classed as `iterable` and `sequence` but not `mapping`; a dict is `iterable`, `sequence` and `mapping` but not `string`; a list is `iterable` and `sequence` but not `string` or `mapping`; a numeric string such as `"1"` is a `string`, not a `number`.

Because strings are sequences and iterables, always pair with `is not string` when you mean a list.

## Use in role entry points
Type tests in `assert` at the start of a role (or `meta/argument_specs.yml`, whose validation task is tagged `always`) catch caller mistakes like passing `"8080,8443"` instead of a list. Use type tests rather than comparing `type_debug` output with a type name.

## Verify
- [ ] Assert fails with a clear message when given a string instead of a list.

## Checked
Date: 2026-10-24. Documentation: Ansible playbook guide, Tests (playbooks_tests.rst), ansible-core plugins/test/core.py, Jinja tests.py (3.x).
Confirmed:
- Result tests failed, changed, succeeded/success, skipped; plugin also provides reachable, unreachable, started, finished, timedout and aliases.
- Type tests string, number, integer, float, boolean, mapping, sequence, iterable, none, callable exist in Jinja; strings are iterable and sequence, not mapping; a numeric string is not a number.
- Removed the claim that result.failed is missing on skipped results.

Method: documentation only; no commands were run.
