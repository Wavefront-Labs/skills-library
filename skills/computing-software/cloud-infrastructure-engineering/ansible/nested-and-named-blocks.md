---
id: computing-software.cloud-infrastructure-engineering.ansible.nested-and-named-blocks
name: nested-and-named-blocks
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, blocks, block-naming, nested-blocks, block]
level: practitioner
status: docs-checked
description: "Name blocks for readable output and nest blocks to scope become, when, tags and error handling, understanding how keywords inherit and conditions accumulate."
sources: ["https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_blocks.html", "https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_tags.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Nested and named blocks

```yaml
- name: Database tier
  when: inventory_hostname in groups['db']
  become: true
  tags: [db]
  block:
    - name: PostgreSQL packages
      ansible.builtin.dnf: {name: [postgresql-server, postgresql-contrib]}

    - name: Primary-only setup
      when: inventory_hostname == groups['db'] | first
      block:
        - name: Initialise cluster
          ansible.builtin.command: postgresql-setup --initdb
          args: {creates: <data_dir>/PG_VERSION}
        - name: Create replication user
          community.postgresql.postgresql_user: {name: repl, role_attr_flags: REPLICATION}
          become_user: postgres
```

## Naming
- Block names have been available since Ansible 2.3; the docs recommend naming tasks, inside blocks or elsewhere, for better visibility into what is running.

## Inheritance rules
- All tasks in a block inherit the directives set on the block (most task keywords except loops); the block itself is not affected, and the most specific level wins (play, then block, then task).
- `when` **accumulates**: the block's condition is evaluated before each task in it, together with the task's own.
- `tags` accumulate across enclosing levels (the `tags` and `when` fields extend rather than replace).
- `environment` and `module_defaults` lists are also combined across levels, inner values winning.
- Block directives also reach tasks pulled in with `include_role`.

## Error handling scope
A block can have its own `rescue` and `always` sections; the rescue runs after a task in the block returns a failed state, and `ansible_failed_task` and `ansible_failed_result` describe the failure inside it.

## Gotchas
- Deep nesting is hard to read; consider moving inner groups into task files.
- Loops cannot be applied to a block (the documented exception to block-level keywords); loop an `include_tasks` instead.

## Verify
```bash
ansible-playbook db.yml --list-tasks      # tasks listed with the tags they inherit from the blocks
```

## Checked
Checked 2026-10-25 against ansible-documentation devel (commit of 2026-10-21) playbook_guide/playbooks_blocks.rst and playbooks_tags.rst, plus ansible-core devel `playbook/taggable.py`, `playbook/conditional.py` and `playbook/base.py` (the `tags`, `when`, `environment` and `module_defaults` attributes extend). Confirmed: inheritance of block directives, the loop exception, `when` evaluated per task, naming recommendation, rescue and always. Removed unconfirmed claims about where block names are displayed, ansible-lint behaviour for blocks, nested-rescue bubbling and the nesting-depth threshold; replaced the host-specific data directory with a placeholder.
Method: documentation only; no commands were run.
