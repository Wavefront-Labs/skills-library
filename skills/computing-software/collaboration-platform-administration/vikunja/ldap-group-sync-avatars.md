---
id: computing-software.collaboration-platform-administration.vikunja.ldap-group-sync-avatars
name: ldap-group-sync-avatars
category: computing-software
field: collaboration-platform-administration
product: vikunja
tags: [vikunja, groupsyncfilter, ldap-teams, avatarsyncattribute, immutable-ldap-id, ad-nested-groups]
level: advanced
status: docs-checked
description: "Sync LDAP groups into Vikunja teams and avatars from a directory attribute: filter placeholders, Active Directory nesting, service-account rebind and the immutable id setting."
sources:
  - https://raw.githubusercontent.com/go-vikunja/website/main/src/content/docs/setup/ldap.mdx
  - https://raw.githubusercontent.com/go-vikunja/vikunja/main/config-raw.json
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Group sync: set `groupsyncenabled: true`. At login Vikunja searches groups with `groupsyncfilter`, creates matching teams if missing and adds the user. Default filter: `(&(objectclass=*)(|(objectclass=group)(objectclass=groupOfNames)))`.

Per the config reference:
- The filter may contain `{userdn}` and `{username}` (escaped). With a placeholder, every matching group is a membership and `attribute.memberid` is ignored; login fails if the value is empty. OpenLDAP: `(&(objectclass=groupOfNames)(member={userdn}))`. Active Directory with nested groups: `(&(objectClass=group)(member:1.2.840.113556.1.4.1941:={userdn}))`.
- Without a placeholder Vikunja fetches all groups and checks `attribute.memberid` (default `member`), which is slow on large directories and misses AD groups with more than 1500 members.
- `groupsyncuseserviceaccount: true` re-binds as the service account before the group search, for users who cannot enumerate groups.

Avatars: `avatarsyncattribute` names an attribute holding raw image bytes (for example `jpegPhoto`); it is used as the avatar at login.

`attribute.id`: an immutable attribute (`objectGUID` for AD, `entryUUID` for OpenLDAP) so renames keep accounts, teams and shares. Migration happens gradually at next login and is one-way. Users must not be able to edit their own value of `attribute.username` while it is set.

## Checked

2026-11-04: checked against the LDAP page (group and avatar sections) and config-raw.json (groupsyncfilter, groupsyncuseserviceaccount, avatarsyncattribute, attribute.memberid, attribute.id).

Method: documentation only; no commands were run.
