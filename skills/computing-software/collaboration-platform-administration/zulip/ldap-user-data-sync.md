---
id: computing-software.collaboration-platform-administration.zulip.ldap-user-data-sync
name: ldap-user-data-sync
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [ldap-sync, ldap-attr-map, sync-ldap-user-data, unique-account-id]
level: advanced
status: docs-checked
description: "Synchronise LDAP or Active Directory data into Zulip with sync_ldap_user_data, AUTH_LDAP_USER_ATTR_MAP, unique_account_id, deactivation and a cron job."
sources: ["https://zulip.readthedocs.io/en/latest/production/authentication-methods.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# LDAP user data synchronisation

Fields declared in `AUTH_LDAP_USER_ATTR_MAP` in `/etc/zulip/settings.py` populate new accounts at creation. Existing users are updated by:

```
~zulip/deployments/current/manage.py sync_ldap_user_data
```

Run that from a regular cron job at whatever frequency suits your organisation. Test mappings with `manage.py query_ldap`, then restart with `scripts/restart-server`. Logs are in `/var/log/zulip/ldap.log`. Because syncing overwrites local edits, consider restricting users from changing their name or email in Zulip.

Mappable data:

- Avatars: the `avatar` key, usually from `thumbnailPhoto` or `jpegPhoto`.
- Custom profile fields: create the field first, then map e.g. `'custom_profile_field__linkedin_profile': 'linkedinProfile'`.
- Email changes (Zulip 11.0+): map `unique_account_id` to a stable identifier. Use the `dn` only if it never changes; Active Directory's `objectSid` is recommended. Binary attributes such as `objectSid` also need `LDAP_UNIQUE_ACCOUNT_ID_IS_BINARY` set.

Deactivation:

- Active Directory: uncomment `"userAccountControl": "userAccountControl"` in the map; accounts with ACCOUNTDISABLE are treated as deactivated.
- Other servers: map `deactivated` to a boolean attribute, for example `nsAccountLock` on FreeIPA.
- Disabled users cannot log in immediately because Zulip queries LDAP on every login, but full deactivation (including logging out sessions) happens at the next sync.
- Users no longer matched by `AUTH_LDAP_USER_SEARCH` are deactivated at the next sync when LDAP is the only backend, or when `LDAP_DEACTIVATE_NON_MATCHING_USERS` is True.

## Checked

Confirmed against the LDAP Synchronizing data, avatars, custom profile fields, email addresses, automatic deactivation and non-matching users sections of the authentication-methods page. Nothing removed.

Method: docs-checked 2026-11-09 against docs/production/authentication-methods.md in the zulip/zulip repository (main), the source of the cited page.
