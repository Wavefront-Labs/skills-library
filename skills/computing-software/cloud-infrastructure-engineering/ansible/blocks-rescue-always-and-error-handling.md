---
id: computing-software.cloud-infrastructure-engineering.ansible.blocks-rescue-always-and-error-handling
name: blocks-rescue-always-and-error-handling
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, blocks, block, rescue, always, block-rescue-always, error-handling, failed-when, ignore-errors, ignore-unreachable, any-errors-fatal, max-fail-percentage, ansible-failed-task, ansible-failed-result, fail-module, assert-module, meta-end-host, meta-end-play, transactions, rollback]
level: practitioner
status: docs-checked
description: "Group Ansible tasks in block/rescue/always (try-catch-finally), scope when/become/tags once, roll back on failure, and pick failed_when vs ignore_errors vs any_errors_fatal vs max_fail_percentage."
sources: ["https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_blocks.html", "https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_error_handling.html", "https://docs.ansible.com/ansible/latest/collections/ansible/builtin/meta_module.html", "https://docs.ansible.com/ansible/latest/collections/ansible/builtin/assert_module.html", "https://github.com/ansible/ansible/blob/devel/lib/ansible/errors/__init__.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Blocks, rescue/always and error handling

**Goal:** failures stop the right thing (one host, one batch, or the whole run), clean-up
always runs, and partial changes are rolled back instead of left half-applied.

## 1. Block = shared directives + try/catch/finally
```yaml
- name: Deploy app release
  block:
    - ansible.builtin.unarchive:
        src: "app-{{ ver }}.tgz"
        dest: /opt/app/releases/
    - ansible.builtin.file:
        src: "/opt/app/releases/{{ ver }}"
        dest: /opt/app/current
        state: link
      notify: restart app
    - ansible.builtin.uri:
        url: "http://localhost:8080/health"
        status_code: 200
      retries: 10
      delay: 3
      register: h
      until: h.status == 200
  rescue:
    - ansible.builtin.debug:
        msg: "{{ ansible_failed_task.name }} failed: {{ ansible_failed_result.msg | default('') }}"
    - ansible.builtin.file:
        src: "/opt/app/releases/{{ prev_ver }}"
        dest: /opt/app/current
        state: link
    - ansible.builtin.fail:
        msg: "Deploy {{ ver }} rolled back"     # re-raise so the play still fails
  always:
    - ansible.builtin.file:
        path: /opt/app/deploy.lock
        state: absent
  when: deploy_enabled | bool
  become: true
  tags: [deploy]
```
- Directives on the block apply to the tasks in it (the directive does not affect the block itself).
- `rescue` runs after a task in the block returns a `failed` state. If the rescue tasks succeed,
  Ansible reverts the failed status of the original task and continues as if it had succeeded; the
  rescued task does not trigger `max_fail_percentage` or `any_errors_fatal`. Add `fail` at the end
  of `rescue` if the play should still stop.
- `always` runs regardless of the results of the block and rescue sections.
- Errors from invalid task definitions and unreachable hosts do not trigger `rescue` or `always`.
- `ansible_failed_task` and `ansible_failed_result` are available in `rescue` (added in 2.1); in
  ansible-core 2.14 and later they propagate from an inner block to an outer `rescue`.
- Handlers notified in a block do not run on failure by default; the docs show `meta: flush_handlers`
  in `rescue` to make sure they run even after an error.
- Blocks cannot be looped; wrap the block in a task file and loop `include_tasks`.

## 2. Deciding what counts as failure
| Need | Use |
|---|---|
| Non-zero rc is fine | `failed_when: r.rc not in [0, 2]` (register the result first) |
| Output decides | `failed_when: "'FAILED' in r.stderr"` |
| Several conditions | a list is joined with an implicit `and`; use one string with `or` to fail on any |
| Keep going but remember | `ignore_errors: true` + `register` + later `when: r is failed` |
| Host down is acceptable | `ignore_unreachable: true` (play or task; added in 2.7) |
| Business rule | `ansible.builtin.assert` with `that`, `fail_msg`, `quiet` |
| Stop this host, keep others | `ansible.builtin.meta: end_host` (without failing it; 2.8+) |
| Stop the whole play | `ansible.builtin.meta: end_play` (without failing the hosts) |

`ignore_errors` only works when the task runs and returns `failed`: it does not ignore undefined
variable errors, connection failures, execution issues such as missing packages, or syntax errors.
Prefer `block/rescue` or a precise `failed_when` over `ignore_errors` when later tasks depend on success.

## 3. Play-level blast radius
```yaml
- hosts: web
  serial: 10
  max_fail_percentage: 30      # abort once MORE than 30% of a batch has failed
  any_errors_fatal: true       # alternative: first failure stops all hosts after the current task
```
By default a failed host drops out and the play continues on the others. With `any_errors_fatal`,
Ansible finishes the fatal task on all hosts in the current batch and then stops the play on all
hosts; set it at play or block level and recover with `rescue`. `max_fail_percentage` applies per
batch with `serial`; the percentage must be exceeded, not equaled (for serial 4, use 49 to abort
on 2 failures).

## 4. Unreachable vs failed
An unreachable host is marked UNREACHABLE and removed from the active hosts for the run;
`meta: clear_host_errors` clears the failed state (see the meta module for exactly which hosts
it reactivates). `ansible-playbook` exit codes in the core source: 0 success, 1 generic error, 2 hosts
failed, 4 hosts unreachable (bit flags).

## Gotchas
- A `rescue` that only logs swallows the error; re-fail if the play must stop.
- Handlers: `--force-handlers`, `force_handlers: True` in a play, or `force_handlers = True` in
  ansible.cfg run notified handlers even on hosts with failed tasks (an unreachable host can still prevent it).
- Never write `{{ }}` in `failed_when`/`changed_when`: they are raw Jinja2 expressions.

## Verify
- [ ] Force a failure in a middle task and confirm `rescue` reverts, `always` cleans up, and the play ends non-zero.
- [ ] `ansible-playbook ...; echo $?` gives 0, 2 or 4 as expected.

## Checked
Checked 2026-10-23 against ansible-documentation (playbooks_blocks.rst, playbooks_error_handling.rst) and
ansible-core devel `modules/meta.py`, `modules/assert.py` and `errors/__init__.py` (`ExitCode`); devel is 2.23 dev.
Confirmed the rescue/always semantics, version notes (2.1, 2.7, 2.8, 2.14), failed_when list rule, any_errors_fatal and
max_fail_percentage behaviour, exit codes. Fixed: `always` is not skipped by a skipped block (removed unconfirmed
claim), `ignore_errors` limits, `max_fail_percentage` is strictly "more than". Removed an unconfirmed RHCE
reference, the `requiretty` example and "`block` does not catch Jinja errors at parse time".
Method: documentation only; no commands were run.
