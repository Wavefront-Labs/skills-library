---
id: computing-software.cloud-infrastructure-engineering.ansible.conditionals-on-imports-vs-includes
name: conditionals-on-imports-vs-includes
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, conditionals, conditional-import, when-import, include-tasks, import-tasks, dynamic-reuse]
level: practitioner
status: docs-checked
description: "Know how when behaves on import_tasks/import_role (copied to every task, re-evaluated each time) versus include_tasks/include_role (evaluated once), and pick the right one."
sources: ["https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_conditionals.html#conditionals-with-reuse", "https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_reuse.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Conditionals on imports vs includes

## import_* (static): when is applied to every task
```yaml
- ansible.builtin.import_tasks: setup_db.yml
  when: db_enabled | bool
```
Ansible applies the condition to all tasks in the imported file and evaluates each task separately
(the docs compare this to tag inheritance). Consequence:
```yaml
# setup_db.yml, imported with: when: x is not defined
- ansible.builtin.set_fact:
    x: foo          # task 1 runs: x is not yet defined
- ansible.builtin.debug:
    var: x          # task 2 is SKIPPED: x is now defined
```
Any task inside that changes a variable used in the condition affects the tasks after it.

## include_* (dynamic): when applies to the include itself
```yaml
- ansible.builtin.include_tasks: setup_db.yml
  when: db_enabled | bool
```
The condition is evaluated when the include task runs and does not apply to the individual tasks
in the file, so in the example above both tasks run when `x` is undefined.

## Which to use
| Need | Use |
|---|---|
| Condition depends on a value changed inside the file | `include_tasks` |
| File name from an inventory variable | `include_tasks` (imports cannot use `{{ inventory_var }}` in the name) |
| `--list-tasks` and `--start-at-task` must see inner tasks | `import_tasks` |
| Notify individual handlers from the file | `import_tasks` (includes cannot trigger handlers within them) |

Roles follow the same rule: `roles:` with `when` and `import_role` with `when` add the condition
to all tasks in the role; `include_role` with `when` applies it to the include.

## Playbook level
`import_playbook` accepts a condition too; Ansible then returns a skipped message for every task
on every host that does not match, which creates repetitive output. The docs suggest the
`group_by` module can be a more streamlined way to get the same result.

## Verify
- [ ] `--list-tasks` lists imported tasks but not tasks inside includes, which tells you which mechanism is in use.

## Checked
Checked 2026-10-23 against ansible-documentation (playbooks_conditionals.rst "Conditionals with reuse";
playbooks_reuse.rst comparison table). Confirmed the import/include semantics, `import_playbook` note and table
rows. Removed unconfirmed claims about fact-based file names, handler notify chains, tag `apply`, run-time cost,
and "facts gathering" on conditional playbooks.
Method: documentation only; no commands were run.
