---
id: computing-software.cloud-infrastructure-engineering.ansible.tag-inheritance-roles-plays-imports-includes
name: tag-inheritance-roles-plays-imports-includes
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, tags, tag-inheritance, tagged-includes, role-tags, play-tags, apply-keyword]
level: practitioner
status: docs-checked
description: "Predict which tasks a tag selects: inheritance from plays, roles, blocks and import_* versus include_*, and pushing tags into included tasks with apply."
sources: ["https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_tags.html", "https://github.com/ansible/ansible-documentation", "https://github.com/ansible/ansible"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tag inheritance: plays, roles, imports and includes

## Static things pass tags down
Tags on a **play**, **block**, `roles:` entry or static import (`import_role`, `import_tasks`)
are added to every task inside.
```yaml
- hosts: web
  tags: [web]                # every task in the play, incl. gathering facts → 'web'
  roles:
    - role: nginx
      tags: [nginx]          # every nginx task gets 'nginx' and 'web'
  tasks:
    - ansible.builtin.import_tasks: deploy.yml
      tags: [deploy]         # each task in deploy.yml gets 'deploy'
```
`ansible-playbook site.yml --tags nginx` runs the nginx role tasks only (plus `always`).

## Dynamic includes do not
Tags on `include_tasks` / `include_role` apply to the **include statement only**:
```yaml
- ansible.builtin.include_tasks: deploy.yml
  tags: [deploy]
```
`--tags deploy` runs the include, but the tasks inside run only if they are themselves tagged
`deploy` (or `always`). Fix with `apply`:
```yaml
- ansible.builtin.include_tasks:
    file: deploy.yml
    apply:
      tags: [deploy]
  tags: [deploy]             # both needed: one selects the include, apply tags the inner tasks
```
Same for roles:
```yaml
- ansible.builtin.include_role:
    name: nginx
    apply: {tags: [nginx]}
  tags: [nginx]
```
Alternative: wrap the include in a block that carries the tag:
```yaml
- block:
    - ansible.builtin.include_tasks: deploy.yml
  tags: [deploy]
```

## Role tags
- On `roles:` entries and `import_role`: inherited (as above).
- Tags written on tasks inside the role add to inherited ones.
- Role dependencies (`meta/main.yml`) inherit the tags of the depending role.

## Gotchas
- A play-level tag also lands on the implicit tasks of the play (such as fact gathering), including those added via roles.
- Fact gathering is tagged `always` but can still be skipped: if you tag the play and then skip that tag with `--skip-tags`, or run `--tags` without it, gathering is skipped too.
- `--list-tags` and `--list-tasks` cannot show tags or tasks inside dynamically included files or roles; test includes with a real `--check` run.

## Verify
- [ ] `ansible-playbook site.yml --tags deploy --list-tasks` (imports) and a `--check --tags deploy` run (includes) execute exactly the intended tasks.

## Checked
Date: 2026-10-24. Documentation: Ansible playbook guide, Tags page (playbooks_tags.rst, devel).
Confirmed:
- Plays, blocks, the roles keyword and static imports inherit tags; include_* tags apply only to the include; the apply keyword and the block form are the documented workarounds.
- Role dependencies are tagged with the role-level tag; play tags also tag implicit tasks.
- Fact gathering is tagged always but can be skipped by skipping or omitting the play's tag; list-tags and list-tasks cannot show dynamic includes.

Method: documentation only; no commands were run.
