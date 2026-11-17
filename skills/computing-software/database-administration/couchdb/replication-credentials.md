---
id: computing-software.database-administration.couchdb.replication-credentials
name: replication-credentials
category: computing-software
field: database-administration
product: couchdb
tags: [replication, credentials, basic-auth, authorization-header, ibm-iam]
level: practitioner
status: docs-checked
description: "Ways to give CouchDB replication endpoints credentials: auth.basic object, URL userinfo, Authorization header, IBM IAM apikey, and their precedence."
sources:
  - https://raw.githubusercontent.com/apache/couchdb/main/src/docs/src/replication/replicator.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Three forms, chosen in this order of precedence:

1. `auth.basic` object (3.2.0): preferred, allows characters such as `@` and `:` in the username and password.

```json
{"target": {"url": "http://someurl.com/mydb",
            "auth": {"basic": {"username": "$username", "password": "$password"}}}}
```

2. URL userinfo, `"target": "http://adm:pass@localhost:5984/bar"`: compact, but cannot hold `@` or `:` in credentials, and deprecated per RFC3986. CouchDB still supports it with no removal release set.
3. An `Authorization: Basic $b64encoded_username_and_password` entry in `headers`. Base64 can wrongly suggest the credentials are hidden, encouraging leaks.

If the `auth` object has credentials they are used; otherwise URL userinfo; otherwise the header.

**IBM IAM.** With the optional `couch_replicator_auth_ibm` plugin enabled:

```json
{"auth": {"ibm": {"iam": {"api_key": "$apikey"}}}}
```

## Checked

2026-11-04. Confirmed against the CouchDB replication/replicator page (Specifying Usernames and Passwords, IBM IAM apikey): the three forms, 3.2.0, @ and : limits, RFC3986 deprecation, header downside, precedence, couch_replicator_auth_ibm. Nothing removed.

Method: documentation only; no commands were run.
