---
id: computing-software.cloud-infrastructure-engineering.ansible.roles-keyword-vs-import-role-vs-include-role
name: roles-keyword-vs-import-role-vs-include-role
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, include-import, roles-keyword-vs-include, include-role, import-role]
level: practitioner
status: docs-checked
description: "Choose between the roles keyword, import_role and include_role: execution order relative to tasks, handler and variable visibility, tags, loops and conditionals."
sources: ["https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_reuse_roles.html", "https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_reuse.html", "https://docs.ansible.com/ansible/latest/collections/ansible/builtin/include_role_module.html", "https://docs.ansible.com/ansible/latest/collections/ansible/builtin/import_role_module.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# roles: vs import_role vs include_role

## Execution order in a play
1. `pre_tasks` (then handlers they triggered)
2. `roles:` (in listed order, dependencies first)
3. `tasks:`: `import_role` and `include_role` run **here**, in the order defined
4. handlers triggered by roles or tasks
5. `post_tasks` (then their handlers)

So a role in `roles:` always runs before any task in `tasks:`; use `import_role` in `tasks:` when a role must run between specific tasks.

## Comparison
| | roles: | import_role | include_role |
|---|---|---|---|
| processed | parse time | parse time | runtime |
| loop | no | no | yes |
| when | applied to each task | applied to each task | evaluated once, for the include |
| tags on call | applied to all tasks of the role | applied to all tasks | only the include itself (use `apply`) |
| role vars/defaults visible to other play tasks | yes, at parse time (including earlier tasks) | yes, at parse time | only after the include and only with `public: true` |
| handlers available to whole play | yes | yes | yes (the module notes say handlers are made available to the whole play) |
| `--list-tasks` shows inner tasks | yes | yes | no |
| role parameters (`{role: x, param: v}`) | yes, only here | no | no |
| runs once per play even if listed twice | yes (unless parameters differ or `allow_duplicates`) | follows the role's `allow_duplicates` setting (option defaults to true) | `allow_duplicates` option defaults to true |

## Examples
```yaml
- hosts: web
  roles:
    - common
  tasks:
    - name: Wait for storage before app
      ansible.builtin.wait_for: {path: /mnt/data/.ready}
    - ansible.builtin.import_role:
        name: app
    - ansible.builtin.include_role:
        name: vhost
      loop: "{{ sites }}"
      loop_control: {loop_var: site}
```

## Gotchas
- include_role with `tasks_from` for one entry point: `include_role: {name: app, tasks_from: upgrade}`.
- Only the `roles:` keyword accepts role parameters; `vars:` is not the same as a role parameter (this matters for de-duplication).
- Since ansible-core 2.15, `vars:` on a `roles:` entry no longer leak into the play's variable scope.
- `include_role` and `import_role` do not work in handlers.

## Verify
```bash
ansible-playbook site.yml --list-tasks      # roles: and import_role tasks are listed in order; include_role contents are not
```

## Checked
Checked 2026-10-25 against ansible-documentation devel (commit of 2026-10-21) playbook_guide/playbooks_reuse_roles.rst (execution order, include versus import, tags, role parameters, `vars:` scoping note), playbooks_reuse.rst (comparison table: loops, `--list-tasks`, task options) and the ansible-core `include_role` and `import_role` module documentation (`public`, `allow_duplicates`, handlers note, handlers limitation). Confirmed: execution order, loop and conditional behaviour, tag behaviour, listing behaviour, role parameter limitation. Removed the unconfirmed claim that mixing `roles:` and `import_role` runs a role once; replaced the handler row with the module's documented statement.
Method: documentation only; no commands were run.
