---
id: computing-software.systems-network-administration.netbox.default-permissions-exempt-view
name: default-permissions-exempt-view
category: computing-software
field: systems-network-administration
product: netbox
tags: [default-permissions, exempt-view-permissions, object-permissions]
level: advanced
status: docs-checked
description: "Use DEFAULT_PERMISSIONS and EXEMPT_VIEW_PERMISSIONS and know their overwrite behaviour."
sources: ["https://netboxlabs.com/docs/netbox/configuration/security/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Default and exempt permissions

Goal: give every user baseline access without database permissions.

**DEFAULT_PERMISSIONS** applies object permissions to any authenticated user regardless of the database. Default value lets users manage their own tokens:
```
{
    'users.view_token': ({'user': '$user'},),
    'users.add_token': ({'user': '$user'},),
    'users.change_token': ({'user': '$user'},),
    'users.delete_token': ({'user': '$user'},),
}
```
Each value is a tuple of constraint dictionaries. Example allowing every user to create device roles beginning with "temp":
```
DEFAULT_PERMISSIONS = {
    'dcim.add_devicerole': ({'name__startswith': 'temp'},)
}
```
A custom value overwrites the default mapping, so reproduce the token entries if you still want them.

**EXEMPT_VIEW_PERMISSIONS** lists models (`<app>.<model>`) viewable by all users, authenticated or anonymous:
```
EXEMPT_VIEW_PERMISSIONS = ['dcim.site', 'dcim.region', 'ipam.prefix']
```
`['*']` exempts all models, but not certain sensitive ones such as user permissions, which must be listed individually. The value must be an iterable.

**Checklist**

1. Preserve token entries when overriding.
2. Avoid `*` unless intended.
3. Remember exempt models are anonymous-visible.

## Checked

Method: docs-checked 2026-11-09 against https://netboxlabs.com/docs/netbox/configuration/security/ (downloaded; searched DEFAULT_PERMISSIONS and EXEMPT_VIEW_PERMISSIONS passages: token defaults, temp example, overwrite warning, wildcard caveat, iterable requirement, authenticated and anonymous wording).
