---
id: computing-software.cloud-infrastructure-engineering.ansible.playbook-structure-and-roles
name: playbook-structure-and-roles
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, ansible-playbook, playbook-structure, project-layout, site-yml, roles, import-role, include-role, import-tasks, include-tasks, static-vs-dynamic, role-dependencies, meta-main, argument-specs, pre-tasks, post-tasks, tags, block-rescue-always, delegate-to, run-once, collections, ansible-cfg, import-playbook, tasks-from, list-tags]
level: practitioner
status: docs-checked
description: "Lay out an Ansible project: site.yml importing per-tier plays, roles, static vs dynamic includes and tag propagation, argument_specs, block/rescue."
sources:
  - https://docs.ansible.com/projects/ansible/latest/playbook_guide/playbooks_reuse.html
  - https://docs.ansible.com/projects/ansible/latest/playbook_guide/playbooks_reuse_roles.html
  - https://docs.ansible.com/projects/ansible/latest/playbook_guide/playbooks_blocks.html
  - https://docs.ansible.com/projects/ansible/latest/playbook_guide/playbooks_tags.html
  - https://docs.ansible.com/projects/ansible/latest/playbook_guide/playbooks_delegation.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Ansible playbook structure and roles — a project you can navigate and slice

**Goal:** a repository where any operator can find what configures a host, run just one
tier or one concern with `--limit`/`--tags`, and reuse roles across projects. Writing
idempotent tasks inside those roles is
`computing-software.cloud-infrastructure-engineering.ansible.idempotent-playbooks-and-roles`.

## 1. Project layout
```
ansible.cfg                 # project settings such as roles_path
requirements.yml            # pinned collections and roles
inventories/{prod,stage}/   # hosts + group_vars + host_vars per environment
site.yml                    # imports the tier playbooks, nothing else
playbooks/
  webservers.yml  dbservers.yml  bootstrap.yml
roles/                      # project-specific roles
collections/ansible_collections/<NS>/<NAME>/roles/   # optional: shared roles as a collection
```
```yaml
# site.yml
- ansible.builtin.import_playbook: playbooks/bootstrap.yml
- ansible.builtin.import_playbook: playbooks/webservers.yml
- ansible.builtin.import_playbook: playbooks/dbservers.yml
```
One play per host group; the play is thin and only lists roles plus orchestration.

## 2. A tier playbook
```yaml
- name: Web tier
  hosts: webservers
  become: true
  serial: 5
  pre_tasks:
    - name: Drain from load balancer
      ansible.builtin.uri: { url: "http://lb.internal/drain/{{ inventory_hostname }}", method: POST }
      delegate_to: localhost
  roles:
    - role: common
      tags: [common]
    - role: nginx
      tags: [nginx]
  post_tasks:
    - name: Re-enable in load balancer
      ansible.builtin.uri: { url: "http://lb.internal/enable/{{ inventory_hostname }}", method: POST }
      delegate_to: localhost
```
Order of execution: `pre_tasks` → their handlers → `roles` → `tasks` → handlers →
`post_tasks` → handlers.

## 3. Import (static) vs include (dynamic)
| | `import_*` | `include_*` |
|---|---|---|
| Resolved | at parse time | at run time, when reached |
| `tags:` on it | applied to **every** task inside | apply to the include itself only |
| Loops | not allowed | allowed (`loop:` over include_role) |
| `--list-tasks`, `--start-at-task` | sees inner tasks | does not |

Rule: **import by default**; include only for loops or fact-dependent filenames. To
make tags reach tasks inside an include, use
`include_role: { name: x, apply: { tags: [x] } }` plus `tags: [x]` on the include.

## 4. Role interface
- Validate inputs with `meta/argument_specs.yml` (Ansible 2.11+); validation runs
  automatically before the role's tasks:
  ```yaml
  argument_specs:
    main:
      short_description: Install and configure nginx
      options:
        nginx_listen_port: { type: int, default: 80 }
        nginx_sites: { type: list, elements: dict, required: true }
  ```
- Split large roles with `tasks/main.yml` importing `install.yml`, `config.yml`,
  `service.yml`; give extra entry points (`tasks_from: upgrade`) instead of boolean modes.
- Role dependencies in `meta/main.yml` always run before the role that lists them, and are
  deduplicated at the play level; prefer listing roles explicitly in the play so ordering is visible.

## 5. Error handling and orchestration
```yaml
- block:
    - ansible.builtin.include_tasks: migrate.yml
  rescue:
    - ansible.builtin.include_tasks: rollback.yml
    - ansible.builtin.fail: { msg: "Migration failed and was rolled back" }
  always:
    - ansible.builtin.include_tasks: unlock.yml
```
- `run_once: true` + `delegate_to: "{{ groups['dbservers'][0] }}"` for one-off cluster actions.

## Gotchas
- Tags on `include_tasks` / `include_role` do not reach inner tasks without `apply`.
- `--tags` runs only tasks carrying the tag and skips the rest, including block `rescue`/`always` sections that lack it.
- Role deduplication happens only at the play level, so separate plays can rerun a role.
- Under delegation, connection and `become` options are templated from the delegated-to host, not the original task host.
- The `public` option on `import_role`/`include_role` controls whether the role's `vars/` and `defaults/` enter play scope.

## Verify
- [ ] `ansible-playbook site.yml --list-tasks --list-tags` shows every intended task and tag (tasks inside includes are not listed).
- [ ] `--tags nginx --limit web01 --check` touches only nginx tasks on one host.
- [ ] Calling a role with a missing required argument fails before any task runs.
- [ ] `ansible-lint` passes; no bare `include:` (deprecated) remains.
- [ ] `site.yml` contains only `import_playbook` lines.

## Checked
2026-11-01. Confirmed against the Ansible playbook guide pages on reusing artifacts (import vs include table: parse time vs run time, loops, `--list-tasks`, `--list-tags`, `--start-at-task`), roles (execution order, `meta/argument_specs.yml` from 2.11 with a validation task tagged `always`, dependency order and play-level deduplication, `tasks_from`, `public`), tags (import inheritance, `apply` for includes), blocks and delegation (`delegate_to`, `serial`, `run_once`). Removed: `any_errors_fatal` and percentage `serial` examples, fact-dependent include filename row, the `--tags` and `become: false` and flush_handlers gotchas that the pages do not support.
Method: documentation only; no commands were run.
