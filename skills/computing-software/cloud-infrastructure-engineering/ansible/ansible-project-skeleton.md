---
id: computing-software.cloud-infrastructure-engineering.ansible.ansible-project-skeleton
name: ansible-project-skeleton
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, playbook-syntax, ansible-project-skeleton, project-layout, requirements-yml]
level: practitioner
status: docs-checked
description: "Lay out an Ansible project repository: inventories per environment, group_vars, site.yml with import_playbook, roles, roles_path in ansible.cfg, and requirements files."
sources: ["https://docs.ansible.com/ansible/latest/tips_tricks/sample_setup.html", "https://docs.ansible.com/ansible/latest/tips_tricks/ansible_tips_tricks.html", "https://docs.ansible.com/automation-controller/latest/html/userguide/projects.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Ansible project skeleton

The documented sample layout puts inventories (`production`, `staging`), `group_vars/`, `host_vars/`, `site.yml`, tier playbooks and `roles/` at the top level. This skill's extended layout (items marked * are project conventions, not from the docs):

```
infra-ansible/
  ansible.cfg
  ansible-navigator.yml *          # EE image, mode, artifact settings
  .ansible-lint *
  requirements.yml *               # roles + collections, pinned
  inventories/
    prod/
      hosts.yml
      group_vars/
      host_vars/
    staging/...
  playbooks/
    site.yml                       # import_playbook of the tier playbooks
    webservers.yml
    dbservers.yml
  roles/
    common/
      tasks/main.yml  handlers/main.yml  templates/  files/
      vars/main.yml  defaults/main.yml  meta/main.yml
  library/                         # optional custom modules, auto-added to module path
```

## Why this shape (per the Ansible docs)
- One inventory per environment; for larger setups or very different variables, a directory per environment each holding its own `hosts` file plus `group_vars/` and `host_vars/` (fully separate variables, more files to maintain).
- `group_vars/all` holds values true everywhere; `group_vars/<group>.yml` per group; `host_vars/<host>.yml` per machine.
- `site.yml` is the entry point and uses `import_playbook` to include tier playbooks; run one tier alone or narrow with `--limit`.
- Each role is a directory with `tasks`, `handlers`, `templates`, `files`, `vars` (higher precedence), `defaults` (lowest precedence), `meta`; Ansible loads `main.yml` in each. Handlers run at end of each play and only when a notifying task changed.
- If playbooks move into a `playbooks/` subdirectory, set `roles_path` in `ansible.cfg` to the roles directory; otherwise Ansible looks for `roles/` next to the playbooks.
- Keep playbooks, roles, inventory and variables in git; use FQCNs, name plays/tasks, set `state` explicitly; test in staging first and use `--syntax-check`; use `serial` for batches; use Execution Environments for consistent runs.
- Prefer magic variables such as `playbook_dir` over paths tied to `ansible.cfg`.
- Vault tip from the docs: keep variable names visible by putting values in an encrypted file with `vault_` prefixed names, referenced from a plain vars file.

## Scaffolding
```bash
ansible-galaxy role init roles/nginx
```

## Gotchas
- Defaulting `inventory` in `ansible.cfg` to staging is a project convention* that stops a bare `ansible-playbook` hitting prod.
- Collections: the sample-setup page gives no collection layout (only a link to the index). A `requirements.yml` for collections and roles, and whether automation controller reads `collections/requirements.yml` and `roles/requirements.yml` on project sync, were not verified (the controller docs URL now redirects to a legacy site that returned 404).
- Keep group_vars in one place (beside the inventory) to avoid two variable sources.

## Verify
- [ ] Fresh clone + `ansible-galaxy install -r requirements.yml` + `ansible-playbook playbooks/site.yml --syntax-check` passes.

## Checked
Method: 2026-11-08 docs-only read of the Ansible sample setup and tips-and-tricks pages; layout, inventory, role, import_playbook and roles_path claims confirmed. The automation controller projects page could not be read (301 to a legacy site, then 404), so the controller requirements.yml claims were removed or hedged. Collection scaffolding command and .gitignore advice removed as unsourced.
