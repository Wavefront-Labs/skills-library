---
id: computing-software.systems-network-administration.netbox.remote-authentication-settings
name: remote-authentication-settings
category: computing-software
field: systems-network-administration
product: netbox
tags: [remote-auth, remote-user-header, group-sync]
level: advanced
status: docs-checked
description: "Trust a reverse proxy header for login and sync groups."
sources: ["https://netboxlabs.com/docs/netbox/configuration/remote-authentication/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Remote authentication

Goal: let a reverse proxy authenticate users.

`REMOTE_AUTH_ENABLED` (default False) must be True for the rest to apply. Local authentication remains available alongside it.

**Settings and defaults**

- `REMOTE_AUTH_BACKEND`: `'netbox.authentication.RemoteUserBackend'`; built-in alternative `netbox.authentication.LDAPBackend`.
- `REMOTE_AUTH_HEADER`: `'HTTP_REMOTE_USER'`. For header `X-Remote-User`, set `HTTP_X_REMOTE_USER`.
- `REMOTE_AUTH_AUTO_CREATE_USER`: False; create local accounts for remote users.
- `REMOTE_AUTH_DEFAULT_GROUPS`: `[]`; `REMOTE_AUTH_DEFAULT_PERMISSIONS`: `{}`.
- Group sync: `REMOTE_AUTH_GROUP_SYNC_ENABLED` (False), `REMOTE_AUTH_GROUP_HEADER` (`'HTTP_REMOTE_USER_GROUP'`), `REMOTE_AUTH_GROUP_SEPARATOR` (`|`), `REMOTE_AUTH_AUTO_CREATE_GROUPS` (False). The separator must match what your proxy sends.

**Header compatibility.** Some WSGI servers drop headers containing unsupported characters. gunicorn v22.0 and later silently drops headers with underscores; this can be changed with gunicorn's `header_map` setting.


Remote user authentication infers identity from an HTTP header set by the reverse proxy, such as nginx or Apache. `REMOTE_AUTH_DEFAULT_PERMISSIONS` maps permission names to attribute dictionaries, or `None` to allow all objects. Group names arrive in the group header and are split on the separator.

**Checklist**

1. Enable flag set.
2. Header name uses the `HTTP_` form.
3. WSGI server not dropping headers.

## Checked

2026-11-03: confirmed against the cited NetBox documentation: Remote authentication page: REMOTE_AUTH_* parameter names and defaults, group sync parameters, and the gunicorn 22.0 underscore-header drop with header_map. Removed: Nothing.

Method: documentation only; no commands were run.
