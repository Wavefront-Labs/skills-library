---
id: computing-software.cybersecurity-defensive.keycloak.user-profile-schema-and-validation
name: user-profile-schema-and-validation
category: computing-software
field: cybersecurity-defensive
product: keycloak
tags: [cybersecurity-defensive, keycloak, user-profile, attributes, validators, unmanaged-attributes]
level: practitioner
status: docs-checked
description: "Define the realm user profile schema in Keycloak to control attribute requirements, permissions, validators and rendered forms."
sources:
  - https://github.com/keycloak/keycloak/blob/main/docs/documentation/server_admin/topics/users/user-profile.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# user profile schema and validation
The user profile is a per-realm schema for user attributes, managed in the admin console under *Realm Settings* > *User Profile* (attribute form or *JSON Editor* sub-tab). It lets administrators define the attribute schema, whether an attribute is required (for users, admins, both, or depending on requested scopes), view and edit permissions, and per-attribute validators. Registration, update profile, brokering and account console forms render dynamically from it without theme changes.

The default configuration manages `username`, `email`, `firstName`, `lastName`. `username` and `email` have special handling: you can change their settings but cannot remove them, and the realm Login settings (*Email as username*, *Edit username*) override the profile configuration.

JSON shape from the docs (abbreviated):
```
{ "unmanagedAttributePolicy": "DISABLED",
  "attributes": [ { "name": "myattribute", "displayName": "My Attribute",
   "required": { "roles": ["user","admin"], "scopes": ["foo","bar"] },
   "permissions": { "view": ["admin","user"], "edit": ["admin","user"] },
   "validations": { "length": { "max": 255 } } } ] }
```
*Who can edit* marks an attribute writable by user and/or admin; *Who can view* marks it read-only for them. Use permissions to make sensitive or system attributes admin-only or read-only.

Unmanaged attributes (not defined in the profile) are disabled by default. Set *Unmanaged Attributes* under *Realm Settings* > *General* (JSON values `DISABLED`, `ENABLED`, `ADMIN_VIEW`, `ADMIN_EDIT`): Enabled applies to all contexts; Admin can view and Admin can edit apply only to the administrative context. Unmanaged attributes have a maximum length of 2048 characters; make one managed and add a `length` validator to change that.

## Checked
2026-11-03. Confirmed against server_admin/topics/users/user-profile.adoc: menu paths, default attributes, special handling, JSON keys, unmanaged policy values and the 2048 limit. Removed: "confirm field names" hedge, the claim that making an attribute required forces update-profile, and the Verify step.
Method: documentation only; no commands were run.
