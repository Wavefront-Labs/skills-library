---
id: computing-software.systems-network-administration.apache-guacamole.user-mapping-xml
name: user-mapping-xml
category: computing-software
field: systems-network-administration
product: apache-guacamole
tags: [systems-network-administration, apache-guacamole, user-mapping-xml, file-based-authentication, authorize, connection-xml, md5, basic-auth]
level: intro
status: draft
description: "Define users and connections in Guacamole's default file-based auth, user-mapping.xml: structure, md5 encoding, DEFAULT connection, auto-reread, and common parse errors."
sources:
  - https://guacamole.apache.org/doc/gug/configuring-guacamole.html
  - https://guacamole.apache.org/doc/gug/troubleshooting.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# user-mapping.xml

File: `GUACAMOLE_HOME/user-mapping.xml` (the default authentication provider). Changes are re-read automatically; no restart.

```xml
<user-mapping>
    <authorize username="alice" password="<MD5-HASH>" encoding="md5">
        <connection name="Web server">
            <protocol>ssh</protocol>
            <param name="hostname">10.0.0.5</param>
            <param name="port">22</param>
        </connection>
    </authorize>
</user-mapping>
```
- Root `<user-mapping>`; one `<authorize>` per user.
- `password` is plaintext unless `encoding="md5"` (hash goes in the attribute). The troubleshooting page says valid encodings are `plain` and `md5` only.
- A user with a single connection may put `<protocol>`/`<param>` directly under `<authorize>`; it is named DEFAULT.
- Every `<connection>` and `<param>` needs a `name` attribute.

Errors that block all logins until fixed (servlet container log):
- `Attribute "name" required for connection tag` / `param tag`
- `Unexpected character data`: text outside a `<param>`
- `Invalid encoding type`: use `plain` or `md5`
- `User mapping could not be read`: missing or unreadable file; check the path and container permissions

Limits: no admin UI, history, sharing or balancing; use a database extension for those (apache-guacamole.database-auth-overview).

Verify: log in as the user and see the named connections.
