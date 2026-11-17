---
id: computing-software.cloud-infrastructure-engineering.ansible.looping-include-tasks-and-include-role
name: looping-include-tasks-and-include-role
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, loops, include-import, loop-include-tasks, include-in-loop, loop-var, include-role, nested-loops]
level: practitioner
status: docs-checked
description: "Loop over include_tasks or include_role to repeat a block of tasks per item, rename loop_var to avoid item collisions, and handle file lookup paths for included files."
sources: ["https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_loops.html", "https://docs.ansible.com/ansible/latest/collections/ansible/builtin/include_tasks_module.html", "https://docs.ansible.com/ansible/latest/collections/ansible/builtin/include_role_module.html", "https://github.com/ansible/ansible-documentation", "https://github.com/ansible/ansible"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Looping include_tasks and include_role

Blocks cannot take a loop (the block docs exempt loops from directives a block can carry); looping a set of tasks means looping an **include**. Static imports cannot be called from a loop. Most keywords, including `loop`, `with_items` and conditionals, apply to `include_tasks`; the do-until loop is not supported there.

```yaml
# main.yml
- name: Configure each virtual host
  ansible.builtin.include_tasks: vhost.yml
  loop: "{{ vhosts }}"
  loop_control:
    loop_var: vhost
    label: "{{ vhost.name }}"
```
```yaml
# vhost.yml
- name: Create docroot for {{ vhost.name }}
  ansible.builtin.file: {path: "/srv/{{ vhost.name }}", state: directory}

- name: Install certificates
  ansible.builtin.copy: {src: "{{ item }}", dest: "/etc/ssl/{{ vhost.name }}/"}
  loop: "{{ vhost.certs }}"           # inner loop uses item; outer is vhost
```
Always set `loop_var` on the outer loop: by default each loop sets `item`, so an inner loop would overwrite the outer value. Ansible detects a loop variable that is already defined and reports it.

## Nested data instead of nested includes
For simple two-level iteration skip the include:
```yaml
loop: "{{ vhosts | subelements('certs') }}"   # item.0 = vhost, item.1 = cert
loop: "{{ users | product(groups_list) | list }}"
```

## Looping a role
```yaml
- name: Deploy each app instance
  ansible.builtin.include_role:
    name: app_instance
  loop: "{{ instances }}"
  loop_control:
    loop_var: instance
  vars:
    app_port: "{{ instance.port }}"
```
Inside the role, use `instance` or the mapped `app_port`.

## File lookup for included files
Relative local paths are searched first in the current role (its `tasks/` subdirectory, then the role directory), then in parent roles, then relative to the task file, then relative to the play file; the current working directory is not searched. Dynamic names:
```yaml
- ansible.builtin.include_tasks: "{{ lookup('ansible.builtin.first_found', ['os/' + ansible_facts.distribution + '.yml', 'os/default.yml']) }}"
```
`first_found` given relative names tries the current task's location first and then goes up through the containing role, play and include locations; its `paths` option lists extra directories to search.

## Performance
Prefer modules that accept lists (`package: name: "{{ list }}"`) and filters over include loops.

## Gotchas
- Tags on the include apply only to the include task; `apply:` accepts task keywords (for example `tags`, `become`) that are applied to the tasks within the include.
- `loop_control.extended: true` exposes `ansible_loop.index`, `first`, `last`, `length` and more, handy in the included file.

## Verify
- [ ] No loop-variable collision warnings or errors when the play runs.

## Checked
Date: 2026-10-24. Documentation: Ansible playbook guide, Loops (playbooks_loops.rst, shared_snippets/with2loop.txt), devel; lookup plugin sources; include_tasks module docs; Search paths page (playbook_pathing.rst); reuse docs.
Confirmed:
- include_* can loop, imports cannot; blocks exempt loops; loop_var collision is detected; apply accepts task keywords such as tags and become; the do-until loop is not supported on include_tasks.
- Local relative path search order; extended loop variables.
- Removed exact warning text, performance, register and output claims.

Method: documentation only; no commands were run.
