---
id: computing-software.email-administration.dovecot.doveadm-quota-get-and-recalc
name: doveadm-quota-get-and-recalc
category: computing-software
field: email-administration
product: dovecot
tags: [doveadm-quota, quota-get, quota-recalc, quota-plugin, mail-plugins, quota-usage]
level: practitioner
status: docs-checked
description: "Display and recalculate per-user quota usage with doveadm quota get and quota recalc, and the mail_plugins requirement."
sources:
  - https://doc.dovecot.org/main/core/man/doveadm-quota.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`doveadm quota get` and `doveadm quota recalc` exist only when the global `mail_plugins` setting contains the quota plugin. Without it the commands are unavailable, which is the first thing to check when doveadm complains that the command is unknown.

Selectors follow the doveadm convention: `-A` runs for all users, `-F file` for users listed in the file, `--no-userdb-lookup` with the `USER` environment variable for one user, and `-u user` for matching users (wildcards allowed).

- `doveadm quota get -u jane` shows current usage. Storage values are reported in kilobytes. The default formatter is table with columns for quota name, type (STORAGE, MESSAGE), value, limit and percent. Select another formatter with `-f` (flow, json, pager, tab, table) for scripts.
- `doveadm quota recalc -u jane` recalculates the current quota usage. It is the natural step when stored counters may have drifted from reality, for example after a manual change in the mail directory or a restore.

The manual lists `dovecot.conf` (including the dict section), `conf.d/10-mail.conf` (mailbox locations and namespaces) and `conf.d/90-quota.conf` (quota configuration) as the relevant files.

Workflow for an over-quota complaint: run `get`, expunge as needed, run `recalc`, then `get` again.

## Checked

2026-11-08. Read doveadm-quota(1) in full plus shared includes. Fixed a wrong claim that omitting a selector runs for all users (-A is required), removed an unsourced mdbox purge step, and added the documented formatter and files.

Method: documentation only; no commands were run.
