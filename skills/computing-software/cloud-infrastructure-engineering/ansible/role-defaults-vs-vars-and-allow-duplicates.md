---
id: computing-software.cloud-infrastructure-engineering.ansible.role-defaults-vs-vars-and-allow-duplicates
name: role-defaults-vs-vars-and-allow-duplicates
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, roles, role-defaults, role-vars, allow-duplicates, role-deduplication, role-params]
level: practitioner
status: docs-checked
description: "Put role variables in defaults/ (overridable) or vars/ (internal constants), pass role params, and control whether a role listed twice runs twice with allow_duplicates."
sources: ["https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_reuse_roles.html", "https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_variables.html#understanding-variable-precedence", "https://docs.ansible.com/ansible/latest/collections/ansible/builtin/include_role_module.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Role defaults vs vars, and allow_duplicates

## defaults/ vs vars/
| | `defaults/main.yml` | `vars/main.yml` |
|---|---|---|
| Precedence | **lowest of all** (level 2) | high (15): beats inventory, group_vars, host_vars, play vars |
| Purpose | the role's public interface: anything a user may override | internal constants, OS-specific mappings |
| Override from inventory | yes | **no** — only extra vars, set_fact, include_vars, role params, block/task vars win |

```yaml
# roles/nginx/defaults/main.yml   - users override these in group_vars
nginx_worker_processes: auto
nginx_listen_port: 80
nginx_sites: []

# roles/nginx/vars/RedHat.yml     - loaded by include_vars per OS, not for users
nginx_package: nginx
nginx_conf_dir: /etc/nginx
nginx_user: nginx
```
Classic bug: putting `nginx_listen_port` in `vars/` — then `group_vars/web.yml: nginx_listen_port: 8080`
is silently ignored. Rule: if a user might ever want to change it, it goes in defaults.

## Role params
```yaml
roles:
  - role: nginx
    vars: {nginx_listen_port: 8080}     # vars keyword on the roles entry
  - {role: nginx, nginx_listen_port: 8081}   # role param (a key on the entry that is not a keyword)
```
In the precedence list, "Role (and include_role) params" are entry 20 of 22 (counting command-line values as 1), above registered vars and `set_fact` and below only include params and extra vars, so they beat inventory. `vars:` on a `roles:` entry is not the same thing as a role parameter, and since ansible-core 2.15 such `vars:` no longer leak into the play's variable scope (older releases added them to the play variables, controlled by `private_role_vars`).

## Running a role twice: deduplication
Ansible runs a role only **once per play** if it is listed multiple times unless the parameters defined on the role differ. Providing different `vars:` values is not the same as passing different role parameters, and only the `roles:` keyword accepts role parameters (`import_role` and `include_role` do not):
```yaml
roles:
  - {role: app_instance, instance: a}
  - {role: app_instance, instance: b}     # runs again: different parameters
```
Force repeated runs even with identical params in `roles/app_instance/meta/main.yml`:
```yaml
allow_duplicates: true
```
Dependencies: a role required by two other roles runs once (good for `common`) unless different parameters, tags or a different `when` are given on each definition, or the role sets `allow_duplicates: true`. De-duplication happens before variable evaluation, so lazily evaluated values can make two invocations look identical. `include_role` is dynamic: its `allow_duplicates` option defaults to true.

## Gotchas
- Dedup compares role parameters (and tags and `when` for dependencies), not `vars:`; it does not consult the invocation signature of parent roles.
- Variables from `vars/` and `defaults/` are imported into play scope unless disabled with `public` on `import_role`/`include_role` (or `private_role_vars`); tasks in a role see their own role's defaults, while tasks outside a role see the last role's defaults. Prefix variable names with the role name.
- Argument specs (`meta/argument_specs.yml`) document defaults and validate parameters; keep them in sync with `defaults/`.

## Verify
- [ ] Override a default from group_vars and confirm with `debug`; the same for a vars/ value shows the override does not apply (by design).
- [ ] `--list-tasks` shows the role once or twice as intended (roles from `roles:` and `import_role` are listed; `include_role` contents are not).

## Checked
Checked 2026-10-25 against ansible-documentation devel (commit of 2026-10-21) playbook_guide/playbooks_reuse_roles.rst (defaults and vars, run-a-role-twice, dependency de-duplication, `vars:` scoping note), playbook_guide/playbooks_variables.rst (precedence list) and playbooks_reuse.rst (include versus import), plus ansible-core `include_role` documentation (`allow_duplicates` default). Confirmed: precedence positions (defaults 2, role vars 15, role params 20), what overrides role `vars/`, the de-duplication rules and their exceptions, `allow_duplicates`, and variable scope notes. Corrected the claim that different `vars:` make a role run again (only different role parameters, tags or `when` do).
Method: documentation only; no commands were run.
