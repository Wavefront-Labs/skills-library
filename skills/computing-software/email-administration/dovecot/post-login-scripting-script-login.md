---
id: computing-software.email-administration.dovecot.post-login-scripting-script-login
name: post-login-scripting-script-login
category: computing-software
field: email-administration
product: dovecot
tags: [post-login, script-login, userdb-keys, imap-alert, acl-groups, rawlog]
level: advanced
status: docs-checked
description: "Run a script after authentication but before the session starts: environment, changing userdb fields, alerts, ACL groups and denying logins."
sources:
  - https://doc.dovecot.org/main/core/config/post_login_scripting.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
To run something after authentication but before the IMAP or POP3 session starts, point the imap or pop3 executable at the `script-login` service in the service block. Several scripts can be listed, such as `script-login rawlog /usr/local/bin/postlogin.sh /usr/local/bin/postlogin2.sh`, and they run in order.

Facts to remember:
- The script runs with the privileges of the user setting of the service (root by default). Change that if it must read user mail.
- Post-login scripts cannot run in a proxy passdb, because proxied logins are not logging into the local Dovecot.
- Standard input and output are redirected to the client's socket, so writing to stdout sends data to the client. Standard error goes to Dovecot's error log.
- Userdb fields arrive as environment variables with uppercased keys (a `home` field becomes `HOME`). To add or change fields, set them in the environment and name them in `USERDB_KEYS`. This can change any Dovecot setting, such as the mail location.

Most such tasks are now easier in pure configuration using the Lua authentication database.

Recipes from the page:
- Alert the client by printing `* OK [ALERT] ...` with CRLF line endings. Not all clients show alerts, and some break with bare LF.
- Use UNIX groups for ACLs by building `ACL_GROUPS` from `groups $USER`.
- Deny a connection after successful login by testing `$USER` or `$IP` in the script, printing a `* NO [ALERT]` message and exiting without running `exec "$@"`.

## Checked

2026-11-03. Confirmed on the Post-login Scripting page: script-login in the imap/pop3 service, multiple scripts run in order, runs with the service user (root by default), no use in proxy passdb, stdin/stdout on the client socket and stderr to the error log, uppercased userdb fields as environment variables, USERDB_KEYS, the Lua authentication database tip, the CRLF alert recipe, ACL_GROUPS from groups and the deny-by-USER/IP recipe. Fixed: the deny recipe prints a NO [ALERT] and stops without exec, rather than "exiting with an error".

Method: documentation only; no commands were run.
