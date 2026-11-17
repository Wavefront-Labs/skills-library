---
id: computing-software.email-administration.mail-server-administration.master-cf-services
name: master-cf-services
category: computing-software
field: email-administration
product: mail-server-administration
tags: [master-cf-services, master-cf, postfix-services, process-limit]
level: advanced
status: docs-checked
description: "Read and edit master.cf: service columns, chroot, wakeup, process limits and per-service -o overrides."
sources:
  - https://www.postfix.org/master.5.html
  - https://www.postfix.org/postconf.1.html
  - https://www.postfix.org/postconf.5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Master cf services

**Goal:** know what each daemon line means (master(5) manual).
## Columns
`service type private unpriv chroot wakeup maxproc command`; `-` means default.
## Steps
1. List services: `postconf -Mf`.
2. Add per-service overrides with `-o name=value` lines indented under the service.
3. Limit a service: set maxproc (e.g. `smtp unix - - n - 20 smtp`); `-` means the `default_process_limit` setting (default 100).
4. Chroot is `n` by default since Postfix 3.0 (`y` before); keep it `n` when a service needs files outside the jail, such as certificates or sockets.
## Failure modes
- A chrooted smtpd cannot read host files or sockets until they are copied in or chroot is off.
- Continuation lines must begin with whitespace, otherwise they parse as new services.
## Verify
- `postfix check`, `postfix reload`, then `postconf -Mf | grep submission`.
- The mail log shows each service's `postfix/<name>` tag.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.

## Checked
Date: 2026-11-02. Documentation: Postfix source docs (vdukhovni/postfix html/ tree, same text as postfix.org): master(5), postconf(1), postconf(5).
Confirmed: the column names and `-` default, whitespace-led continuation lines, `-o name=value` overrides, `postconf -M`, chroot default `n` from 3.0, `default_process_limit` 100.
Corrected or removed: only added defaults.
Method: documentation only; no commands were run.
