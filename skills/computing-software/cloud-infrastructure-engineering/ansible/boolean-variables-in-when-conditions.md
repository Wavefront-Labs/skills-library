---
id: computing-software.cloud-infrastructure-engineering.ansible.boolean-variables-in-when-conditions
name: boolean-variables-in-when-conditions
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, conditionals, when-bool, bool-filter, when]
level: intro
status: docs-checked
description: "Evaluate boolean variables in when safely: string vs real booleans from extra vars, surveys and INI inventory, the bool filter, and core 2.19 conditional strictness."
sources: ["https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_conditionals.html#conditionals-based-on-variables", "https://docs.ansible.com/ansible/latest/collections/ansible/builtin/bool_filter.html", "https://docs.ansible.com/ansible/latest/porting_guides/porting_guide_core_2.19.html", "https://docs.ansible.com/ansible/latest/reference_appendices/config.html", "https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_variables.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Booleans in when

```yaml
- name: Enable TLS
  ansible.builtin.include_tasks: tls.yml
  when: enable_tls | bool
```

## Why | bool
Conditionals require boolean input, so apply `| bool` to non-boolean variables, such as strings
like `'yes'`, `'on'`, `'1'` or `'true'`. Values often arrive as strings:
- `-e enable_tls=false` uses `key=value` syntax, and values passed that way are interpreted as
  strings. Use JSON to keep types: `-e '{"enable_tls": false}'`.
- Other string sources include INI inventory group vars.

The `bool` filter accepts true values (`True`, `'yes'`, `'on'`, `'1'`, `'true'`, `1`) and false values
(`False`, `'no'`, `'off'`, `'0'`, `'false'`, `0`), compared case-insensitively. An invalid value gives a
deprecation warning. For more permissive checks use the `truthy` and `falsy` tests.

## Patterns
```yaml
when: not (skip_reboot | default(false) | bool)
when: (feature_x | default(false) | bool) and ansible_facts['os_family'] == 'RedHat'
```

## ansible-core 2.19 and later: boolean results required
Since 2.19 a conditional whose result is not a boolean is an error by default, for example
`Conditional result was 'localhost' of type 'str', which evaluates to True. Conditionals must have a boolean result.`
The setting `ALLOW_BROKEN_CONDITIONALS` (env `ANSIBLE_ALLOW_BROKEN_CONDITIONALS`, default false, added
in 2.19) temporarily reduces this to a warning; the config entry notes it is slated for deprecation
once it has no effect (2.23). Use explicit predicates (`| bool`, `| length > 0`, `is truthy`).

## Gotchas
- Check variables you are unsure about with `is defined` first; for optional flags chain `| default(false) | bool`.
- Compare booleans directly (`when: flag | bool`), not by string comparison with `"true"`.

## Verify
```bash
ansible-playbook p.yml -e enable_tls=false --check -v     # TLS tasks skipped
```

## Checked
Checked 2026-10-23 against ansible-documentation (playbooks_conditionals.rst, playbooks_variables.rst, 2.19
porting guide) and ansible-core devel `plugins/filter/bool.yml` and `config/base.yml`. Fixed: the 2.19
error is raised for non-boolean results generally, with the documented message text. Removed unconfirmed claims
about surveys and environment lookups, and the "arbitrary string returns false" behaviour (the filter now warns).
Method: documentation only; no commands were run.
