---
id: computing-software.cloud-infrastructure-engineering.ansible.passing-vars-to-import-tasks-and-include-tasks
name: passing-vars-to-import-tasks-and-include-tasks
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, include-import, import-tasks-vars, include-tasks, import-tasks]
level: practitioner
status: docs-checked
description: "Pass variables to imported and included task files with vars, understand evaluation time differences, and build reusable parameterised task files."
sources: ["https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_reuse.html", "https://docs.ansible.com/ansible/latest/collections/ansible/builtin/include_tasks_module.html", "https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_variables.html#understanding-variable-precedence"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Passing vars to task files

```yaml
- name: Create app user and dirs (static)
  ansible.builtin.import_tasks: tasks/app_user.yml
  vars:
    app_user: billing
    app_home: /srv/billing

- name: Configure each instance (dynamic, looped)
  ansible.builtin.include_tasks:
    file: tasks/instance.yml
  vars:
    instance_name: "{{ item.name }}"
    instance_port: "{{ item.port }}"
  loop: "{{ instances }}"
  loop_control:
    loop_var: inst_item            # avoid clashing with loops inside instance.yml
```

## Precedence
Variables passed on an include are "include params", entry 21 of 22 in the documented precedence list (after role params, registered vars and set_fact), so they beat role vars, set_fact and inventory and lose only to extra vars. That makes them good for parameterising a reusable file, but a caller cannot override them from inventory.

## Reusable task file pattern
```yaml
# tasks/instance.yml
- name: "{{ instance_name }} | config"
  ansible.builtin.template:
    src: instance.conf.j2
    dest: "/etc/app/{{ instance_name }}.conf"
- name: "{{ instance_name }} | service"
  ansible.builtin.systemd_service:
    name: "app@{{ instance_name }}"
    state: started
    enabled: true
```

## Gotchas
- With free-form `include_tasks: file.yml`, pass `apply` through `args:`; with `file:` it is a normal parameter.
- Do not reuse `item` inside a looped include; set `loop_var`.

## Verify
```bash
ansible-playbook site.yml --list-tasks   # imported tasks listed; included ones are not
```

## Checked

- Date: 2026-10-26. Documentation release: ansible-core stable-2.22 documentation and source (docs and lib/ branch stable-2.22, checked 2026-10-26; 2.21 is the latest GA release, 2.22 GA is scheduled for Nov 2026).
- Confirmed in docs/docsite/rst/playbook_guide/playbooks_variables.rst: include params are item 21 of the precedence list, above role params, registered vars, set_fact and include_vars, below extra vars; in playbooks_reuse.rst: includes are dynamic and support loops, imports are static and cannot be used in a loop, imported tasks appear in --list-tasks and included ones do not.
- Confirmed in modules/include_tasks.py: `file`, `apply` and free-form parameters, apply through args for free-form, loops and conditionals apply to include_tasks unlike import_tasks, the do-until loop is not supported; modules/systemd_service.py exists.
- Removed unconfirmed claims: the lazy-versus-fixed evaluation paragraph and the variables-do-not-leak remark.

Method: documentation only; no commands were run.
