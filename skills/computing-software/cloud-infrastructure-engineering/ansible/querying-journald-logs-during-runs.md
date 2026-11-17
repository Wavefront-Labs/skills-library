---
id: computing-software.cloud-infrastructure-engineering.ansible.querying-journald-logs-during-runs
name: querying-journald-logs-during-runs
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, services-systemd, journalctl, journald, troubleshooting, failed-service]
level: practitioner
status: docs-checked
description: "Pull journald logs into a playbook run when a service fails to start: journalctl by unit and time window in a rescue block, plus fetching logs for later analysis."
sources: ["https://www.freedesktop.org/software/systemd/man/latest/journalctl.html", "https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_blocks.html", "https://docs.ansible.com/ansible/latest/collections/ansible/builtin/fetch_module.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Querying journald logs during runs

When `service: state=started` fails, Ansible only says "Unable to start service app: Job for
app.service failed". Put the reason in the job output automatically.

## Rescue semantics (Ansible docs)
- `rescue` runs only after a task returns a failed state; invalid task definitions and unreachable hosts do not trigger it. `always` runs regardless.
- If rescue succeeds, the original failure is reverted for the run, the play continues, and it does not trigger `max_fail_percentage` or `any_errors_fatal`; Ansible still reports a failure in the playbook statistics.
- `ansible_failed_task` and `ansible_failed_result` hold the failed task and its result (propagated from inner blocks to an outer rescue in ansible-core 2.14+).
- The page does not say what happens to host status if the rescue tasks themselves fail; since the example ends with `fail`, the run stops for that host either way.

```yaml
- name: Start app with diagnostics on failure
  block:
    - name: Record start time
      ansible.builtin.set_fact:
        start_ts: "{{ now(fmt='%Y-%m-%d %H:%M:%S') }}"
    - name: Start app
      ansible.builtin.systemd_service: {name: app, state: started}
  rescue:
    - name: Collect journal for the unit since the attempt
      ansible.builtin.command: >
        journalctl -u app --since "{{ start_ts }}" --no-pager -o short-iso -n 200
      register: journal
      changed_when: false
      become: true
    - name: Show it
      ansible.builtin.debug: {var: journal.stdout_lines}
    - ansible.builtin.fail:
        msg: "app failed to start; see journal above"
```
`now()` is a Jinja helper not covered by the cited pages and evaluates on the controller; if clocks differ, use a relative `--since` (the man page says relative times take a `-` or `+` prefix) or `-b` with `-n`.

## Useful journalctl options (per the man page)
| Option | Use |
|---|---|
| `-u unit` (repeatable; patterns allowed) | one or more units |
| `--since`, `--until` | absolute (`2012-10-30 18:17:16`) or relative (`-`/`+` prefix) times |
| `-p FROM..TO` | priority range, both ends inclusive; a single level includes more important ones |
| `-b`, `-b -1` | this boot / the previous boot (`-0` last boot, `-1` the one before) |
| `-o json` / `-o cat` / `-o short-iso` | one JSON object per line / message only / RFC 3339 timestamps |
| `--grep 'pattern'` | regex on MESSAGE= (added in systemd 237; case-insensitive if all lowercase) |
| `-n 200 --no-pager` | number of lines (default 10, `all` disables the limit), non-interactive |
| `_PID=1234` | FIELD=VALUE match; `-t` / `--identifier` selects by syslog identifier |

ansible.builtin has no journal query module; `command` with `changed_when: false` is the usual approach (practitioner judgement). Piping JSON through `jq` needs `shell` and `set -o pipefail`.

## Collecting logs centrally after a failed run
```yaml
- ansible.builtin.shell: journalctl -b --no-pager -o short-iso > /var/tmp/journal-{{ inventory_hostname }}.txt
  changed_when: false
- ansible.builtin.fetch:
    src: "/var/tmp/journal-{{ inventory_hostname }}.txt"
    dest: "diag/"
```
`fetch` stores files at `dest/<inventory hostname>/<remote path>` unless `flat: true`; with `flat` and several hosts sharing a filename, each overwrites the previous. `src` must be a file; `fail_on_missing` and `validate_checksum` default to true.

## Gotchas
- Root and members of `systemd-journal`, `adm` and `wheel` can read all journal files; other users see their own per-user journals. Use `become`.
- Running `fetch` with `become` also uses `slurp`, roughly doubling transfer size and risking `MemoryError` on large files; write the file with `become`, then fetch without it where possible.
- The man page ties `--user` to persistent logging via `Storage=` in journald.conf; it does not discuss data loss for volatile storage on reboot (commonly true, not verified here).
- Large `stdout_lines` in AWX job output: keep `-n` small.

## Verify
- [ ] Break the unit on purpose in a test env; the job output contains the service's error line.

## Checked
Method: 2026-11-08 docs-only read of the journalctl man page, Ansible blocks page and fetch module page; options, rescue semantics, fetch behaviour and group access confirmed. Removed or hedged: `-p err..alert` example, `--since -10min` example, SYSLOG_IDENTIFIER field match, volatile-storage claim, `community.general.syslogger` mention (unverified).
