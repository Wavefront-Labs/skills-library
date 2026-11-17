---
id: computing-software.networking-hardware-and-wireless.squid.group-based-access
name: group-based-access
category: computing-software
field: networking-hardware-and-wireless
product: squid
tags: [networking-hardware-and-wireless, squid, groups, external-acl, winbind, authorization]
level: practitioner
status: docs-checked
description: "Restrict access by group membership by combining per-user authentication with an external_acl_type group helper."
sources:
  - https://wiki.squid-cache.org/ConfigExamples/Authenticate/Groups
  - https://www.squid-cache.org/Doc/config/external_acl_type/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Group-based access
Prerequisite: working per-user authentication. The example uses a winbind group helper:
```
external_acl_type testForGroup %LOGIN /usr/local/squid/libexec/ext_wbinfo_group_acl.pl
acl inGroupX external testForGroup someGroupNameX
http_access allow inGroupX
```
`testForGroup` passes the authenticated name (`%LOGIN`) to a script that checks membership; `inGroupX` matches users in `someGroupNameX`. Replace the group name and helper path for your install.

## Checked

2026-11-04. Read the Authenticate/Groups wiki page and confirmed the external_acl_type, acl and http_access lines and the per-user authentication prerequisite. Nothing was removed.

Method: documentation only; no commands were run.
