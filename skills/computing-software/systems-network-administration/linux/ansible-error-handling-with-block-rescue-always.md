---
id: computing-software.systems-network-administration.linux.ansible-error-handling-with-block-rescue-always
name: ansible-error-handling-with-block-rescue-always
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, block-rescue, ansible-block, rescue, always, ignore-errors, failed-when]
level: practitioner
status: docs-checked
description: "Handle Ansible failures on Linux hosts with block, rescue and always, failed_when and any_errors_fatal."
sources:
  - https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_blocks.html
  - https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_error_handling.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Error handling with block/rescue/always

## Shape
```yaml
- name: Upgrade app with rollback
  hosts: web
  serial: 1
  tasks:
    - name: Upgrade and verify
      block:
        - name: Take node out of the load balancer
          ansible.builtin.command: /usr/local/bin/lb-drain {{ inventory_hostname }}
          delegate_to: localhost
        - name: Install new version
          ansible.builtin.command: /usr/local/bin/install-app {{ app_version }}
        - name: Health check
          ansible.builtin.command: /usr/local/bin/app-health-check
      rescue:
        - name: Report what failed
          ansible.builtin.debug:
            msg: "{{ ansible_failed_task.name }} failed: {{ ansible_failed_result.msg | default('') }}"
        - name: Roll back
          ansible.builtin.command: /usr/local/bin/install-app {{ previous_version }}
        - name: Still fail the host so the run is red
          ansible.builtin.fail: { msg: "Upgrade rolled back on {{ inventory_hostname }}" }
      always:
        - name: Return node to the load balancer
          ansible.builtin.command: /usr/local/bin/lb-enable {{ inventory_hostname }}
          delegate_to: localhost
```
The commands are placeholders for your own scripts or modules.

Semantics:
- `rescue` runs only after a task in `block` returns a failed state. If the rescue tasks succeed, Ansible reverts the failed status of the original task and continues the play as if it had succeeded; the rescued failure does not trigger `max_fail_percentage` or `any_errors_fatal`, but Ansible still reports a failure in the playbook statistics. Add an explicit `fail` in `rescue`, as above, if the host should still end the run as failed.
- `always` runs regardless of the results of `block` and `rescue`, including after a failure inside `rescue`.
- `ansible_failed_task` (for example `ansible_failed_task.name`) and `ansible_failed_result` are available inside `rescue`. In ansible-core 2.14 or later both propagate from an inner block to an outer `rescue`.
- Errors caused by invalid task definitions and unreachable hosts do not trigger `rescue` or `always`.
- Directives set on a block, such as `when` and `become`, are inherited by every task inside it (loops excepted).

## Defining failure precisely
```yaml
- name: Check config
  ansible.builtin.command: nginx -t
  register: r
  changed_when: false
  failed_when: r.rc != 0 or 'warn' in r.stderr
```
`ignore_errors: true` only works when the task can run and returns failed; it does not cover undefined variables, connection failures, missing packages or syntax errors. Prefer `failed_when` with an exact condition. Use `ignore_unreachable: true` (Ansible 2.7 and later) to continue past an unreachable host, and `meta: clear_host_errors` to reactivate hosts marked unreachable.

Lists of several `failed_when` or `changed_when` conditions are joined with an implicit `and`; to fail when any one is true, write one string with `or`.

## Stopping the fleet
- `any_errors_fatal: true` (play or block level): when a task errors, Ansible finishes that task on all hosts in the current batch, then stops the play on all hosts (database schema changes).
- `max_fail_percentage: 20` with `serial` applies per batch and aborts the play when the percentage is exceeded, not merely equalled.
- Handlers: if a later task fails, notified handlers do not run on that host by default. Set `force_handlers: True` (play), `--force-handlers`, or `force_handlers = True` in ansible.cfg to run them; an unreachable host can still prevent it. Use `meta: flush_handlers` in a rescue section to run pending handlers after an error.

## Verify
- [ ] Force a failure (wrong version): rescue rolls back, always re-enables the node, the play ends failed for that host only.
- [ ] No bare `ignore_errors` remains where `failed_when` would be exact.

## Checked

Confirmed against the Ansible Blocks and Error handling in playbooks pages, both read in full: rescue and always semantics, failed-status reversal and statistics, unreachable and invalid-definition exclusions, `ansible_failed_task` and `ansible_failed_result`, `ignore_errors`, `ignore_unreachable`, `failed_when` and `changed_when` joining, `any_errors_fatal`, `max_fail_percentage` per batch, handler behaviour. Replaced the example's dnf, uri and systemd module parameters with placeholder commands because those modules are not covered by the sources. Removed the claims that syntax and templating errors get rescued (the page says the opposite), that `ignore_errors` logs red, `tags` inheritance and the ansible-lint check.

Method: docs-checked 2026-11-09 against https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_blocks.html and https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_error_handling.html
