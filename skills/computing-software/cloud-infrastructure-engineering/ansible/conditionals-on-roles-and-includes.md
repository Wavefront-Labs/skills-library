---
id: computing-software.cloud-infrastructure-engineering.ansible.conditionals-on-roles-and-includes
name: conditionals-on-roles-and-includes
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, conditionals, conditional-role, include-role, import-role]
level: practitioner
status: docs-checked
description: "Apply when to roles correctly: roles keyword and import_role push the condition to every task, include_role evaluates once, and the facts-changing trap."
sources: ["https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_conditionals.html#conditionals-with-roles", "https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_reuse.html", "https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_reuse_roles.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Conditionals on roles

## Three ways, three behaviours
The docs describe three ways to apply conditions to roles:
1. Put `when` under the `roles` keyword: the condition is added to all tasks in the role.
2. Put `when` on a static `import_role`: the same condition is added to all tasks in the role.
3. Put conditions on individual tasks or blocks inside the role. To select or skip some tasks inside
   the role you must use the dynamic `include_role` with the condition on the include; Ansible then
   applies the condition to the include itself plus any role tasks that carry the same `when`.
```yaml
roles:
  - role: nginx
    when: install_web | bool          # static: copied onto every task in the role

tasks:
  - ansible.builtin.import_role:
      name: nginx
    when: install_web | bool          # static: same as above

  - ansible.builtin.include_role:
      name: nginx
    when: install_web | bool          # dynamic: applies to the include itself
```

## The trap with static conditions
Because the condition is evaluated for every task, a task inside the role that changes its input
affects the rest:
```yaml
- role: app_install
  when: app_installed_version is not defined
# if a task inside sets app_installed_version, the following role tasks are skipped
```
Use `include_role`, or a dedicated variable that the role does not touch.

## Output
- Static: skipped messages for every task when the condition is false.
- Dynamic: the include is skipped; with `--list-tasks`, tasks inside includes are not listed and
  imported ones are.

## Inside the role
Guard inside the role (conditions on tasks or blocks, with role defaults) so callers do not need to
know the role's internals.

## Verify
```bash
ansible-playbook site.yml -e install_web=false --list-tasks
```
With a static role the tasks are listed; with `include_role` only the include appears.

## Checked
Checked 2026-10-23 against ansible-documentation (playbooks_conditionals.rst "Conditionals with roles" and
"Conditionals with reuse"; playbooks_reuse.rst table). Removed unconfirmed claims about `meta/main.yml`
dependency conditions, `include_role` with `loop`, and `--list-tags` visibility.
Method: documentation only; no commands were run.
