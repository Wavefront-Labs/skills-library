---
id: computing-software.cloud-infrastructure-engineering.ansible.tags-and-handlers
name: tags-and-handlers
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, tags, handler-tags, handlers, notify]
level: practitioner
status: docs-checked
description: "Understand how tags interact with handlers: notified handlers run regardless of tags, tags on handlers are ignored for selection, and flush_handlers with tags."
sources: ["https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_tags.html", "https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_handlers.html", "https://github.com/ansible/ansible-documentation", "https://github.com/ansible/ansible"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Tags and handlers

## Selected tasks still trigger their handlers
```yaml
tasks:
  - name: Render nginx config
    ansible.builtin.template: {src: nginx.conf.j2, dest: /etc/nginx/nginx.conf}
    notify: Reload nginx
    tags: [config]
handlers:
  - name: Reload nginx
    ansible.builtin.service: {name: nginx, state: reloaded}
```
`ansible-playbook site.yml --tags config` → template runs; if it changed, **Reload nginx runs** even though the handler has no `config` tag. Handlers are triggered by notification, not by tag selection.

## Tags on handlers
Handlers ignore all tags and cannot be selected for or against, so a notified handler runs whatever the tag selection. If a restart must be optional, gate it with a variable:
```yaml
handlers:
  - name: Reload nginx
    ansible.builtin.service: {name: nginx, state: reloaded}
    when: allow_restarts | default(true) | bool
```

## flush_handlers and tags
`meta: flush_handlers` is a task; skipping `meta` tasks with tags is supported from Ansible 2.11, so with `--tags` it is skipped unless tagged with the selected tag or `always`:
```yaml
- ansible.builtin.meta: flush_handlers
  tags: [always]
```
Otherwise queued handlers wait until the end of the play.

## Gotchas
- `--tags` on a play where the notifying task is skipped: no notification, no handler — expected but often mistaken for a handler bug.

## Verify
```bash
ansible-playbook site.yml --tags config --check
```
The output should show a `RUNNING HANDLER` line for each notified handler.

## Checked
Date: 2026-10-24. Documentation: Ansible playbook guide, Tags page (playbooks_tags.rst, devel); Handlers page; meta module docs.
Confirmed:
- Handlers ignore tags and cannot be selected for or against.
- Skipping meta tasks with tags is supported from 2.11 (meta module notes), so flush_handlers can be tagged.
- Removed the unreliable-across-versions claim and the grep-based check.

Method: documentation only; no commands were run.
