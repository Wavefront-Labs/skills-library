---
id: computing-software.collaboration-platform-administration.nextcloud.ldap-users-tab-filters
name: ldap-users-tab-filters
category: computing-software
field: collaboration-platform-administration
product: nextcloud
tags: [ldap, user-filter, object-classes, member-of-overlay, raw-ldap-filter]
level: practitioner
status: draft
description: "Control which LDAP users Nextcloud lists, using object classes, group membership via memberOf, or a raw LDAP filter, and know how hidden users arise."
sources:
  - https://docs.nextcloud.com/server/latest/admin_manual/configuration_user/user_auth_ldap.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: list only the right directory users in Nextcloud.

The Users tab controls which LDAP users are listed as Nextcloud users. Which LDAP users may log in is controlled separately on the Login Attributes tab. Users who have access but are not listed are hidden users.

Form fields:
- Only those object classes: Nextcloud finds the object classes typical for user objects and selects the one returning the most users. You can select several.
- Only from those groups: restricts the listing to members of chosen groups. This requires the LDAP server to support the `member-of-overlay` in filters. If it does not, the field is disabled and you should contact your LDAP administrator. Default is no selection.
- x users found: an approximate count that updates as you change the filter. Use it to check your filter before saving.

Raw filter. Click *Edit LDAP Query* to toggle to a raw LDAP filter, bypassing the form. Example:

```
(&(objectClass=inetOrgPerson)(memberOf=cn=nextcloudusers,ou=groups,dc=example,dc=com))
```

Workflow:
1. Start with the form and watch the user count.
2. Switch to a raw filter only when the form cannot express your rule.
3. Check that the count matches the number of people you expect.
4. Then tune the Login Attributes tab for who may sign in.

A count of zero or far too large usually means the Base DN on the Server tab or the object class is wrong (see ldap-backend-capabilities-and-server-tab).

Check: the user count matches the directory group size you intended.
