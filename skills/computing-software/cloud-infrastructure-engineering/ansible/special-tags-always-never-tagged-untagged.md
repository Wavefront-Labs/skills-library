---
id: computing-software.cloud-infrastructure-engineering.ansible.special-tags-always-never-tagged-untagged
name: special-tags-always-never-tagged-untagged
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, tags, always-tag, never-tag, tagged, untagged, skip-tags]
level: practitioner
status: docs-checked
description: "Use the reserved tags always and never on tasks, and the tagged, untagged and all selectors with --tags and --skip-tags, to make tag-scoped runs safe."
sources: ["https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_tags.html", "https://github.com/ansible/ansible-documentation", "https://github.com/ansible/ansible"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Special tags: always, never, tagged, untagged

## always
A task tagged `always` runs on every invocation, whatever `--tags` says, unless you explicitly
skip it with `--skip-tags always` or with another tag defined on that task.
```yaml
- name: Load environment-specific vars
  ansible.builtin.include_vars: "{{ env }}.yml"
  tags: [always]
```
Use for prerequisites every tag-scoped run needs: vars loading, asserts. The internal
fact-gathering task and the role argument-spec validation task are tagged `always` by default.

## never
A task tagged `never` is skipped unless one of its **other** tags is requested.
```yaml
- name: Drop and recreate the database
  community.postgresql.postgresql_db: {name: app, state: absent}
  tags: [never, db-reset]
```
Runs only when you request one of its other tags (`--tags db-reset`). Ideal for destructive, debug or one-off maintenance tasks
kept in the main playbook. Requesting `--tags never` (or `--tags all,never`) runs the never-tagged tasks too; avoid that for destructive ones.

## Selectors for the CLI
| Selector | With `--tags` |
|---|---|
| `tagged` | only tasks with at least one tag (`never` overrides) |
| `untagged` | only tasks with no tags (`always` overrides) |
| `all` (default) | all tasks, tagged and untagged, except `never` |

```bash
ansible-playbook site.yml --tags untagged        # run only the "core" untagged tasks
ansible-playbook site.yml --tags tagged --skip-tags slow   # skip wins over select
ansible-playbook site.yml --list-tags            # what tags exist
ansible-playbook site.yml --tags nginx --list-tasks   # preview selection
```

## Gotchas
- `--skip-tags always` also skips fact gathering and role argument-spec validation, so templates using facts then fail.
- Tags are inherited from blocks, plays, roles and static imports, so `untagged` may match fewer tasks than expected.
- Skipping takes precedence over selecting: `--tags a,b --skip-tags b` runs only `a`.
- Handlers ignore tags; they run when notified.
- `tags` is applied while the playbook is pre-processed, so tag selection also overrides block `rescue`/`always` sections that are not themselves tagged.

## Verify
- [ ] `--list-tasks` with the intended `--tags` shows the always-tasks plus the selected ones, and no never-tasks unless asked.

## Checked
Date: 2026-10-24. Documentation: Ansible playbook guide, Tags page (playbooks_tags.rst, devel).
Confirmed:
- always and never semantics, --tags all, tagged, untagged and all,never; always is skipped only by --skip-tags always or another tag on the task.
- Fact gathering and role argument-spec validation carry always by default.
- Skip takes precedence over select; the --skip-tags tagged and untagged forms and AWX tag claims were removed because the docs do not cover them.

Method: documentation only; no commands were run.
