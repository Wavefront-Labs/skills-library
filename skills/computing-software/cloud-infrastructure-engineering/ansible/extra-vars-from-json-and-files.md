---
id: computing-software.cloud-infrastructure-engineering.ansible.extra-vars-from-json-and-files
name: extra-vars-from-json-and-files
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, variables-precedence, extra-vars, extra-vars-file, at-file, json-extra-vars]
level: practitioner
status: docs-checked
description: "Pass extra vars as key=value, inline JSON or @file (YAML/JSON, vaulted), know the typing differences, and use them safely as the highest-precedence override."
sources: ["Ansible variables guide, defining variables at runtime (https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_variables.html#defining-variables-at-runtime)", "Ansible variables guide, variable precedence (https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_variables.html#understanding-variable-precedence)", "Ansible filters guide, managing data types (https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_filters.html#managing-data-types)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Extra vars from JSON and @file

Extra vars (`-e`/`--extra-vars`) rank last in the precedence list and always win; nothing in a play overrides them, not even `set_fact`. Treat them as operator inputs, not configuration.

## Three forms
Pass the variables as a single quoted string in one of these formats:
```bash
# key=value: every value is interpreted as a STRING
ansible-playbook release.yml --extra-vars "version=1.23.45 other_variable=foo"
# JSON string: real types
ansible-playbook arcade.yml --extra-vars '{"pacman":"mrs","ghosts":["inky","pinky","clyde","sue"]}'
# JSON or YAML file: prepend the file name with @
ansible-playbook release.yml --extra-vars "@some_file.json"
ansible-playbook release.yml --extra-vars "@some_file.yaml"
```
When passing JSON on the command line, escape quotes and special characters for both JSON and your shell. If you have many special characters, use a file instead.

## The type trap
`key=value` values are strings. Use the JSON or file form for booleans, integers, floats and lists, or coerce in the play with `| bool`, `| int`.

## Typical uses
- Release parameters from CI.
- Target selection: `hosts: "{{ target }}"` with `-e target=web_canary`.
- A per-run change record kept in version control and passed as `-e @file`.

## Security
- Values on the command line can appear in process listings, shell history and CI logs; do not pass secrets that way.

## Gotchas
- Because they win over everything, `-e` silently disables role logic that sets the same variable with `set_fact`. Name operator inputs distinctly (`input_version`) and map them.

## Verify
- [ ] `ansible localhost -e @f.yml -m debug -a 'msg={{ replicas | type_debug }}'` shows `int`, not `str`, for a number written in the file.

## Checked
Checked 2026-10-23 against the Ansible documentation source on GitHub (playbooks_variables.rst and playbooks_filters.rst; latest ansible-core release v2.21.5): the three formats, string typing of `key=value`, the `@` file prefix for JSON and YAML, quoting and escaping advice, extra vars winning over everything, and the `type_debug` filter. Removed the unconfirmed claims that repeated `-e` options are applied left to right, that `@file` paths are relative to the current directory, that vaulted extra-vars files are supported, that string `false` is truthy in `when`, and the controller (AWX) and `hostvars`/`delegate_to` remarks.
Method: documentation only; no commands were run.
