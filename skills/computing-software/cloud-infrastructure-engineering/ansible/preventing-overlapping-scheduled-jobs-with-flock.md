---
id: computing-software.cloud-infrastructure-engineering.ansible.preventing-overlapping-scheduled-jobs-with-flock
name: preventing-overlapping-scheduled-jobs-with-flock
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, cron, flock, job-locking, scheduled-tasks, systemd-timers, overlap-prevention]
level: practitioner
status: docs-checked
description: "Deploy cron jobs with Ansible that cannot overlap using flock wrappers: nonblocking versus waiting locks, conflict exit codes and where the lock file lives."
sources: ["https://man7.org/linux/man-pages/man1/flock.1.html", "https://docs.ansible.com/ansible/latest/collections/ansible/builtin/cron_module.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Preventing overlapping scheduled jobs with flock

Goal: a job scheduled every N minutes never runs twice at once on the same host, even when a run
takes longer than N.

## cron + flock
```yaml
- name: Report export every 5 minutes, never overlapping
  ansible.builtin.cron:
    name: report-export                 # keep the name stable across runs
    minute: "*/5"
    user: app
    job: "/usr/bin/flock -n -E 0 /run/lock/report-export.lock /opt/app/bin/export.sh >> /var/log/app/export.log 2>&1"
```
- `-n` (`--nonblocking`) fails rather than waits if the lock cannot be acquired immediately. By default flock waits until the lock is available.
- `-w SECONDS` (`--timeout`) fails if the lock is not acquired within that time; `-w 0` is treated as `--nonblock`.
- `-E NUMBER` (`--conflict-exit-code`) sets the exit status used when `-n` hits a conflicting lock or `-w` times out; the default is 1 and the range is 0-255. `-E 0` makes a deliberate skip exit 0 so monitoring is not paged; drop it if skips should alert.
- A lock is dropped automatically when the file is closed, so a crashed job does not leave a lock that needs cleaning up.
- flock creates the lock file if it does not exist, subject to permissions: the lock path must be writable by the cron user.

Inside a script you control, lock on a file descriptor (the third form of flock takes an open file by descriptor number):
```bash
exec 9>/run/lock/report-export.lock
flock -n 9 || { echo "already running"; exit 0; }
```

## Across hosts
flock manages locks on a file, so it protects one host. For "only one host in the cluster runs it", schedule the job on one host only, or use a lock in a shared service. The man page notes that some filesystems (for example NFS and CIFS) have limited locking support, so keep the lock file on a local path.

## Gotchas
- Two cron entries with different `name:` for the same job (renamed in code) means two schedulers; remove the old one by name.
- Waiting (`-w`) lets runs queue behind a slow job; `-n` skips instead.

## Verify
- [ ] While the job runs, a second `flock -n <lockfile> true` exits with the conflict exit code (1 unless `-E` is given).
- [ ] The log shows no interleaved runs.

## Checked
2026-11-01. Confirmed on the flock(1) man page (`-n`, `-w`, `-E` and its default and range, wait-by-default, lock created if missing, dropped on close, descriptor form, NFS/CIFS limitation) and the ansible.builtin.cron module page (`name`, `minute`, `user`, `job`). Removed (not on those pages): the systemd timer section and its no-overlap claim, `timeout` wrapper advice, `/run/lock` permission claims, the NFSv4 claim, and the `systemctl list-timers` check.
Method: documentation only; no commands were run.
