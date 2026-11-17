---
id: computing-software.database-administration.couchdb.require-valid-user
name: require-valid-user
category: computing-software
field: database-administration
product: couchdb
tags: [authentication, require-valid-user, anonymous-access, up-endpoint, chttpd]
level: intro
status: docs-checked
description: "Block anonymous CouchDB access with chttpd require_valid_user, or require_valid_user_except_for_up to leave /_up open."
sources:
  - https://raw.githubusercontent.com/apache/couchdb/main/src/docs/src/config/auth.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Two settings in `[chttpd]` force authentication, both defaulting to `false`:

```ini
[chttpd]
require_valid_user = false
require_valid_user_except_for_up = false
```

- `require_valid_user = true`: no anonymous requests at all; everyone must authenticate. (Moved in 3.2 from `[couch_httpd_auth]` to `[chttpd]`.)
- `require_valid_user_except_for_up = true`: no anonymous requests except to `/_up`; everything else needs credentials.

## Checked

2026-11-04. Confirmed against the CouchDB config/auth page (chttpd section): require_valid_user and require_valid_user_except_for_up behaviour, example values false, moved in 3.2. Removed the load balancer health-check gloss, which the page does not state.

Method: documentation only; no commands were run.
