---
id: computing-software.cloud-infrastructure-engineering.ansible.multiple-failed-when-and-changed-when-conditions
name: multiple-failed-when-and-changed-when-conditions
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, error-handling, failed-when-multiple, failed-when, changed-when]
level: practitioner
status: docs-checked
description: "Combine several failed_when conditions as lists (AND) or with or, pair them with changed_when, and evaluate rc, stdout and stderr together correctly."
sources: ["https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_error_handling.html", "https://github.com/ansible/ansible-documentation", "https://github.com/ansible/ansible"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Multiple failed_when and changed_when conditions

## List = AND
Lists of `failed_when` (or `changed_when`) conditions are joined with an implicit `and`: the task fails (or reports changed) only when **all** conditions are met.
```yaml
- name: Apply schema migrations
  ansible.builtin.command: /opt/app/bin/migrate --apply
  register: mig
  failed_when:
    - mig.rc != 0
    - "'already applied' not in mig.stderr"      # fail only if rc!=0 AND not the benign message
  changed_when:
    - mig.rc == 0
    - "'No migrations' not in mig.stdout"
```

## or for any-of
```yaml
failed_when: >-
  mig.rc not in [0, 3] or
  'FATAL' in mig.stdout or
  mig.stderr is search('permission denied', ignorecase=True)
```
To fail or report a change when **any** condition holds, put them in one string with an explicit `or`. Use the folded scalar `>-` for long expressions; no `{{ }}` (conditionals are templated implicitly).

## What the keywords decide
- `failed_when` defines what "failure" means for the task; `changed_when` defines whether the task reports a change, which also decides whether handlers are triggered and what the statistics count.
- Be explicit about `rc`: a condition that ignores the return code decides failure without it.

## Common combos
| Command style | changed_when | failed_when |
|---|---|---|
| idempotent CLI returning 0/2 | `rc == 2` | `rc not in [0, 2]` |
| grep check | `false` | `rc > 1` |
| "already exists" errors | `rc == 0` | `rc != 0 and 'exists' not in stderr` |

## Gotchas
- `changed_when: false` marks a read-only task as never changed.
- Since 2.21 the implicit `_task` variable (for example `_task.result.rc`) can replace `register` in `failed_when`, `changed_when`, `when`, `until` and `break_when`.

## Verify
- [ ] Test both the benign and the real error paths (e.g. with a wrapper script returning each rc).

## Checked
Date: 2026-10-24. Documentation: Ansible playbook guide, Error handling (playbooks_error_handling.rst), devel.
Confirmed:
- Lists of failed_when and changed_when conditions are joined with an implicit and; explicit or in one string for any-of; changed_when decides change reporting and handlers; the _task variable.
- Removed the evaluation-order list, command-not-found rc, and check-mode claims.

Method: documentation only; no commands were run.
