---
id: computing-software.email-administration.dovecot.security-hardening-checklist
name: security-hardening-checklist
category: computing-software
field: email-administration
product: dovecot
tags: [security, privilege-separation, first-valid-uid, chroot, dovecot-auth-user, dedicated-uid]
level: intro
status: docs-checked
description: "Dovecot's privilege-separated design and the extra hardening steps: per-user UIDs, separate auth user, chroots, SSL settings and UID ranges."
sources:
  - https://doc.dovecot.org/main/core/config/security.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Dovecot uses multiple processes and privilege separation so that a security hole in one part does not expose the others. Beyond defaults, the security page lists additional options:

- Allocate each user their own UID and GID, so the kernel enforces mail isolation (see the system users page).
- Use a separate `dovecot-auth` style user for the authentication process.
- Chroot the authentication and mail processes (see the chrooting page).
- Apply the TLS settings, covered under SSL configuration.
- Set `first_valid_uid`, `last_valid_uid`, `first_valid_gid` and `last_valid_gid` to contain only the range actually used by mail processes.

The security page itself is only this short list, so treat it as a checklist and follow the linked pages for details. As a sanity check after narrowing the UID range, `doveadm user` shows the uid and gid the userdb returns for a user, so you can confirm real users fall inside the allowed range.

## Checked

2026-11-08. Read the Security page in full. It is a short list; removed four unsourced bullets attributed to other pages and an unsourced claim about how mail processes treat out-of-range UIDs.

Method: documentation only; no commands were run.
