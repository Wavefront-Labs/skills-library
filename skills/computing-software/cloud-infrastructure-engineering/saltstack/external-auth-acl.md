---
id: computing-software.cloud-infrastructure-engineering.saltstack.external-auth-acl
name: external-auth-acl
category: computing-software
field: cloud-infrastructure-engineering
product: saltstack
tags: [saltstack, external-auth, eauth, acl, pam, runner, wheel, master-config]
level: advanced
status: docs-checked
description: "Define Salt external_auth ACLs in the master config: user or group (%) matching, minion targets, function patterns, @runner/@wheel/@jobs, argument limits."
sources:
  - https://raw.githubusercontent.com/saltstack/salt/master/doc/topics/eauth/index.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# external_auth ACLs

eAuth delegates authorization to an external system such as PAM or LDAP. Rules live in the master config under `external_auth`: backend, then user, then allowed minion targets with function patterns.

- Users and functions may be exact, shell globs or regexes; minion targets are compound targets.
- Append `%` to a name to apply the rule to a group.
- Runners and wheel modules need `@runner`, `@wheel` or `@jobs` entries, since they have no minions to scope; globs do not match them.
- Limit arguments with regex values for positional and keyword args. Unlisted arguments accept any value; `.*` skips one.

Use: `salt -a pam <target> <function>` (a user on the master system authenticates with `-a`).

Security note: every user with eAuth privileges can run `saltutil.findjob`, which may reveal data such as minion IDs.

## Checked

2026-11-09. Read against the eauth source (doc/topics/eauth/index.rst); matching syntax, @ entries, groups, argument rules and the findjob warning were confirmed there. Nothing removed.
Method: documentation only; no commands were run.
