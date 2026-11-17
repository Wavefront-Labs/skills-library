---
id: computing-software.cloud-infrastructure-engineering.ansible.handling-unreachable-hosts
name: handling-unreachable-hosts
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, error-handling, unreachable-hosts, clear-host-errors, retry-file, ignore-unreachable, wait-for-connection]
level: practitioner
status: docs-checked
description: "Handle unreachable hosts in Ansible: ignore_unreachable, meta clear_host_errors, wait_for_connection after reboots, and failing the play when too many hosts drop."
sources: ["https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_error_handling.html", "https://docs.ansible.com/ansible/latest/collections/ansible/builtin/meta_module.html", "https://docs.ansible.com/ansible/latest/collections/ansible/builtin/wait_for_connection_module.html", "https://docs.ansible.com/ansible/latest/inventory_guide/intro_patterns.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Handling unreachable hosts

UNREACHABLE (SSH/WinRM could not connect or the connection died) is distinct from FAILED.
`ignore_errors: true` does **not** cover it. An unreachable host is removed from the rest of the
play.

## ignore_unreachable
Task or play keyword (2.7+): the task's unreachable result is reported but the host stays active.
```yaml
- name: Try to collect logs from flaky edge devices
  ansible.builtin.fetch:
    src: /var/log/app.log
    dest: "logs/{{ inventory_hostname }}/"
  ignore_unreachable: true
```
Use it for best-effort steps only.

## Bringing hosts back: meta clear_host_errors
```yaml
- name: Reset failed/unreachable state so later steps try again
  ansible.builtin.meta: clear_host_errors
```
Clears the failed state from the play's hosts, which reactivates hosts removed as unreachable so later tasks try them again.

## Reboots and expected disconnects
Prefer `ansible.builtin.reboot` (waits for reconnect itself). For custom flows:
```yaml
- ansible.builtin.shell: sleep 2 && /sbin/shutdown -r now
  async: 1
  poll: 0
- ansible.builtin.wait_for_connection:
    delay: 20
    timeout: 600
```
Use `wait_for_connection` also as the first task on freshly provisioned hosts
(`gather_facts: false`, then `setup` after the wait).

## Stopping the run when too many drop
```yaml
- hosts: web
  max_fail_percentage: 10   # applies per batch; the percentage must be exceeded
  serial: 20
```
`any_errors_fatal: true` stops the play for all hosts after the first failure.

## Re-running only those hosts
Enable retry files (`retry_files_enabled = True`); `<playbook>.retry` lists the failed hosts from all plays and is overwritten each run; rerun with `--limit @<playbook>.retry`. Useful lists in-play:
`ansible_play_hosts` (still active) vs `ansible_play_hosts_all` (all targeted); the
difference is the failed+unreachable set.

## Diagnose
`ansible <host> -m ping -vvvv` — look for DNS, `Permission denied (publickey)`, host-key prompts,
`timeout` (raise `timeout` in `[defaults]`), or a jump host (`ansible_ssh_common_args`).
Tune `[ssh_connection] retries` for transient network loss.

## Gotchas
- Unreachable mid-task after the module started (e.g. you restarted sshd or networking) can leave work half-done; make such tasks async or reorder them last.
- `ignore_unreachable` on the play also hides real outages — scope it to tasks.
- `--force-handlers` (or `force_handlers: True`) runs handlers after a failure, but the docs note that certain errors, such as a host becoming unreachable, can still prevent a handler from running.

## Verify
- [ ] Recap distinguishes `unreachable=` from `failed=` and matches expectations.
- [ ] Retry file / `ansible_play_hosts_all | difference(ansible_play_hosts)` lists the dropped hosts.

## Checked

- Date: 2026-10-26. Documentation release: ansible-core stable-2.22 documentation and source (docs and lib/ branch stable-2.22, checked 2026-10-26; 2.21 is the latest GA release, 2.22 GA is scheduled for Nov 2026).
- Confirmed in docs/docsite/rst/playbook_guide/playbooks_error_handling.rst: ignore_unreachable added in 2.7 (task or play level), `meta: clear_host_errors` reactivates unreachable hosts, force_handlers caveat, max_fail_percentage applies per batch with serial and must be exceeded, any_errors_fatal aborts after the first failure.
- Confirmed in config/base.yml and intro_patterns.rst: retry files off by default, the .retry file lists failed hosts from all plays and is overwritten each run, `--limit @file`; in vars/manager.py: ansible_play_hosts is ansible_play_hosts_all minus removed hosts; in modules/wait_for_connection.py defaults delay 0, timeout 600; in plugins/connection/ssh.py `retries` retries only on SSH return code 255.
- Removed unconfirmed claims: recap counting of ignored unreachable results, unreachable hosts counting toward max_fail_percentage, unreachable hosts being written to retry files.

Method: documentation only; no commands were run.
