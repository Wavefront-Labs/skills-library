---
id: computing-software.cloud-infrastructure-engineering.ansible.handler-execution-order-and-change-triggering
name: handler-execution-order-and-change-triggering
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, handlers, handler-order, notify-on-change, notify]
level: practitioner
status: docs-checked
description: "Know when handlers run: only on changed notifications, once per play section, in definition order not notify order, and how changed_when controls triggering."
sources: ["https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_handlers.html", "https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_handlers.html#controlling-when-handlers-run", "https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_error_handling.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Handler execution order and triggering

## Only on change
A task notifies its handlers when its result is changed (`notify` takes a list of handler names or one
string). You can control this with `changed_when`:
- `changed_when: false` means the task never reports a change, so it never notifies.
- `changed_when: true` makes a task such as a file copy always notify, restarting the service every run.
- `command`/`shell` tasks need a meaningful `changed_when`, or they cannot signal changes accurately.

```yaml
- name: Render config
  ansible.builtin.template:
    src: app.conf.j2
    dest: /etc/app.conf
  notify: Restart app            # fires only when the file content changed
```

## Once, at the end of each section
Notified handlers run automatically after each of `pre_tasks`, `roles`/`tasks` and `post_tasks`, in
that order. A handler runs once regardless of how many tasks notify it. `meta: flush_handlers`
runs notified handlers earlier; afterwards they can be notified and run again in later sections.

## Definition order, not notify order
```yaml
handlers:
  - name: Restart database       # defined first -> runs first
    ansible.builtin.service:
      name: postgresql
      state: restarted
  - name: Restart app
    ansible.builtin.service:
      name: app
      state: restarted
```
Handlers run in the order they are defined in the `handlers` section, not the order in the `notify`
list. There is one global play-level scope for handlers; they are added to the play in this order:
handlers from `roles:`, then the `handlers:` section, then roles imported with `import_role`, then roles
included with `include_role` (available only after that task runs).

## Gotchas
- A failure later in the play stops the host before handlers run by default: use `--force-handlers`
  or `force_handlers: true`, or flush before risky steps.
- Handler names should be globally unique: with duplicate names only the last one loaded into the play can be notified.
- Handlers ignore tags.

## Verify
- [ ] The run output shows `RUNNING HANDLER [...]` lines in the order you defined the handlers.

## Checked
Checked 2026-10-23 against ansible-documentation (playbooks_handlers.rst: notifying, order, insertion order,
controlling when handlers run, defining when tasks change, limitations) and playbooks_error_handling.rst.
Confirmed the points above. Removed unconfirmed claims about a handler notifying another handler, `--check`
behaviour for handlers, and the `grep`-based verification.
Method: documentation only; no commands were run.
