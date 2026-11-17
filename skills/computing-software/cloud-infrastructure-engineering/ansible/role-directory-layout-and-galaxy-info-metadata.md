---
id: computing-software.cloud-infrastructure-engineering.ansible.role-directory-layout-and-galaxy-info-metadata
name: role-directory-layout-and-galaxy-info-metadata
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, roles, role-directories, galaxy-info, role-structure, meta-main]
level: intro
status: docs-checked
description: "Know what each role directory does (tasks, handlers, defaults, vars, files, templates, library, module_utils, meta) and fill galaxy_info platforms and min_ansible_version."
sources: ["Roles (https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_reuse_roles.html)", "Galaxy user guide (https://docs.ansible.com/ansible/latest/galaxy/user_guide.html)", "Galaxy developer guide (https://docs.ansible.com/ansible/latest/galaxy/dev_guide.html)", "ansible-lint schema rule (https://github.com/ansible/ansible-lint/blob/main/src/ansiblelint/rules/schema.md)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Role directory layout and galaxy_info

```
roles/nginx/
  tasks/main.yml          # entry point; other files via include_tasks/tasks_from
  handlers/main.yml       # handlers, visible to the whole play
  defaults/main.yml       # lowest-precedence, user-overridable values
  vars/main.yml           # high-precedence internal values (OS maps)
  files/                  # static files for copy/script (src: relative here)
  templates/              # .j2 files for template (src: relative here)
  meta/main.yml           # galaxy_info, dependencies, allow_duplicates
  meta/argument_specs.yml # input validation per entry point
  library/                # role-local modules (usable in the role and in roles called after it)
  filter_plugins/ ...     # role-local plugins, same idea (standalone roles only)
  tests/                  # legacy inventory + test.yml (Molecule replaces this)
  molecule/               # scenarios
  README.md
```
Every directory is optional (a role needs at least one of the standard directories); `main.yml` (or `main.yaml`, `main`) is loaded automatically where it exists. `defaults` and `vars` may include nested directories, whose files are read in alphabetical order. Roles in collections cannot embed plugins; they use the collection's `plugins` tree.

## Search order for files and templates
Copy, script, template and include tasks inside a role can reference files in `roles/x/{files,templates,tasks}/` (the directory depends on the task) without relative or absolute paths. Use plain names.

## meta/main.yml galaxy_info
```yaml
galaxy_info:
  role_name: nginx
  namespace: acme
  author: Platform Team
  description: Install and configure NGINX
  license: Apache-2.0
  min_ansible_version: "2.15"
  platforms:
    - name: EL
      versions: ["8", "9"]
    - name: Ubuntu
      versions: [jammy, noble]
  galaxy_tags: [web, nginx]
dependencies: []
```
- `meta/main.yml` is required for uploading a standalone role to Galaxy but not for local use; `ansible-galaxy role info` shows fields such as `namespace`, `license` and `min_ansible_version` that Galaxy stored. For roles imported from GitHub, `role_name` overrides the role name Galaxy uses (it is ignored for roles inside collections).
- ansible-lint's `schema[meta]` validates role `meta/main.yml`.

## Verify
```bash
ansible-lint roles/nginx
```

## Checked

Checked 2026-10-26 against the Ansible documentation (roles, Galaxy user and developer guides, collection structure) and the ansible-lint `schema` rule page. Confirmed: standard role directories and `main.yml` loading, nested `defaults` and `vars` directories, `library/` and `filter_plugins` embedding for standalone roles, file lookup without relative paths, `meta/main.yml` use for Galaxy, `role_name` behaviour, `schema[meta]`. Removed unconfirmed 2.11 gate for nested directories, `module_utils` directory, the lookup order and the platform name list claims.

Method: documentation only; no commands were run.
