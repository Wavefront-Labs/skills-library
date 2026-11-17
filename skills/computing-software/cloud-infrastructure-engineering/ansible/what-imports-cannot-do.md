---
id: computing-software.cloud-infrastructure-engineering.ansible.what-imports-cannot-do
name: what-imports-cannot-do
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, include-import, import-limitations, import-tasks, static-vs-dynamic]
level: practitioner
status: docs-checked
description: "Know the limits of static imports: no loops, no host or inventory vars in file names, conditions copied to every task, and when to switch to include."
sources: ["https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_reuse.html#comparing-includes-and-imports-dynamic-and-static-re-use", "https://docs.ansible.com/ansible/latest/collections/ansible/builtin/import_tasks_module.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# What imports cannot do

Imports (`import_tasks`, `import_role`, `import_playbook`) are processed when the playbook is **parsed**, before any host is contacted.

| Need | import | include |
|---|---|---|
| `loop` over the file | no (imports cannot be used in a loop) | yes |
| file name from an inventory variable or fact (`tasks/{{ ansible_facts.os_family }}.yml`) | no (imports are pre-processed at parse time) | yes |
| file name from an extra var | yes (the docs show it for `import_playbook`) | yes |
| task keywords on the statement (for example `when`) | apply to every imported task | apply to the include task only |
| `--list-tasks` / `--list-tags` shows inner tasks | yes | no |
| `--start-at-task` into the file | yes | no |
| task options on the statement apply to inner tasks | yes | no, the include task only (use `apply`) |
| notify handlers defined inside | individual imported handlers can be notified | notify the include itself, which triggers all its tasks |

## Signs that you need an include
- A loop over the file.
- A file name that depends on inventory variables or gathered facts.
- A decision that depends on the results of earlier tasks.

## import_playbook specifics
- It cannot be a task: it sits at playbook top level, outside a play.
- The docs show its path built from an extra var or a play-level var, not from inventory variables.
- There is no `include_playbook`.

## Rule of thumb
Default to imports for structure (visible, listable, taggable). Use includes when the decision depends on runtime data: loops, facts, results.

## Verify
```bash
ansible-playbook site.yml --syntax-check
ansible-playbook site.yml --list-tasks
```

## Checked

- Date: 2026-10-26. Documentation release: ansible-core stable-2.22 documentation and source (docs and lib/ branch stable-2.22, checked 2026-10-26; 2.21 is the latest GA release, 2.22 GA is scheduled for Nov 2026).
- Confirmed in docs/docsite/rst/playbook_guide/playbooks_reuse.rst (comparison table): imports are pre-processed during parsing, task options apply to all child tasks of an import but only to the include task itself, imports cannot be used in a loop, --list-tasks, --list-tags and --start-at-task see imported tasks only, handlers can be notified individually for imports and via the include name for includes, no import_* with inventory variables, import_playbook cannot be a task and there is no include_playbook.
- Removed unconfirmed claims: verbatim error messages, the when-evaluated-once row, import_playbook when semantics.

Method: documentation only; no commands were run.
