---
id: computing-software.cloud-infrastructure-engineering.ansible.variable-names-and-nested-data-access
name: variable-names-and-nested-data-access
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, variables-precedence, variable-naming, valid-variable-names, bracket-notation, nested-variables, reserved-names]
level: intro
status: docs-checked
description: "Pick valid Ansible variable names that avoid reserved and magic names, and read nested dicts and lists with dot vs bracket notation, including dynamic keys."
sources: ["https://github.com/ansible/ansible-documentation/blob/devel/docs/docsite/rst/playbook_guide/playbooks_variables.rst", "https://github.com/ansible/ansible-documentation/blob/devel/docs/docsite/rst/reference_appendices/special_variables.rst", "https://github.com/ansible/ansible-documentation/blob/devel/docs/docsite/rst/playbook_guide/playbooks_filters.rst", "https://github.com/ansible/ansible-documentation/blob/devel/docs/docsite/rst/porting_guides/porting_guide_core_2.20.rst", "https://github.com/ansible/ansible-lint/blob/main/docs/rules/var-naming.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Variable names and nested data access

## Valid names
- Letters, digits and underscores only; must not start with a digit. `foo_port`, `foo5` and `_foo` are valid; `foo-port`, `foo.port`, `foo port`, `5foo` and `*foo` are not.
- Must not be a Python keyword (`async`, `lambda`, ...) or a playbook keyword (`environment`, ...).
- A leading underscore has no special meaning in Ansible: do not rely on it for privacy or security.
- Do not use names Ansible defines internally (the magic variables on the Special variables page, such as `hostvars`, `groups`, `group_names`, `inventory_hostname`, `role_name`), and avoid names that overwrite Jinja2 globals such as `lookup`, `query`, `q`, `now` and `undef`.
- Prefix role variables with the role name (`nginx_worker_processes`); ansible-lint's `var-naming[no-role-prefix]` reports names inside roles that lack the `role_name_` prefix.

ansible-lint's `var-naming` rule has sub-checks including `var-naming[pattern]`, `var-naming[no-keyword]`, `var-naming[no-reserved]`, `var-naming[no-role-prefix]` and `var-naming[read-only]`.

## Dot vs bracket notation
```yaml
app:
  db:
    host: db1
    port: 5432
  items: [a, b]
```
| Expression | Notes |
|---|---|
| `app.db.host` | readable |
| `app['db']['host']` | always works |
| `app['items']` | **must** use brackets: `app.items` is the dict method `.items()` |
| `ansible_facts['eth0']['ipv4']['address']` | |
| `hostvars[groups['db'][0]]['ansible_host']` | |

The documentation: "Bracket notation always works. Dot notation can cause problems because some keys collide with attributes and methods of python dictionaries." Use brackets for keys that start and end with two underscores or match a known public attribute; its list includes `items`, `keys`, `values`, `update`, `copy`, `get`, `pop`, `index`, `count`, `split`, `format`, `join`, `replace` and many more. Also use brackets when the key contains a dash or dot, or comes from a variable:
```yaml
nic: eth1
ip: "{{ ansible_facts[nic]['ipv4']['address'] }}"
port: "{{ services[svc_name].port | default(80) }}"
```

## Safe deep access
```yaml
"{{ app.db.port | default(5432) }}"                       # works even if app or app.db is missing
"{{ (app.db | default({})).port | default(5432) }}"       # explicit form, clearer to reviewers
```
Since ansible-core 2.8, reading an attribute of an undefined value returns another undefined value, so a `default` at the end of `a.b.c` covers a missing link anywhere in the chain. `community.general.json_query('db.port')` is the JMESPath alternative (needs `jmespath` on the control node).

## Gotchas
- A group name with a dash is accepted but triggers an invalid-group-name warning by default; in an expression `groups.my-group` is parsed as subtraction, so use `groups['my-group']` and prefer underscores.
- Facts are available both as `ansible_facts['...']` (without the `ansible_` prefix) and, while `inject_facts_as_vars` is true (the default), as top-level `ansible_*` variables. That default is deprecated and switches to false in ansible-core 2.24, so use `ansible_facts[...]`.

## Verify
- [ ] `ansible-lint` has no `var-naming` findings.
- [ ] `debug: var=app['items']` prints the list, not a method object.

## Checked
Date 2026-10-24. Release: ansible-core 2.21.5 (source at tag v2.21.5) and the ansible-documentation main branch. Confirmed on the Using variables page (valid names, underscore note, dot-notation collision list, Jinja global names), the Special variables page, the Using filters page (chained undefined since 2.8), the 2.20 porting guide (`INJECT_FACTS_AS_VARS` deprecation, default switch in 2.24) and `config/base.yml`; ansible-lint's `var-naming` rule page for the sub-check names; `TRANSFORM_INVALID_GROUP_CHARS`. Removed the integer-key remark and the `item` and `play_hosts` name advice.
Method: documentation only; no commands were run.
