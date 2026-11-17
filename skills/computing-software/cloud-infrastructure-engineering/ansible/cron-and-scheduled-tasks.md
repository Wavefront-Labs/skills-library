---
id: computing-software.cloud-infrastructure-engineering.ansible.cron-and-scheduled-tasks
name: cron-and-scheduled-tasks
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, cron, cron-module, scheduled-tasks, crontab, cron-d, at-jobs, at-module, systemd-timer, special-time, cron-env, mailto, anacron, logrotate, win-scheduled-task, job-scheduling, idempotent-cron]
level: practitioner
status: docs-checked
description: "Schedule jobs with Ansible's cron module idempotently (name as key, cron.d files, special_time, env vars), remove stale entries, use at for one-shots, and when a systemd timer is better."
sources: ["https://docs.ansible.com/ansible/latest/collections/ansible/builtin/cron_module.html", "https://docs.ansible.com/ansible/latest/collections/ansible/posix/at_module.html", "https://github.com/ansible/ansible/blob/devel/lib/ansible/modules/cron.py", "https://github.com/ansible-collections/ansible.posix/blob/main/plugins/modules/at.py", "https://github.com/systemd/systemd/blob/main/man/systemd.timer.xml", "https://github.com/ansible-collections/community.windows/blob/main/plugins/modules/win_scheduled_task.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cron and scheduled tasks

**Goal:** every scheduled job on a host is declared in Ansible, has a unique name,
runs as the right user, and disappears when removed from the data.

## 1. The cron module, done right
```yaml
- ansible.builtin.cron:
    name: "pg nightly backup"          # the idempotency key: the comment line above the entry
    user: postgres
    minute: "15"
    hour: "2"
    weekday: "*"                       # also day, month; default * for each
    job: "/usr/local/bin/pg_backup.sh >> /var/log/pg_backup.log 2>&1"
    state: present
- ansible.builtin.cron:
    name: "certbot renew"
    cron_file: certbot                 # relative paths resolve under /etc/cron.d (needs user:)
    user: root
    special_time: daily                # annually, daily, hourly, monthly, reboot, weekly, yearly
    job: "certbot renew --quiet --deploy-hook 'systemctl reload nginx'"
- ansible.builtin.cron:                # environment line in the user's crontab
    name: MAILTO
    env: true
    job: ops@example.com
    user: postgres
- ansible.builtin.cron: {name: "old report job", user: root, state: absent}
```
- `name` is how Ansible finds the entry later; change `name` and you get a duplicate plus an orphan. Keep names stable and unique per user/cron_file.
- `cron_file` uses that file instead of a user's crontab (relative paths resolve under `/etc/cron.d`); it requires `user` unless `state: absent`, is assumed to be managed exclusively by the module, and must never be `/etc/crontab`.
- `disabled: true` comments the line out instead of removing it.
- `backup: true` saves the previous crontab (`backup_file` in the result).
- Quote `*` and `*/5` values in YAML: an unquoted `*` starts a YAML alias.

## 2. Environment and paths
Cron does not run your login profile, so use absolute paths in `job`, set variables such as `PATH` via
`env: true` entries, or wrap the command in a script. The module docs require symbols such as `%` to be
escaped properly in the job line. For `env: true`, `name` is the variable name and `job` (alias `value`) its value;
`insertbefore`/`insertafter` position the variable relative to another one.

## 3. Removing what Ansible no longer declares
The module has no `exclusive` option. Either own the whole file with `template` to `/etc/cron.d/app`
(the simplest guarantee: unlisted jobs vanish), or keep a `cron_jobs` list plus a
`cron_jobs_removed` list of names with `state: absent`.

## 4. One-off jobs: `at`
```yaml
- ansible.posix.at: {command: "/usr/local/bin/rotate-keys.sh", count: 20, units: minutes}
- ansible.posix.at: {command: "/usr/local/bin/rotate-keys.sh", state: absent}   # cancel matching
```
`units` is one of minutes, hours, days, weeks; all jobs go to the `a` queue; `unique: true` skips adding a job when a matching one exists. The module requires the `at` command. Good for one-shot deferrals.

## 5. When to use a systemd timer instead
Pick a systemd timer (see the services skill) when you need `Persistent=true` catch-up for runs missed while
the machine was off or `RandomizedDelaySec=` spreading of start times; both are documented in `systemd.timer`.
Keep cron for simple jobs.

Windows: `community.windows.win_scheduled_task` with `triggers` and `actions` lists.

## Gotchas
- Two tasks with the same `name` but different `user` are separate entries (crontab per user).
- A `job` containing `"` inside YAML double quotes needs escaping; use a YAML single-quoted string or `>`-folded scalar.
- Editing a user crontab by hand later breaks nothing, but the next run will not remove hand-added lines.
- `minute: "*/5"` runs 12 times an hour; a job that takes 6 minutes overlaps; make the job itself guard against concurrent runs.

## Verify
- [ ] `crontab -l -u postgres` shows the entries preceded by `#Ansible: <name>` comment lines (not for `env: true` entries, which have no comment line).
- [ ] Second run reports `changed=0`; renaming an entry in data removes the old one (via `state: absent`) rather than leaving two.

## Checked
Checked 2026-10-26 against ansible-core devel `cron.py`, ansible.posix `at.py`, community.windows `win_scheduled_task.py`
and systemd `man/systemd.timer.xml`. Confirmed: `name` as the `#Ansible: <name>` marker and required, `cron_file` rules,
`special_time` choices, `disabled`, `env`, `backup_file`, `at` options and requirement, `Persistent=` and
`RandomizedDelaySec=`, `triggers`/`actions`. Removed unconfirmed claims: cron default PATH value, `%` newline
semantics, `flock`, journald/`list-timers` points, boot-time behaviour and log commands.
Method: documentation only; no commands were run.
