---
id: computing-software.cloud-infrastructure-engineering.ansible.handlers-with-loops-and-notify-from-loops
name: handlers-with-loops-and-notify-from-loops
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, handlers, handler-loop, notify, loops]
level: practitioner
status: docs-checked
description: "Notify handlers from looped tasks (one run regardless of items), loop inside a handler over changed items, and pass item details with listen topics or facts."
sources: ["https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_handlers.html#notifying-and-loops", "https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_loops.html", "https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_loops.html#registering-variables-with-a-loop"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Handlers and loops

## Notify from a loop
```yaml
- name: Deploy vhosts
  ansible.builtin.template:
    src: vhost.conf.j2
    dest: "/etc/nginx/conf.d/{{ item.name }}.conf"
  loop: "{{ vhosts }}"
  notify: Reload nginx
```
Handlers are triggered if the task as a whole changed; with a loop the task is changed if any item
changed. The handler is queued once, and notify alone does not tell it which items changed.
The docs show a templated notify (`notify: Restart {{ item }}`) with handlers named per service and warn
that if any iteration changes, all of those handlers run.

## Act per changed item
Register the loop result and loop in the handler over the changed results (handlers are tasks, and a
registered loop result holds a `results` list with an entry per item):
```yaml
- name: Deploy unit files
  ansible.builtin.template:
    src: "{{ item }}.service.j2"
    dest: "/etc/systemd/system/{{ item }}.service"
  loop: "{{ app_units }}"
  register: unit_files
  notify: Restart changed units

handlers:
  - name: Restart changed units
    ansible.builtin.systemd_service:
      name: "{{ item.item }}"
      state: restarted
      daemon_reload: true
    loop: "{{ unit_files.results | selectattr('changed') | list }}"
    loop_control:
      label: "{{ item.item }}"
```

## Templated handler names (avoid)
Variables in handler names are risky: names are templated early, so the value may not be available and the
play can fail. Prefer the registered-results pattern above, or put variables in the handler's parameters.

## listen for fan-out
```yaml
handlers:
  - name: Restart php-fpm
    ansible.builtin.service:
      name: php-fpm
      state: restarted
    listen: web config changed
  - name: Reload nginx
    ansible.builtin.service:
      name: nginx
      state: reloaded
    listen: web config changed
```

## Gotchas
- If the registering task was skipped, `unit_files.results` may be missing; guard with `| default([])`.
- Notification is per task: there is no notify setting inside `loop_control`.

## Verify
- [ ] Changing one unit template restarts only that unit.

## Checked
Checked 2026-10-23 against ansible-documentation (playbooks_handlers.rst "Notifying and loops", naming and
variables sections; playbooks_loops.rst "Registering variables with a loop") and the existence of
`ansible.builtin.systemd_service` in ansible-core devel. Removed unconfirmed claims about lint behaviour and
empty-list iteration details.
Method: documentation only; no commands were run.
