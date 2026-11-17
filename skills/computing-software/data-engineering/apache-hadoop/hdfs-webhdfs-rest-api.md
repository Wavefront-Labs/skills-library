---
id: computing-software.data-engineering.apache-hadoop.hdfs-webhdfs-rest-api
name: hdfs-webhdfs-rest-api
category: computing-software
field: data-engineering
product: apache-hadoop
tags: [data-engineering, apache-hadoop, hdfs, webhdfs, rest, http, curl]
level: practitioner
status: docs-checked
description: "WebHDFS REST API: URL format, auth modes, the two-step 307 redirect for CREATE and APPEND, operation list, and permission defaults (644 files, no umask)."
sources:
  - https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/WebHDFS.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WebHDFS

URL: `http://<HOST>:<HTTP_PORT>/webhdfs/v1/<PATH>?op=...`. With SSL the scheme is `swebhdfs://`.

Auth:
- Security off: `user.name=<USER>` query parameter.
- Security on: `delegation=<TOKEN>`, or `curl --negotiate -u :` for Kerberos SPNEGO.
- `dfs.web.authentication.kerberos.principal` must start with `HTTP/`; `dfs.web.authentication.kerberos.keytab` holds its keytab.

Operations (a subset of those the page lists, grouped by HTTP verb): `OPEN`, `GETFILESTATUS`, `LISTSTATUS` (GET); `LISTSTATUS_BATCH` (GET, `startAfter`, batch size from `dfs.ls.limit`); `CREATE`, `MKDIRS`, `RENAME` (PUT, with `destination`); `APPEND` (POST); `DELETE` (DELETE, `recursive=true|false`).

CREATE and APPEND take two steps:

```
curl -i -X PUT "http://<HOST>:<PORT>/webhdfs/v1/<PATH>?op=CREATE"
# NameNode replies 307 with a DataNode Location
curl -i -X PUT -T <LOCAL_FILE> "<Location URL>"
```

Step 2 returns 201 Created (CREATE) or 200 OK (APPEND; the APPEND step 2 is a POST). With `noredirect=true` the NameNode answers 200 OK with the location in the response instead of a 307. The two steps stop clients sending data before the redirect; the page describes this as a workaround for `Expect: 100-continue` bugs in some HTTP libraries.

Files get 644 and directories 755 by default; no server-side umask is applied, so `fs.permissions.umask-mode` has no effect.

Timeouts: `dfs.webhdfs.socket.connect-timeout` and `dfs.webhdfs.socket.read-timeout`, 60s each. Errors: `IllegalArgumentException` 400, `SecurityException` 401, `IOException` 403, `FileNotFoundException` 404, `RuntimeException` 500.

## Checked
Confirmed 2026-11-08 against the Apache Hadoop WebHDFS REST API page (fetched copy labelled 3.3.5): URL and `swebhdfs://` forms, the three auth modes, the Kerberos principal and keytab properties, the operation list by verb, the 307 two-step CREATE/APPEND flow and `noredirect`, 644/755 defaults without server-side umask, `LISTSTATUS_BATCH` with `startAfter` and `dfs.ls.limit`, the 60s socket timeouts and the error-code table. Reworded the redirect rationale and noredirect behaviour to what the page says.
Method: docs-only read of cited pages, 2026-11-08


Verify: `curl -i "http://<HOST>:<PORT>/webhdfs/v1/?op=LISTSTATUS"` returns 200 with JSON.
