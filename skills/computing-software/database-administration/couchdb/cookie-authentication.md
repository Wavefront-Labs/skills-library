---
id: computing-software.database-administration.couchdb.cookie-authentication
name: cookie-authentication
category: computing-software
field: database-administration
product: couchdb
tags: [security, cookie-auth, session, authsession, login]
level: practitioner
status: docs-checked
description: "Log in to CouchDB with POST /_session to get an AuthSession cookie, reuse it on later requests, and adjust the token lifetime with timeout."
sources:
  - https://raw.githubusercontent.com/apache/couchdb/main/src/docs/src/intro/security.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Cookie authentication avoids the browser's basic-auth dialog and repeated password sending. The `_session` API decodes HTML form submissions, so a plain form works. From curl, mimic one:

```
curl -vX POST $HOST/_session \
  -H 'Content-Type:application/x-www-form-urlencoded' \
  -d 'name=anna&password=secret'
```

A `200` response includes `Set-Cookie: AuthSession=...; Version=1; Path=/; HttpOnly` and `{"ok":true}`.

Use the token on later requests without credentials:

```
curl -vX PUT $HOST/mydatabase --cookie AuthSession=<token> \
  -H "X-CouchDB-WWW-Authenticate: Cookie" \
  -H "Content-Type:application/x-www-form-urlencoded"
```

By default a token is valid for 10 minutes. After that the user must authenticate again. Change the lifetime with `timeout` (seconds) in the `[chttpd_auth]` section.

## Checked

2026-11-04. Confirmed against the CouchDB intro/security page (Authentication, Cookie authentication): form-encoded POST to _session, the Set-Cookie AuthSession header, reuse with the X-CouchDB-WWW-Authenticate header, the 10 minute default and the timeout setting in seconds. Nothing removed.

Method: documentation only; no commands were run.
