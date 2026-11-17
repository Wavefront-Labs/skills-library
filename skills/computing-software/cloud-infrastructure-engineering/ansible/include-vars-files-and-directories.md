---
id: computing-software.cloud-infrastructure-engineering.ansible.include-vars-files-and-directories
name: include-vars-files-and-directories
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, variables-precedence, include-vars, dir-include-vars, vars-files, os-specific-vars, first-found]
level: practitioner
status: docs-checked
description: "Load variables at runtime with include_vars from a file, a directory (depth, files_matching, ignore_files) or the first_found OS-specific file, and know its precedence."
sources: ["https://docs.ansible.com/ansible/latest/collections/ansible/builtin/include_vars_module.html", "https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_variables.html#understanding-variable-precedence", "https://docs.ansible.com/ansible/latest/collections/ansible/builtin/first_found_lookup.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# include_vars for files and directories

`include_vars` is a **task**: it loads variables at runtime, can be conditional and looped, and
its variables have high precedence (level 18 — above role vars, host facts, block/task vars, below
`set_fact`/registered vars and extra vars).

## Single file
```yaml
- name: Load release metadata
  ansible.builtin.include_vars:
    file: "release/{{ app_version }}.yml"
```
A relative `file` is looked up in the role's `vars/` subdirectory (inside a role) or relative to the playbook.

## OS-specific vars (the standard pattern)
```yaml
- name: Load OS-specific variables
  ansible.builtin.include_vars: "{{ lookup('ansible.builtin.first_found', params) }}"
  vars:
    params:
      files:
        - "{{ ansible_facts['distribution'] }}-{{ ansible_facts['distribution_major_version'] }}.yml"
        - "{{ ansible_facts['distribution'] }}.yml"
        - "{{ ansible_facts['os_family'] }}.yml"
        - default.yml
      paths: ["{{ role_path }}/vars"]
```

## Whole directory
```yaml
- ansible.builtin.include_vars:
    dir: vars/services
    extensions: [yml, yaml]
    files_matching: '^svc_.*'
    ignore_files: [README.yml]
    depth: 1               # default 0 = recurse through all subdirectories
    name: services         # load everything under one dict key instead of top level
```
Files in a directory are sorted alphabetically before loading, so later files override earlier top-level keys. `extensions` defaults to `json`, `yaml`, `yml`; `ignore_unknown_extensions: true` skips other files such as a README. With `name:`, the result is a single dict, which avoids polluting the namespace.

## Loading into a named dict from a file
```yaml
- ansible.builtin.include_vars:
    file: endpoints.yml
    name: endpoints        # access as endpoints.api_url
```

## vars_files vs include_vars
| | `vars_files` (play) | `include_vars` (task) |
|---|---|---|
| evaluated | at play start | when the task runs |
| conditional / loop | no | yes |
| facts available in path | no (before gathering) | yes |
| precedence | 14 | 18 |

## Gotchas
- Because precedence is high, `include_vars` overrides role defaults **and** inventory vars — teams get surprised when inventory overrides stop working. Use role `defaults/` for overridable values.
- Variables loaded this way are host-scoped and stay set for the rest of the run, not just the role (the docs list `include_vars` among host-scope variables).
- With the default global `hash_behaviour = replace`, a dict in a later file replaces the whole earlier dict. The task option `hash_behaviour: merge` merges instead, but it does not apply per file inside `dir`; loop over files if you need that.
- Variable files loaded by `include_vars` can be vault-encrypted (see the vault guide).

## Verify
- [ ] The task result (`-v`) returns `ansible_included_var_files`, listing the files actually loaded.

## Checked
Checked 2026-10-25 against ansible-core devel `modules/include_vars.py` documentation and the first_found lookup examples, and ansible-documentation devel (commit of 2026-10-21) playbook_guide/playbooks_variables.rst (precedence list and scopes) and vault_guide/vault_encrypting_content.rst. Confirmed: option names and defaults (`depth` 0, `extensions`, `ignore_unknown_extensions`, `hash_behaviour`), alphabetical loading, relative path lookup, precedence numbers 14 and 18 (counting the command-line values entry as 1), host scope, the `first_found` params pattern and `ansible_included_var_files`. Narrowed the hash_behaviour note to what the module documents.
Method: documentation only; no commands were run.
