---
id: computing-software.systems-network-administration.linux.at-batch-and-scheduler-access-control
name: at-batch-and-scheduler-access-control
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, at, atq, atrm, atd, batch, cron-allow, cron-deny, at-allow, at-deny, job-scheduling, one-off-jobs, lpic-1, rhcsa, sysadmin]
level: practitioner
status: docs-checked
description: "Schedule one-off jobs with at and load-gated batch (atq, atrm, atd), and control who may use cron and at through cron.allow/cron.deny and at.allow/at.deny."
sources:
  - https://manpages.debian.org/bookworm/at/at.1.en.html
  - https://manpages.debian.org/bookworm/at/atd.8.en.html
  - https://manpages.debian.org/bookworm/at/at.allow.5.en.html
  - https://github.com/cronie-crond/cronie/blob/master/man/crontab.1
  - https://www.freedesktop.org/software/systemd/man/latest/systemd-run.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# at, batch, and who may schedule jobs

**Goal:** run a command once at a set time (or when the box is idle), and restrict scheduling
to the accounts that should have it.

## 1. at
```bash
systemctl enable --now atd                       # start the at daemon
echo '/usr/local/bin/rotate-keys.sh' | at 02:30
at now + 2 hours <<'EOF'
systemctl restart app
EOF
at -f job.sh 23:00 tomorrow
at 09:00 2026-10-20
at -m teatime                                    # -m: mail the user when the job completes even if there was no output
atq                                              # list: job#, time, queue, user
at -c 7 | tail                                   # show job 7's full script (env + commands)
atrm 7
```
`at` keeps the working directory, environment and umask of the invoking shell (except some variables), unlike cron. Standard output and standard error are mailed to the user; redirect to a file if mail is not set up.

## 2. batch
`batch` runs the job when the load average drops below 1.5 or the value given to atd with `-l`; atd `-b` sets the minimum seconds between batch job starts (default 60). The default queue is `a` for `at` and `b` for `batch` (`-q`). Example: `echo 'make -j4 > build.log 2>&1' | batch`.

## 3. Access control
| File exists | Effect (cronie crontab(1); at.allow(5)) |
|---|---|
| `/etc/cron.allow` | a user must be listed to use `crontab` |
| no cron.allow, `/etc/cron.deny` | a user must not be listed |
| neither | only the superuser may use `crontab` |
`/etc/at.allow` and `/etc/at.deny` work the same way for `at`/`batch`: if at.allow exists only listed users may use at; otherwise
users not listed in at.deny may; an empty `at.deny` means every user may; with neither file only the superuser may.
The files are lists of usernames, one per line, and whitespace is not permitted.
```bash
printf 'root\nops\n' > /etc/cron.allow
```
The man pages do not say whether the superuser is exempt from the allow lists; list `root` explicitly. Whether already installed crontabs
of newly denied users keep running is not documented in the pages checked; remove them with `crontab -r -u <user>` to be sure.

## Gotchas
- `atd` must be running for queued jobs to execute; check the service.
- systemd alternative for one-offs: `systemd-run --on-calendar='2026-10-20 09:00' cmd` (a transient timer unit; systemd-run(1)).

## Verify
- [ ] `echo 'touch /tmp/at-ok' | at now + 1 minute`; file appears and `atq` empties.
- [ ] A user not in cron.allow is refused by `crontab`.

## Checked

Checked against at(1), atd(8) and at.allow(5) on manpages.debian.org (bookworm), cronie crontab(1) (cronie-crond/cronie, last push 2026-10-14) and systemd-run(1) (systemd repository).
Confirmed: `-m`, `-f`, `-q` with default queues a and b, `-c`, `atq`, `atrm`, time specs (`now + 2 hours`, `tomorrow`, `teatime`, `YYYY-MM-DD`), environment/cwd/umask capture, mail of output, batch load threshold 1.5 and atd `-l`/`-b` (60 s), at.allow/at.deny rules including the empty at.deny case, cron.allow/cron.deny rules, `systemd-run --on-calendar`.
Removed as unconfirmed: CIS benchmark advice, file mode and ownership advice, the Debian and RHEL default differences, the exact error message, the statement that denied users' crontabs still run, DST remark.

Method: documentation only; no commands were run.
