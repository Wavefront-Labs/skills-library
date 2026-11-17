---
id: computing-software.cloud-infrastructure-engineering.ansible.roles-and-playbooks-inside-collections
name: roles-and-playbooks-inside-collections
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, collection-roles, collection-playbooks, collection-development, fqcn]
level: practitioner
status: docs-checked
description: "Ship roles and playbooks in a collection, call them by FQCN (acme.platform.nginx, ansible-playbook acme.platform.site), and handle role naming and plugin lookup rules."
sources: ["Collection structure, roles and playbooks directories (https://docs.ansible.com/ansible/latest/dev_guide/developing_collections_structure.html)", "Using collections in playbooks (https://docs.ansible.com/ansible/latest/collections_guide/collections_using_playbooks.html)", "ansible-lint role-name rule (https://github.com/ansible/ansible-lint/blob/main/src/ansiblelint/rules/role_name.md)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Roles and playbooks inside collections

```
acme/platform/
  galaxy.yml
  roles/
    nginx/                 # role names: lowercase alphanumeric and underscore, starting with a letter
      tasks/main.yml
      meta/argument_specs.yml
  playbooks/
    site.yml
    patch.yml
    files/ templates/      # resources for playbooks
  plugins/modules/
```

## Calling collection roles
```yaml
- hosts: web
  roles:
    - acme.platform.nginx
  tasks:
    - ansible.builtin.include_role:
        name: acme.platform.nginx
        tasks_from: upgrade
```
Inside the collection's own roles, refer to sibling content by FQCN too (`acme.platform.my_module`), or set `collections: [acme.platform]` in the role's `meta/main.yml`.

## Running collection playbooks
```bash
ansible-playbook acme.platform.site -i inventory
ansible-playbook acme.platform.patch -e target=web
```
(ansible-core 2.11+; the FQCN, with or without extension, also works with `import_playbook` and keeps the playbook in collection context). Hosts in collection playbooks should be a variable such as `hosts: '{{ target | default("all") }}'` so users do not run them against their whole inventory, and playbooks must live in the `playbooks/` directory (no `roles/` subdirectory there).

## Differences from standalone roles
- Role names are limited to lowercase alphanumeric characters plus `_` and must start with a letter; the directory name is the role name, and Galaxy collection import fails otherwise.
- Roles in a collection cannot contain plugins; plugins live in the collection's `plugins` tree and are accessible to all roles in the collection.
- For roles imported from GitHub `role_name` in metadata overrides the name; for collections it is ignored.
- Declare collection dependencies in `galaxy.yml`.
- Use FQCNs for modules and plugins in role tasks, or set `collections:` in the role's `meta/main.yml`; roles do not inherit the `collections` keyword from the calling playbook.

## Versioning
Roles are versioned with the collection version; consumers pin `acme.platform:>=2.1,<3`.

## Verify
```bash
ansible-doc -t role -l                      # roles with argument specs, with their short descriptions
ansible-playbook acme.platform.site --syntax-check
```

## Checked

Checked 2026-10-26 against the Ansible collection structure documentation (roles and playbooks directories), the collections-in-playbooks guide and the ansible-lint `role-name` rule. Confirmed: role name rules, no plugins inside collection roles, `role_name` ignored for collections, FQCN playbooks from ansible-core 2.11, playbook `hosts` variable guidance, `collections:` in role `meta/main.yml` and non-inheritance from the playbook, `ansible-doc -t role -l`. Removed unconfirmed AAP, dependency, `meta/requirements.yml` and FQCN parsing claims.

Method: documentation only; no commands were run.
