---
id: computing-software.email-administration.mailcow.mailcow-dovecot-expunge-old-mail
name: mailcow-dovecot-expunge-old-mail
category: computing-software
field: email-administration
product: mailcow
tags: [doveadm-expunge, junk-cleanup, trash-cleanup, ofelia-scheduler, retention-cron]
level: practitioner
status: docs-checked
description: "Delete old Junk, Trash or any mail with doveadm expunge and schedule it with host cron or the Ofelia job scheduler."
sources: ["https://docs.mailcow.email/manual-guides/Dovecot/u_e-dovecot-expunge/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Expunging old mail with doveadm

Run `doveadm expunge` inside `dovecot-mailcow` (`docker compose exec dovecot-mailcow ...`). Examples from the docs:
- one user's read Junk older than 4 hours: `doveadm expunge -u 'mailbox@example.com' mailbox 'Junk' SEEN not SINCE 4h`
- all users' Junk saved more than 7 days ago: `doveadm expunge -A mailbox 'Junk' savedbefore 7d`
- all mail in all folders older than 52 weeks by internal date: `doveadm expunge -A mailbox % before 52w` (`before` uses the mail's internal date; `savedbefore` uses when it was saved here)
- unflagged mail older than two weeks in a custom subfolder of a user's inbox.
Time spans and search keys follow the doveadm-search-query manual.

Scheduling: either a script on the host that does `cd` to the mailcow directory and runs the command, called from `crontab -e` (for example `0 4 * * *`), or the Docker scheduler Ofelia. For Ofelia, add labels to `dovecot-mailcow` in `docker-compose.override.yml`: `ofelia.enabled: "true"`, `ofelia.job-exec.dovecot-expunge-junk.schedule: "0 0 4 * * *"` (Ofelia's Go cron format has a seconds field), `.command: "doveadm expunge -A mailbox 'Junk' savedbefore 2w"` and `.tty: "false"`.

## Checked

2026-11-09. Confirmed on the expunge page: the four doveadm examples, before versus savedbefore, search-query references, host cron script with crontab entry, and the Ofelia labels with the seconds-first Go cron format. No changes needed.

Method: docs-checked 2026-11-09 against the full Dovecot expunge page (u_e-dovecot-expunge.en.md in mailcow-dockerized-docs).
