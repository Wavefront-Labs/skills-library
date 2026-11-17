---
id: computing-software.cloud-infrastructure-engineering.ansible.no-log-on-tasks-and-loops
name: no-log-on-tasks-and-loops
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, no-log-secrets, no-log-task, no-log-loop, no-log, loop-control-label, secrets]
level: practitioner
status: docs-checked
description: "Apply no_log to tasks that handle secrets, prevent loop items from leaking credentials in per-item output, and keep failures debuggable with conditional no_log."
sources: ["https://docs.ansible.com/ansible/latest/reference_appendices/faq.html#how-do-i-keep-secret-data-in-my-playbook", "https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_loops.html#limiting-loop-output-with-label", "https://github.com/ansible/ansible-documentation/blob/devel/docs/docsite/rst/playbook_guide/playbooks_secret_masking.rst", "https://ansible.readthedocs.io/projects/lint/rules/no-log-password/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# no_log on tasks and loops

## What no_log does
`no_log: true` censors the task result handed to callbacks: only a few status keys such as `changed` and `failed` are kept, and a `censored` entry reads
`"the output has been hidden due to the fact that 'no_log: true' was specified for this result"`.
It can be set on a task, block or play.

```yaml
- name: Create DB user
  community.postgresql.postgresql_user:
    name: app
    password: "{{ vault_app_db_password }}"
  no_log: true
```
Modules also mark their own sensitive options (`no_log: true` in the argument spec, for example the `user` module's `password`), and those values are masked even without task-level `no_log`; **anything else** (a command's stdout echoing the secret, error messages) is not.

## Loops leak per item
Without `no_log`, each item is printed in the per-item output line, for example `ok: [h] => (item={'user': 'svc', 'password': 'S3cret'})`.
```yaml
- name: Create service users
  ansible.builtin.user:
    name: "{{ item.name }}"
    password: "{{ item.password | password_hash('sha512', item.salt) }}"
  loop: "{{ service_users }}"
  loop_control:
    label: "{{ item.name }}"     # prints only the name per item
  no_log: true                    # censors the result
```
`loop_control.label` only shortens the displayed item and, per the docs, is for readability, not for protecting sensitive data; set `no_log: true` on the task. With `no_log` the default callback prints `(censored due to no_log)` instead of the item.

## Keeping it debuggable
```yaml
  no_log: "{{ not (debug_secrets | default(false) | bool) }}"
```
Run with `-e debug_secrets=true` only in a private terminal session, never in CI/AWX.
Better: debug with a dummy secret in a test environment.

## Where no_log does not reach
- A later task that prints a registered secret (for example `debug: var=result`) is not protected by the earlier task's `no_log`; give that task `no_log: true` too, or do not print it.
- Values stored with `set_fact` are ordinary variables: mark the `set_fact` task `no_log: true` and do not cache secrets (`cacheable: true` persists facts to the fact cache).
- `no_log` does not prevent data from being shown when debugging Ansible itself with `ANSIBLE_DEBUG` (documented in the FAQ).
- Task **names** are not hidden by `no_log`.
- Since ansible-core 2.22 (devel docs), Ansible can also mask individual registered secret values (vault content, `no_log` module options, prompted passwords, the `register_secret` filter) as `$REDACTED$` without hiding the whole result.

## Gotchas
- `no_log` on a block is inherited by its tasks (and on a play by all its tasks), which makes the play hard to debug; the FAQ recommends applying it to single tasks once the playbook is finished.
- A failing `no_log` task gives no error detail; run the same task with a test secret to diagnose.
- ansible-lint `no-log-password` (opt-in via `enable_list`) flags tasks that use passwords in loops without `no_log`.

## Verify
- [ ] `grep -c 'S3cret' job.log` is 0 for a run with a known test secret at `-vv`.

## Checked
Checked 2026-10-25 against ansible-documentation devel (commit of 2026-10-21) reference_appendices/faq.rst (keep secret data), playbook_guide/playbooks_loops.rst (label note), playbooks_secret_masking.rst, the ansible-core devel `_internal/_task.py` (censored result text) and `plugins/callback/__init__.py` (item shown as censored under `no_log`), and the ansible-lint `no-log-password` rule page. Confirmed: the censored message, label not protecting secrets, module `no_log` options, `ANSIBLE_DEBUG` caveat, play-level `no_log`, opt-in lint rule, and the 2.22 masking feature. Removed unconfirmed claims about controller job events, `-vvv` fact output, connection transfer logs and `keep_remote_files`.
Method: documentation only; no commands were run.
