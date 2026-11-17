---
id: computing-software.cloud-infrastructure-engineering.ansible.role-handlers-and-cross-role-notification
name: role-handlers-and-cross-role-notification
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, handlers, roles, role-handlers, cross-role-handlers, listen]
level: practitioner
status: docs-checked
description: "Define handlers in roles/handlers/main.yml, notify them from other roles or play tasks, avoid name collisions between roles, and handle include_role handler visibility."
sources: ["Handlers: running operations on change (https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_handlers.html)", "Roles, storing and finding roles (https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_reuse_roles.html)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Role handlers and cross-role notification

## Layout
```
roles/nginx/
  tasks/main.yml        # notify: Reload nginx
  handlers/main.yml     # - name: Reload nginx ...
```
Handlers from every role in the play are loaded into **one play-wide handler list**. Any task in
the play — in another role or in `tasks:` — can notify them.

## Cross-role notification
```yaml
# roles/app/tasks/main.yml
- name: Install vhost for the app
  ansible.builtin.template: {src: vhost.conf.j2, dest: /etc/nginx/conf.d/app.conf}
  notify: "nginx : Reload nginx"     # role-qualified name, unambiguous
```
Better decoupling: the nginx role publishes a topic, consumers notify the topic:
```yaml
# roles/nginx/handlers/main.yml
- name: Reload nginx
  ansible.builtin.service: {name: nginx, state: reloaded}
  listen: nginx config changed
```
`notify: nginx config changed` from any role. Listen topics decouple handlers from their names, but `listen` topics cannot be templated. The handler only exists if the nginx role is in the play, so make the dependency explicit in `meta/main.yml` `dependencies` or document the requirement.

## Name collisions
Handler names live in one global scope. Two roles both defining `Restart service`: only the last one loaded into the play can be notified and executed, shadowing the others. Prevent with
role-prefixed names (`nginx | Restart`), role-qualified notify (`role_name : handler_name`), or listen topics.

## include_role vs import_role / roles:
- `roles:` and `import_role`: handlers are loaded into the play before it runs, so any task can notify them.
- `include_role`: handlers are available at runtime only **after** the `include_role` task has executed, so a task earlier in the play cannot notify them.
- A handler cannot itself run `import_role` or `include_role`.

## Ordering
Handlers run in the order they were defined, not the order of notification. They are inserted into the play in this order: handlers of roles in `roles:`, the play's `handlers:` section, roles loaded with `import_role`, then roles loaded with `include_role`. If app must restart after nginx reloads, order roles accordingly or chain: handler A notifies handler B. Notified handlers run after each of `pre_tasks`, `roles`/`tasks` and `post_tasks`; `meta: flush_handlers` runs them earlier.

## Gotchas
- Handlers ignore tags: `--tags` and `--skip-tags` do not filter them; they run when notified.
- A test of a single role cannot exercise cross-role notifies; test with a playbook that includes both roles.

## Verify
- [ ] `ansible-playbook --list-tasks` won't show handlers; instead trigger a change in the consumer role and confirm `RUNNING HANDLER [nginx : Reload nginx]`.

## Checked

Checked 2026-10-26 against ansible-documentation main (2026-10-21), the handlers page.
- Confirmed: one global play-level handler scope; the insertion order (roles in `roles:`, `handlers:`, `import_role`, `include_role`); a duplicate name is shadowed by the last loaded handler; `role_name : handler_name` notification; `listen` topics (not templatable); handlers from `include_role` exist only after the include executes; handlers cannot run `import_role`/`include_role`; handlers ignore tags; `meta: flush_handlers` and the automatic flush points.
- Removed as unconfirmed: the exact "handler not found" message, the `public` export remark, loop and duplicate-dependency handler behaviour, and the Molecule remark.

Method: documentation only; no commands were run.
