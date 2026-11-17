---
id: computing-software.cloud-infrastructure-engineering.ansible.include-role-public-and-apply-keywords
name: include-role-public-and-apply-keywords
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, include-import, role-public, apply-keyword, include-role, tasks-from, defaults-from]
level: advanced
status: docs-checked
description: "Use include_role options public, apply, tasks_from, vars_from, defaults_from and handlers_from to control variable visibility and push keywords like tags and become into the role."
sources: ["https://docs.ansible.com/ansible/latest/collections/ansible/builtin/include_role_module.html", "https://docs.ansible.com/ansible/latest/collections/ansible/builtin/import_role_module.html", "https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_tags.html#tag-inheritance-for-includes-blocks-and-the-apply-keyword"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# include_role: public and apply

## public: variable visibility
By default `include_role` keeps the role's `defaults/` and `vars/` **private** to the role
(`public: false`). Tasks after the include cannot see `nginx_port` defined in the role's defaults.
```yaml
- ansible.builtin.include_role:
    name: nginx
    public: true            # expose defaults/vars to the rest of the play after the include
- ansible.builtin.debug: {var: nginx_port}
```
`import_role` and `roles:` expose variables to the play at parse time, so earlier roles and tasks see them too. That default is controlled by `private_role_vars` (ansible.cfg, default false); since 2.17 `import_role` and `include_role` can override it per use with `public`.

## apply: push keywords onto the role's tasks
Keywords on the `include_role` task apply to the include itself only. `apply` passes them down:
```yaml
- ansible.builtin.include_role:
    name: app
    apply:
      tags: [deploy]
      become: true
      become_user: app
      environment: {HTTP_PROXY: "{{ proxy }}"}
      delegate_to: "{{ deploy_host }}"
  tags: [deploy]       # needed so --tags deploy selects the include itself
  when: deploy_enabled | bool
```
`apply` accepts a hash of task keywords (for example `tags`, `become`) applied to all tasks within the included role. Task-level keywords, loops and conditionals written on the `include_role` task apply only to the include itself, so loops and `when` belong there. `include_role` ignores some keywords such as `until` and `retries`, and does not work in handlers.

## Picking entry points
```yaml
- ansible.builtin.include_role:
    name: postgres
    tasks_from: backup        # tasks/backup.yml instead of main.yml
    vars_from: replica        # vars/replica.yml
    defaults_from: minimal    # defaults/minimal.yml
    handlers_from: noop       # handlers/noop.yml
    allow_duplicates: true
    rolespec_validate: true   # default true: validate against meta/argument_specs.yml if a spec exists
```
`import_role` (static) has the same entry-point options, and `allow_duplicates` defaults to true on both. Role argument specs are keyed by entry-point name (`main` unless another tasks file is used).

## Gotchas
- `public: true` exposes vars only **after** the include runs; with `roles:` or `import_role` they are available to earlier roles and tasks as well.
- Tags on an `include_*` task apply only to the include itself, so a tag needed to select the role's tasks goes in `apply` and, to select the include, on the task as well.
- Handlers from an included role are made available to the whole play.

## Verify
- [ ] `ansible-playbook --tags deploy` runs the role's tasks (the `apply` tags work) as well as the include.
- [ ] `debug: var=<role var>` after the include shows the value only when `public: true`.

## Checked
Checked 2026-10-25 against ansible-core devel `modules/include_role.py` and `modules/import_role.py` documentation, `config/base.yml` (DEFAULT_PRIVATE_ROLE_VARS) and ansible-documentation devel (commit of 2026-10-21) playbook_guide/playbooks_tags.rst and playbooks_reuse_roles.rst. Confirmed: `public`, `apply`, `tasks_from`, `vars_from`, `defaults_from`, `handlers_from`, `allow_duplicates` and `rolespec_validate` options and defaults, include-only keyword scope, tag behaviour with `apply`, handlers availability. Removed unconfirmed claims about `when` inside `apply`, loop-iteration variable visibility and the argument-spec naming rule beyond entry points.
Method: documentation only; no commands were run.
