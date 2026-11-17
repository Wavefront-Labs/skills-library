---
id: computing-software.cloud-infrastructure-engineering.ansible.block-keywords-vars-and-loop-limitation
name: block-keywords-vars-and-loop-limitation
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, blocks, block-when, block-become, block-vars, block-loop, block-no-loop]
level: practitioner
status: docs-checked
description: "Apply when, become, tags, vars and other keywords once on a block so every task inherits them, and work around the rule that blocks cannot loop."
sources: ["https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_blocks.html", "https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_variables.html#understanding-variable-precedence", "https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_loops.html", "https://github.com/ansible/ansible/blob/devel/lib/ansible/playbook/block.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Block keywords, block vars, and why blocks cannot loop

## Keywords on a block are inherited by the tasks in it
```yaml
- name: Configure database tier
  when: "'db' in group_names"
  become: true
  become_user: postgres
  tags: [db]
  environment:
    PGDATA: /var/lib/pgsql/data
  module_defaults:
    community.postgresql.postgresql_query:
      db: app
  vars:
    pg_version: 16
  block:
    - name: Init cluster
      ansible.builtin.command: /usr/pgsql-{{ pg_version }}/bin/initdb
      args:
        creates: /var/lib/pgsql/data/PG_VERSION
    - name: Create schema
      community.postgresql.postgresql_query:
        query: "CREATE SCHEMA IF NOT EXISTS app"
```
The docs say most of what you can apply to a single task, with the exception of loops, can be
applied at block level, and that the directive does not affect the block itself: it is inherited by the
tasks in it (including tasks pulled in by `include_role`). In the `Block` class the block
accepts, among others, `when`, `tags`, `notify`, `delegate_to`, `collections` and the common base
keywords (become and connection keywords, `vars`, `environment`, `module_defaults`,
`ignore_errors`, `any_errors_fatal`, `no_log`, `check_mode`, `diff`, `throttle`, `timeout`,
`run_once`, `remote_user`). A task can override an inherited keyword (for example `become: false`).

## How `when` on a block is applied
The docs state that the `when` condition is evaluated before each task in the block runs, so it is
re-evaluated per task. To evaluate once, compute a fact first:
```yaml
- ansible.builtin.set_fact:
    do_db: "{{ 'db' in group_names and not db_skip | bool }}"
- name: Database work
  when: do_db | bool
  block:
    - ansible.builtin.debug:
        msg: runs only when do_db is true
```

## Block vars
`vars:` on a block apply to the tasks in the block only. In the documented variable precedence list
"Block vars (for tasks in block only)" sit above role vars and below task vars.

## Blocks cannot loop
`loop` is a task keyword; the docs say block-level directives exclude loops, and `Block` has no
`loop` attribute. Put the block body in a task file and loop over `include_tasks`:
```yaml
- name: Configure each instance
  ansible.builtin.include_tasks: instance.yml     # contains the block with rescue/always
  loop: "{{ instances }}"
  loop_control:
    loop_var: inst
```
A block with `rescue` and `always` inside `instance.yml` gives per-item error handling. To leave a
loop early, use `loop_control: break_when:` (added in ansible-core 2.18).

## Gotchas
- A block `name` is for readability (names for blocks exist since 2.3); a block is not a task.
- `rescue` and `always` need a `block` (the parser rejects them without one).
- `ansible_failed_task` and `ansible_failed_result` exist only in `rescue`; from ansible-core 2.14
  they propagate from an inner block to an outer `rescue`.

## Verify
- [ ] `ansible-playbook --syntax-check` passes (no `loop` on the block).

## Checked
Checked 2026-10-23 against ansible-documentation (playbooks_blocks.rst, playbooks_variables.rst precedence list,
playbooks_loops.rst) and ansible-core devel `playbook/block.py` and `keyword_desc.yml` (devel is 2.23 dev). Fixed:
block-vars precedence is stated by position (above role vars, below task vars), not "level 16"; the old claim
that loops cannot break is stale because `break_when` exists since 2.18. Removed unconfirmed claims about the
exact error text for `loop` on a block, `notify` semantics, and `delegate_facts` interplay.
Method: documentation only; no commands were run.
