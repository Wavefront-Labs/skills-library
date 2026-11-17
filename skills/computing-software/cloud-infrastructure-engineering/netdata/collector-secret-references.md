---
id: computing-software.cloud-infrastructure-engineering.netdata.collector-secret-references
name: collector-secret-references
category: computing-software
field: cloud-infrastructure-engineering
product: netdata
tags: [netdata, secrets, env-file-cmd, urienc]
level: advanced
status: docs-checked
description: "Keep collector credentials out of plain config using Netdata secret references (env, file, cmd, store), with resolver rules, timeouts and error patterns."
sources:
  - https://raw.githubusercontent.com/netdata/netdata/master/src/collectors/SECRETS.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Syntax:
- `${env:VAR_NAME}`
- `${file:/absolute/path}`
- `${cmd:/absolute/path/to/command args}`
- `${store:<kind>:<name>:<operand>}`
- URI-encoded variants: `${env+urienc:...}`, `${file+urienc:...}`, `${cmd+urienc:...}`, `${store+urienc:...}`

```
password: "${file:/run/secrets/mysql_password}"
dsn: "postgresql://postgres:${store+urienc:vault:vault_prod:secret/data/netdata/pg#password}@db.example.com:5432/postgres"
```

Rules:
- env: must be set in the environment of the Netdata service or collector process; whitespace trimmed.
- file: absolute path, readable by the `netdata` user, 3 second timeout on Unix, contents trimmed. On Unix it reads through `nd-run` unprivileged.
- cmd: absolute path, 10 second timeout, arguments split on whitespace (no pipes, redirects or shell quoting unless you invoke a shell), stdout trimmed, stderr ignored.
- Use `+urienc` only for a single URI component such as a password.

Gotchas:
- Secrets resolve when a job starts or restarts; failure means the job does not start and an error is logged.
- `trust_discovered_targets: yes` lets discovered targets read files, run commands and fetch secrets; enable only if every target is trusted.
- There is no privilege fallback if `nd-run` fails.

Error patterns: environment variable is not set; file path must be absolute; command path must be absolute; command timed out after 10s; unknown modifier.

## Checked

2026-11-04. Confirmed against the Netdata Secrets page: the four reference forms and +urienc variants, the DSN example, env, file and cmd rules, nd-run behaviour with no privilege fallback, the single-URI-component advice, resolution at job start, trust_discovered_targets risk, and the error patterns. Added the Unix qualifier to the 3 second file timeout.

Method: documentation only; no commands were run.
