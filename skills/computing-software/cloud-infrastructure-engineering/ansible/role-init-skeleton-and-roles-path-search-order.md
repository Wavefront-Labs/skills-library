---
id: computing-software.cloud-infrastructure-engineering.ansible.role-init-skeleton-and-roles-path-search-order
name: role-init-skeleton-and-roles-path-search-order
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, roles, role-init, role-skeleton, roles-path, role-search-order, ansible-galaxy]
level: intro
status: docs-checked
description: "Scaffold roles with ansible-galaxy role init (including custom skeletons), and control where Ansible finds roles via roles_path, playbook-relative roles/ and collections."
sources: ["Creating roles with ansible-galaxy (https://docs.ansible.com/ansible/latest/galaxy/dev_guide.html)", "Roles, storing and finding roles (https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_reuse_roles.html)", "ansible-galaxy CLI source (https://github.com/ansible/ansible/blob/devel/lib/ansible/cli/galaxy.py)", "Default role skeleton in ansible-core (https://github.com/ansible/ansible/tree/devel/lib/ansible/galaxy/data/default/role)", "Configuration settings, DEFAULT_ROLES_PATH (https://github.com/ansible/ansible/blob/devel/lib/ansible/config/base.yml)", "ansible-lint rule role-name (https://github.com/ansible/ansible-lint/blob/main/src/ansiblelint/rules/role_name.md)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# role init, skeletons and roles_path

## Scaffolding
```bash
ansible-galaxy role init --init-path roles nginx
```
creates `roles/nginx/{defaults,files,handlers,meta,tasks,templates,tests,vars}/` plus `README.md`, with `main.yml` files in `defaults`, `handlers`, `meta`, `tasks` and `vars` and `tests/inventory` plus `tests/test.yml` (delete what you don't use; empty directories are noise). `--force` replaces an existing directory of the same name; `--type container` creates the Container Enabled variant.

## Custom skeleton
Make every new role start with your standards (argument_specs, molecule scenario, README template):
```bash
ansible-galaxy role init --role-skeleton ./skeletons/role --init-path roles nginx
```
```ini
[galaxy]
role_skeleton = ./skeletons/role
role_skeleton_ignore = ^.git$, ^.*/.git_keep$
```
When a skeleton is used, `init` copies all its files and directories to the new role, renders any `.j2` file found outside a `templates` folder (the only useful variable is `role_name`), and does not copy the `.git` folder or `.git_keep` files. `role_skeleton_ignore` is a list of regular expressions matched against directory names and relative file paths.

## Where roles are found (search order)
For `roles: [nginx]` / `include_role: name=nginx`:
1. Collections, if you use them.
2. A `roles/` directory relative to the playbook file.
3. The configured `roles_path` (`ANSIBLE_ROLES_PATH`, `[defaults] roles_path`).
   Default: `~/.ansible/roles:/usr/share/ansible/roles:/etc/ansible/roles`.
4. The directory where the playbook file is located.
A role can also be called with a fully qualified path: `- role: '/path/to/my/roles/common'`.

```ini
[defaults]
roles_path = ./roles:./vendor/roles
```
Install Galaxy roles into the vendor path: `ansible-galaxy role install -r requirements.yml -p vendor/roles`.

## Gotchas
- Two roles with the same name in different paths: the search order above decides which is used. Use FQCN roles from collections or unique names.
- `roles/` is searched relative to the playbook file, so a playbook in a `playbooks/` subdirectory does not see a `roles/` directory at the repository root unless `roles_path` includes it. `roles_path` is declared with `expand_relative_paths`; verify the effective value with `ansible-config dump` and a test run from the directory CI uses.
- ansible-lint's `role-name` rule requires role names to start with a letter and contain only lowercase letters, digits and underscores.

## Verify
- [ ] `ansible-config dump | grep ROLES_PATH` shows the intended order.
- [ ] `ansible-playbook site.yml --list-tasks` resolves every role (no "role not found").

## Checked

Checked 2026-10-26 against ansible-documentation main (2026-10-21) and ansible-core 2.21.5 sources.
- Confirmed: `ansible-galaxy role init` options `--init-path`, `--role-skeleton`, `--force`, `--type container`; the generated tree (the default skeleton in core contains README.md, defaults, files, handlers, meta, tasks, templates, tests, vars and no `.travis.yml`); skeleton rules for `.j2` files and `.git`/`.git_keep`; `[galaxy] role_skeleton` and `role_skeleton_ignore`; the four-step role search order and the default `roles_path`; the ansible-lint `role-name` rule.
- Fixed: the `.travis.yml` file is not part of the current default skeleton.
- Removed as unconfirmed: the collection-root `role init` instruction, the claim about dashed role names, and the silent first-found remark.

Method: documentation only; no commands were run.
