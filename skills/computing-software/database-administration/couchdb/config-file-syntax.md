---
id: computing-software.database-administration.couchdb.config-file-syntax
name: config-file-syntax
category: computing-software
field: database-administration
product: couchdb
tags: [configuration, ini-syntax, parameter-types, comments, jwt-keys]
level: intro
status: docs-checked
description: "CouchDB ini syntax rules: sections, parameters, comments, the five value types, equals signs in names since 3.3, and restart requirement."
sources:
  - https://raw.githubusercontent.com/apache/couchdb/main/src/docs/src/config/intro.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```ini
; This is a comment
[section]
param = value ; inline comments are allowed
```

- A line is a section header, a `name = value` parameter, an empty line, or a comment. `;` starts a comment; everything after it is ignored.
- Whitespace around `=` is optional.
- Parameter names are case-sensitive.
- Value types: boolean (`true` or `false`), integer, string, tuple and proplist. Tuple and proplist values follow Erlang style and naming.
- A section groups parameters for a subsystem; for example `httpd` also holds parameters that interact with the HTTP server.
- Since 3.3, `=` is allowed inside parameter names, only when the separator is ` = ` with at least one space on each side. This helps `[jwt_keys]`, where base64 keys can contain `=`.
- Since 3.3, the undocumented multi-line value ability was removed.

Restart CouchDB after editing a configuration file to apply changes.

## Checked

2026-11-04. Confirmed against the CouchDB config/intro page: comment syntax, line kinds, case-sensitive names, five value types, 3.3 changes for = in names and multi-line values, restart after editing. Nothing removed.

Method: documentation only; no commands were run.
