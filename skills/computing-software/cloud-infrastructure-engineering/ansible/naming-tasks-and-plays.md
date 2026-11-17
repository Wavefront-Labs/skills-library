---
id: computing-software.cloud-infrastructure-engineering.ansible.naming-tasks-and-plays
name: naming-tasks-and-plays
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, playbook-syntax, task-naming, name-tasks, name-rule, start-at-task, readable-output]
level: intro
status: docs-checked
description: "Name every play and task so output, --start-at-task, --list-tasks and controller job logs are readable, following the ansible-lint name rule conventions."
sources: ["https://ansible.readthedocs.io/projects/lint/rules/name/", "https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_startnstep.html", "https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_loops.html#limiting-loop-output-with-label"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Naming tasks and plays

Names are the interface: they appear in output, `--list-tasks`, `--start-at-task`, `--step`,
callback plugins, and controller job events. Unnamed tasks show as `TASK [ansible.builtin.copy]`,
which is useless when a role has twelve copies.

## Rules that ansible-lint enforces
- `name[missing]` — every task and play has a name.
- `name[casing]` — names start with an uppercase letter.
- `name[template]` — Jinja only at the **end** of a name: `Install {{ pkg }}` ok, `{{ pkg }} install` flagged (rendering a templated name is not always possible, and fixed text up front helps find the failing task in the source).
- `name[play]` — plays need names too.
- `name[unique]` — task names are unique within a play (including `pre_tasks`, `tasks`, `post_tasks` and `handlers`); this keeps `--start-at-task` reliable.
- `name[prefix]` (opt-in via `enable_list`) — in included task files other than `main.yml`, prefix with the file path stem: `Restart server` in `tasks/deploy.yml` becomes `deploy | Restart server`. `main.yml` is exempt.

## Good names
Imperative, describe the desired state, not the module:
```yaml
- name: Ensure nginx is installed
- name: Deploy nginx site config for {{ app_name }}
- name: Restart nginx               # handler; notify by exactly this string
```
Avoid: `copy file`, `shell`, `task 3`.

## Why it matters operationally
```bash
ansible-playbook site.yml --list-tasks
ansible-playbook site.yml --start-at-task "Deploy nginx site config for shop"
ansible-playbook site.yml --step
```
`--start-at-task` matches the task name or a shell-style wildcard pattern of it (for example `"Deploy nginx*"`); if the play has play-level fact gathering or argument validation, those implicit tasks run first. Unique names (`name[unique]`) make this reliable.

Ansible adds the role name to tasks of a role, so do not repeat it in the task name.

## Loops
The task banner is printed once for the whole loop, so `{{ item }}` has no per-item value in a name. Per-item output lines come from `loop_control.label`, which keeps them short instead of dumping the whole dict (it is for readability, not for protecting secrets; use `no_log` for that):
```yaml
- name: Create users
  ansible.builtin.user: {name: "{{ item.name }}"}
  loop: "{{ users }}"
  loop_control: {label: "{{ item.name }}"}
```

## Gotchas
- Handler names are identifiers; renaming one silently breaks every `notify:` that used the old string (use `listen:` topics to decouple).
- The templating inside a name is discouraged because rendering it is not always possible (`name[template]`).
- Do not put secrets in names; `no_log` hides task results, not the task name.

## Verify
- [ ] `ansible-lint` reports no `name[...]` findings (`name[casing]` can be fixed automatically with `--fix`).
- [ ] `--list-tasks` reads as a runbook.

## Checked
Checked 2026-10-25 against the ansible-lint `name` rule page (src/ansiblelint/rules/name.md on GitHub), ansible-documentation devel (commit of 2026-10-21) playbook_guide/playbooks_startnstep.rst and playbooks_loops.rst, and the ansible-core devel `executor/play_iterator.py` (the `--start-at-task` match uses the name or an fnmatch pattern). Confirmed: the `name[...]` sub-rules including `name[unique]` and the opt-in `name[prefix]` format, `--start-at-task` matching and implicit play-level tasks, and the `label` note. Corrected the `name[prefix]` example (`main.yml` is exempt) and added `name[unique]`. Removed unconfirmed claims about duplicate names, banner values and secrets in logs.
Method: documentation only; no commands were run.
