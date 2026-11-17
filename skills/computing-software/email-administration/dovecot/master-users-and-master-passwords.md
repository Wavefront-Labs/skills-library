---
id: computing-software.email-administration.dovecot.master-users-and-master-passwords
name: master-users-and-master-passwords
category: computing-software
field: email-administration
product: dovecot
tags: [master-users, master-passdb, result-success-continue, auth-master-user-separator, login-as-other-user, master-password]
level: advanced
status: docs-checked
description: "Let master users log in as other users with a master passdb, result_success=continue, the separator format and ACL consequences."
sources:
  - https://doc.dovecot.org/main/core/config/auth/master_users.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Master users can log in as other users, and a master password can open any account. There are two ways to log in as someone else: give the target in the SASL authorization ID field, or send both names in one username using `auth_master_user_separator`.

Configure a new passdb with `master=yes`. Master accounts cannot log in as themselves, so they need not exist in the userdb. Add `result_success=continue` where possible. Dovecot then checks that the login user exists before allowing the master login. Without it, a nonexistent target can produce an internal login error or even create a new user. It does not work with PAM, or with LDAP unless `passdb_ldap_bind = yes`, because both need the user's own password.

To let a master user also log in as themselves, add them to the normal passdb, or list the master passdb twice, with and without `master=yes`. Separate locations let the master user hold a different password for each role, which avoids accidentally acting as someone else. Keep master users few and single-purpose, for example a spam account that trains filters from users' spam folders.

If the ACL plugin is on, a master user is still subject to ACLs and by default sees no mailboxes. Options:
- add a global ACL for the master user;
- set `acl_user = %{user}` to keep `%{master_user}` available;
- return `userdb_fields { master_user=%{user} }` to hide the master login.

The master passdb can be a passwd-file (`passwd_file_path`, with `master = yes` and `result_success = continue`) or an SQL query such as `SELECT password FROM users WHERE userid = '%{user}' and master_user = true`. With `auth_master_user_separator = *`, a test login is `1 login loginuser*masteruser masterpass`. Debug with `log_debug = category=auth`.

Master passwords are different: a passdb listed first that checks one shared password (for example `passdb static { password = ... result_success = continue }`) and then continues to the primary passdb, which verifies the user exists and supplies the extra fields.

## Checked

2026-11-08. Read the Master Users/Passwords page in full. Added the passwd-file and SQL forms, test login and master-password flow.

Method: documentation only; no commands were run.
