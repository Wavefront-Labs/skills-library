---
id: computing-software.cloud-infrastructure-engineering.ansible.handler-names-and-listen-topics
name: handler-names-and-listen-topics
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, handlers, listen, handler-naming, dynamic-handler-names, notify]
level: practitioner
status: docs-checked
description: "Notify handlers reliably: unique static handler names, listen topics to group several handlers behind one event, and why templated handler names misbehave."
sources: ["https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_handlers.html", "https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_handlers.html#naming-handlers", "https://github.com/ansible/ansible/blob/devel/lib/ansible/playbook/handler.py", "https://github.com/ansible/ansible/blob/devel/lib/ansible/plugins/strategy/__init__.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Handler names and listen topics

## Names are identifiers
Handlers must be named for tasks to notify them with `notify`. If the name is not found, the run
fails with `The requested handler '<name>' was not found in either the main handlers list nor in the
listening handlers list`. Each handler should have a globally unique name: with duplicates only the
last one loaded into the play can be notified and executed, shadowing the earlier ones.

A role handler can be notified as `role_name : handler_name` (note the spaces around the colon):
`notify: "nginx : Restart nginx"`, which is the way to target a role's handler when another handler has the same name.

## listen: handler topics
```yaml
handlers:
  - name: Restart memcached
    ansible.builtin.service:
      name: memcached
      state: restarted
    listen: restart web stack

  - name: Restart apache
    ansible.builtin.service:
      name: apache2
      state: restarted
    listen: restart web stack

tasks:
  - name: Update shared config
    ansible.builtin.template:
      src: web.conf.j2
      dest: /etc/web.conf
    notify: restart web stack
```
Notifying a topic runs all handlers listening to it, whatever their names. This decouples tasks and
handlers from names, which makes sharing handlers among playbooks and roles easier. Handlers still
run in the order they are defined. In the ansible-core source `listen` is a list of strings, so
one handler can listen on several topics.

## Variables in handler names
The docs advise against variables in handler names: names are templated early, so the value may not
be available; if the variable is missing the whole play fails, and changing it mid-play does not
create a new handler. Put variables in the handler's task parameters instead:
```yaml
handlers:
  - name: Restart web service
    ansible.builtin.service:
      name: "{{ web_service_name | default('httpd') }}"
      state: restarted
```
Handler names can contain a template, but `listen` topics cannot.

## Gotchas
- Notifying the same handler many times runs it once.
- A task that notifies via a loop notifies if any item changed.

## Verify
- [ ] Every `notify` target exists as a handler `name` or `listen` topic.
- [ ] Change the template and run: the expected handlers show `RUNNING HANDLER`.

## Checked
Checked 2026-10-23 against ansible-documentation (playbooks_handlers.rst: naming handlers, variables with
handlers, handlers in roles) and ansible-core devel `plugins/strategy/__init__.py` (error text) and
`playbook/handler.py` (`listen` is a list). Removed unconfirmed claims: case-sensitivity, chained handler
behaviour, the `no-handler` lint rule and the "unrendered name" explanation.
Method: documentation only; no commands were run.
