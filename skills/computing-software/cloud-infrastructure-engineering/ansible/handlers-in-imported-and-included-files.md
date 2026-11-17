---
id: computing-software.cloud-infrastructure-engineering.ansible.handlers-in-imported-and-included-files
name: handlers-in-imported-and-included-files
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, handlers, handler-includes, import-handlers, include-tasks, import-tasks]
level: advanced
status: docs-checked
description: "Split handlers into separate files with import_tasks or include_tasks under handlers:, and know how notify resolves to the include versus the inner handler names."
sources: ["https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_handlers.html#includes-and-imports-in-handlers", "https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_reuse.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Handlers from imported and included files

Both static imports and dynamic includes can appear in the `handlers:` section, with different notify semantics.

## import_tasks: notify the inner names
```yaml
# handlers/main.yml
- ansible.builtin.import_tasks: handlers/nginx.yml
- ansible.builtin.import_tasks: handlers/php.yml
```
```yaml
# handlers/nginx.yml
- name: Reload nginx
  ansible.builtin.service:
    name: nginx
    state: reloaded
```
A static import used as a handler is effectively rewritten by the handlers inside it before the play
runs. The import itself cannot be notified; the tasks inside it can be notified individually, so
`notify: Reload nginx` works. The reuse docs likewise list "can trigger individual imported handlers".

## include_tasks: notify the include
```yaml
handlers:
  - name: Restart app stack
    ansible.builtin.include_tasks: restart_stack.yml
```
```yaml
# restart_stack.yml - plain task list
- ansible.builtin.service:
    name: app-worker
    state: restarted
- ansible.builtin.service:
    name: app-web
    state: restarted
```
Notifying a dynamic include as a handler executes all tasks within the include. It is not possible to
notify a handler defined inside a dynamic include, so inner task names cannot be notified. This is
how to make a multi-step handler.

## Choosing
| Want | Use |
|---|---|
| Organise many independent handlers into files | `import_tasks` |
| One notification triggers a sequence | `include_tasks` (or `listen` on several handlers) |
| File name from a variable | `include_tasks` (include file names are templated; imports are processed before the run) |

`listen` is the alternative for sequences: several handlers listening to one topic run in definition order.

## Limitations (documented)
- A handler cannot run `import_role` or `include_role`.
- Handlers ignore tags.

## Verify
- [ ] Trigger the notifying task: the output lists the inner handler (import) or the include's tasks (include).

## Checked
Checked 2026-10-23 against ansible-documentation (playbooks_handlers.rst "Includes and imports in handlers"
and "Limitations"; playbooks_reuse.rst comparison table). Removed unconfirmed claims about facts in import
filenames, deduplication of included handler tasks, and the "handler not found" message for inner included names
(the docs say only that it is not possible).
Method: documentation only; no commands were run.
