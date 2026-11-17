---
id: computing-software.cybersecurity-defensive.authelia.file-user-database
name: file-user-database
category: computing-software
field: cybersecurity-defensive
product: authelia
tags: [authelia, file-backend, users-database, yaml, toml, json, watch, authentication-backend]
level: practitioner
status: docs-checked
description: "Run Authelia's file authentication backend with a YAML, TOML or JSON users file, hot reload via watch, and email or case-insensitive login search."
sources:
  - https://www.authelia.com/configuration/first-factor/file/
  - https://www.authelia.com/reference/guides/passwords/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The file backend stores users and password hashes in one file, which suits small installations.

```yaml
authentication_backend:
  file:
    path: '/config/users.yml'
    watch: true
    search:
      email: false
      case_insensitive: false
```

```yaml
users:
  john:
    disabled: false
    displayname: 'John Doe'
    password: '<ARGON2_HASH>'
    email: 'john@example.com'
    groups:
      - 'admins'
```

- The format follows the extension: `.toml` is TOML, `.json` is JSON, anything else (including `.yml`) is YAML. Authelia writes the file back in the same format, for example after a password reset, so never rename the extension without converting the contents.
- `watch` defaults to `false` (the example above turns it on). `watch: true` reloads the database when the file changes, so edits need no restart.
- `search.email` lets users log in with their email; emails must then be unique and no username may be an email. `search.case_insensitive` allows any case for the username and requires lowercase-only usernames. Both are experimental.
- `extra_attributes` declares custom per-user attributes with `value_type` (`string`, `integer`, `boolean`) and `multi_valued`; they are validated and usable in OpenID Connect claims.
- A published JSON schema lets editors validate the users file.

Check: edit a user with the file watcher on, then log in as that user without restarting.

## Checked

2026-11-08. Read in full: first-factor/file, reference/guides/passwords. Added that watch defaults to false (draft example enables it).

Method: documentation only; no commands were run.
