---
id: computing-software.cloud-infrastructure-engineering.ansible.flushing-handlers-mid-play
name: flushing-handlers-mid-play
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, handlers, flush-handlers, meta, restart-before-verify]
level: practitioner
status: docs-checked
description: "Run pending handlers before the end of a section with meta flush_handlers, e.g. restart a service before a health check, and know where handlers flush automatically."
sources: ["https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_handlers.html", "https://docs.ansible.com/ansible/latest/collections/ansible/builtin/meta_module.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Flushing handlers mid-play

By default notified handlers run automatically after each of these sections, in order:
`pre_tasks`, `roles`/`tasks`, `post_tasks`. Inside a section, notifications accumulate, and a
handler notified by several tasks still runs once.

## The usual reason to flush
```yaml
tasks:
  - name: Deploy nginx config
    ansible.builtin.template:
      src: nginx.conf.j2
      dest: /etc/nginx/nginx.conf
      validate: nginx -t -c %s
    notify: Reload nginx

  - name: Apply pending handlers now
    ansible.builtin.meta: flush_handlers

  - name: Verify site answers with new config
    ansible.builtin.uri:
      url: "http://localhost/healthz"
      status_code: 200
    retries: 5
    delay: 3
    register: hc
    until: hc.status == 200
```
Without the flush, the check would run against the old configuration and the reload would happen
later. Other cases: a service must restart before a dependent role configures against it, or a
rolling deploy needs the restart before the host is added back to the load balancer in the same play.

## Behaviour details
- `meta: flush_handlers` triggers any handlers that have been notified at that point in the play.
- Once handlers have run, automatically or by a flush, they can be notified and run again in later
  sections of the play.
- Handlers have a single play-level scope, including handlers from roles, so a flush is not limited to one role's handlers.
- Handlers notified within the `roles` section are automatically flushed at the end of the `tasks` section.
- `flush_handlers` cannot itself be used as a handler.

## Gotchas
- If a task fails before the flush, notified handlers do not run on that host by default; use
  `force_handlers` (see the force-handlers skill) or put the flush in a `rescue` section.
- Meta tasks work as handlers only since ansible-core 2.14.

## Verify
- [ ] Output shows `RUNNING HANDLER [...]` right after the flush task and before the verify task.

## Checked
Checked 2026-10-23 against ansible-documentation (playbooks_handlers.rst, "Controlling when handlers run",
"Handlers in roles", "Meta tasks as handlers") and the ansible-core `meta` module documentation. Confirmed
section order, flush semantics and the 2.14 note. Removed unconfirmed claims about `when` on meta tasks, serial
batches, and `import_tasks`/`include_tasks` flush behaviour.
Method: documentation only; no commands were run.
