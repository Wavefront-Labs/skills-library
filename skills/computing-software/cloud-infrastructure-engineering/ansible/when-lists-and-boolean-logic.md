---
id: computing-software.cloud-infrastructure-engineering.ansible.when-lists-and-boolean-logic
name: when-lists-and-boolean-logic
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, conditionals, when-list, and-or-conditions, bool-filter, conditional-bare-variables]
level: intro
status: docs-checked
description: "Combine conditions in when: list form as implicit AND, explicit and/or/not with parentheses, bool coercion of strings, version comparisons and in/not in membership."
sources: ["https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_conditionals.html", "https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_tests.html", "https://github.com/ansible/ansible-documentation", "https://github.com/ansible/ansible"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# when lists and boolean logic

`when` is a raw Jinja2 expression — no `{{ }}`.

## List form = AND
```yaml
when:
  - ansible_facts['os_family'] == 'RedHat'
  - ansible_facts['distribution_major_version'] | int >= 8
  - not skip_firewall | bool
```
All items must be true. Easiest to read and diff; one condition per line.

## OR and grouping
```yaml
when: >-
  (ansible_facts['distribution'] == 'CentOS' and ansible_facts['distribution_major_version'] == '7')
  or ansible_facts['distribution'] == 'Amazon'
```
Use `>-` folded block for long expressions. Parenthesise every mixed and/or so readers do not depend on operator precedence.

## Membership and comparisons
```yaml
when: inventory_hostname in groups['canary']
when: "'nginx' not in installed_packages"
when: ansible_facts['distribution'] in ['Ubuntu', 'Debian']
when: ansible_facts['kernel'] is version('5.14', '>=')    # version comparison test, not string comparison
when: app_port | int > 1024
```
Quote the whole value when it starts with a quote character (YAML rule).

## Booleans from strings
Variables from `-e key=value`, surveys, or INI inventory are strings. `"false"` is truthy.
```yaml
when: enable_tls | bool          # 'yes','on','1','true' → True; 'no','off','0','false' → False (case-insensitive)
when: not (enable_tls | bool)
```
ansible-core 2.19 requires conditionals to produce a real boolean: a non-boolean result such as a non-empty string is an error ("Conditionals must have a boolean result"), which the `ALLOW_BROKEN_CONDITIONALS` setting can temporarily reduce to a warning. Use an explicit predicate such as `| bool` (an invalid value gives a deprecation warning), `| length > 0`, or the `truthy` / `falsy` tests for more permissive conversion.

## Defined/empty checks
```yaml
when:
  - proxy is defined
  - proxy | length > 0
```
or `when: proxy | default('') | length > 0`.

## Gotchas
- `distribution_major_version` is a string fact: compare to `'8'` or cast `| int`.
- Variables given as strings (such as `"yes"`) need `| bool` to act as booleans in a conditional.
- List conditions are joined with AND only; for OR write one expression with `or`.
- Not every fact exists on every host (for example `lsb_major_release` needs `lsb_release` installed); `is defined` guards help.
- With a loop, `when` is evaluated separately for each item.

## Verify
- [ ] A `debug` task printing the expression with sample inputs gives a real boolean before you put it in `when`.

## Checked
Date: 2026-10-24. Documentation: Ansible playbook guide, Conditionals (playbooks_conditionals.rst), Tests, porting guide for ansible-core 2.19, ansible-core convert_bool.py and bool filter docs.
Confirmed:
- when is a raw Jinja2 expression; list form is AND; per-item evaluation in loops; bool filter accepted values; 2.19 requires boolean results (ALLOW_BROKEN_CONDITIONALS reduces the error to a warning).
- Removed the CONDITIONAL_BARE_VARS statement and the package_facts note.

Method: documentation only; no commands were run.
