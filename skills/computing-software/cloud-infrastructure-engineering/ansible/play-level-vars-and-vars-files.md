---
id: computing-software.cloud-infrastructure-engineering.ansible.play-level-vars-and-vars-files
name: play-level-vars-and-vars-files
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, playbook-syntax, play-vars-files, vars-files, vars-files-fallback, variables]
level: intro
status: docs-checked
description: "Define play-level vars and vars_files, load per-environment or per-OS files with fallback lists, and know their precedence against inventory and role vars."
sources: ["Using variables (https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_variables.html)", "Conditionals, variables and facts (vars_files fallback lists) (https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_conditionals.html)", "Playbook keywords (https://docs.ansible.com/ansible/latest/reference_appendices/playbooks_keywords.html)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Play-level vars and vars_files

```yaml
- name: Configure web tier
  hosts: web
  vars:
    http_port: 8080
    app_env: "{{ env | default('dev') }}"
  vars_files:
    - vars/common.yml
    - "vars/{{ app_env }}.yml"
    - [ "vars/{{ ansible_facts['os_family'] }}.yml", vars/os_default.yml ]   # first found wins
  tasks: [...]
```

## Rules
- A nested list is a fallback chain: Ansible loads the first file in the list that exists, and raises an error if none of them is found.
- Paths can be templated with facts: the conditionals guide gathers facts first, then interpolates `ansible_facts['os_family']` into the file name.
- `vars`, `vars_files` and `vars_prompt` entries have play scope.

## Precedence
play `vars` (12) < play `vars_prompt` (13) < play `vars_files` (14) < role vars (15) < block vars < task vars < include_vars < set_fact/registered < role params < include params < extra vars. Play vars beat **all inventory vars** (group_vars and host_vars), a frequent surprise when someone expects host_vars to override a play default. Use role defaults for overridable defaults instead.

## Gotchas
- Large `vars:` blocks in plays hide configuration; prefer group_vars for environment data and role defaults for tunables.

## Verify
```yaml
- ansible.builtin.debug: {var: http_port}
```

## Checked

Checked 2026-10-26 against ansible-documentation main (2026-10-21).
- Confirmed: the precedence order (play vars, then `vars_prompt`, then `vars_files`, then role vars, block vars, task vars, `include_vars`, registered vars and `set_fact`, role params, include params, extra vars), with all inventory, `group_vars`, `host_vars` and host facts below play vars; the `vars_files` fallback-list behaviour including the error when no file matches; play scope of `vars`, `vars_files` and `vars_prompt`.
- Removed as unconfirmed: the claim that `vars_files` paths are relative to the playbook directory, the missing-plain-file error, and the vault remark.

Method: documentation only; no commands were run.
