---
id: computing-software.email-administration.dovecot.doveadm-user-userdb-lookup
name: doveadm-user-userdb-lookup
category: computing-software
field: email-administration
product: dovecot
tags: [doveadm-user, userdb-lookup, auth-userdb-socket, auth-info, field-extraction]
level: practitioner
status: docs-checked
description: "Inspect what the userdb returns for a user with doveadm user, expand templates, print one field and simulate request conditions."
sources:
  - https://doc.dovecot.org/main/core/man/doveadm-user.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`doveadm user` shows userdb information for one or more users, or reports whether a user exists in the configured userdb. It is the quickest check that a new database returns the right uid, gid, home and mail location.

Behaviour from the documentation:
- `-e` with a string containing `%variables` prints the expansion for that user, and cannot combine with `-f` or `-u`.
- `-f field` prints only the named userdb field's value, and cannot combine with `-e` or `-u`.
- `-u` shows only values from the userdb. Without it, if `uid`, `gid`, `home` or `mail_path` are missing from the userdb, their defaults come from the config file.
- `-x name=value` gives auth_info conditions, the same set as `doveadm auth`: service, local and remote IPs and ports. This matters when the userdb query depends on `%{protocol}` or `%{local_ip}`, or the userdb is otherwise service-specific.
- `-a socket` selects an alternate UNIX socket; the default is `auth-userdb` in the runtime directory, which may differ if `base_dir` is overridden.

The user argument accepts `*` and `?` wildcards, for example `doveadm user '*.?oe@example.net'` lists matching users (this needs a userdb that can iterate). A userdb can also depend on the protocol, such as a passwd-file path containing `%{protocol}`, which is when `-x service=imap` matters.

Use it after changing userdb SQL or LDAP, and compare against what an actual login produces. It talks to the auth process through its userdb socket, so the Dovecot server must be running.

## Checked

2026-11-08. Read doveadm-user(1) in full plus the -x include. Content was accurate; removed an unsourced comparison with dsync and added wildcard and %{protocol} passwd-file notes.

Method: documentation only; no commands were run.
