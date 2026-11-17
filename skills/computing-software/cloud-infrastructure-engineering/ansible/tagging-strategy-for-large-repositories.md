---
id: computing-software.cloud-infrastructure-engineering.ansible.tagging-strategy-for-large-repositories
name: tagging-strategy-for-large-repositories
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, tags, tag-strategy, roles, playbook-structure]
level: practitioner
status: docs-checked
description: "Design a tagging scheme for large Ansible repos: role-name tags, lifecycle tags (install, config, service), never-tagged debug and dangerous tasks, and enforcement."
sources: ["https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_tags.html", "https://docs.ansible.com/ansible/latest/tips_tricks/ansible_tips_tricks.html", "https://github.com/ansible/ansible-documentation", "https://github.com/ansible/ansible"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Tagging strategy for large repositories

Without a scheme, tags become a pile of one-offs nobody trusts. A scheme that scales:

## 1. Role-name tag, applied at the call site
```yaml
roles:
  - {role: nginx, tags: [nginx]}
  - {role: postgres, tags: [postgres]}
```
`--tags nginx` runs one role from site.yml (plus `always` tasks). Applying at the call site (static `roles:` or `import_role`) tags every task, and the role's dependencies, without touching the role.

## 2. Lifecycle tags inside roles (small fixed vocabulary)
| Tag | Meaning |
|---|---|
| `install` | packages, binaries |
| `config` | templates, files |
| `service` | enable/start |
| `users` | accounts, keys |
| `firewall` | ports, rules |

So `--tags config` re-renders configuration estate-wide quickly, and `--tags nginx --skip-tags install` is "nginx config only".

## 3. Safety tags
- `never` + specific tag for destructive or debug tasks: `tags: [never, wipe_data]`, `tags: [never, debug]`.
- `always` sparingly: only for tasks every selection needs (loading vars, preflight asserts).

## 4. Rules
- Document the vocabulary in the repo README; review new tags.
- Tag at the highest sensible level (role, block), not every task.
- Remember include semantics: a tag on a dynamic include applies only to the include; use `apply: {tags: [...]}` to tag its tasks.
- Do not use tags for environment selection; use inventory groups and limits.
- Tags on handlers are ignored, so do not design handler selection around them.

## Enforce
- A CI job runs `ansible-playbook site.yml --list-tags` and compares the output to an allowed list (the command prints every tag per play, but not tags inside dynamic includes).

## Verify
```bash
ansible-playbook site.yml --list-tags
```

## Checked
Date: 2026-10-24. Documentation: Ansible playbook guide, Tags page (playbooks_tags.rst, devel).
Confirmed:
- Role-level tags tag all tasks and dependencies; always and never usage; handlers ignore tags; list-tags output limits.
- Removed unverifiable claims about ansible-lint, tips-and-tricks content and a shell pipeline.

Method: documentation only; no commands were run.
