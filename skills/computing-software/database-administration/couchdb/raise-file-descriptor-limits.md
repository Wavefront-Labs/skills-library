---
id: computing-software.database-administration.couchdb.raise-file-descriptor-limits
name: raise-file-descriptor-limits
category: computing-software
field: database-administration
product: couchdb
tags: [ulimit, file-descriptors, systemd, max-dbs-open, vm-args]
level: advanced
status: docs-checked
description: "Raise CouchDB resource limits: max_dbs_open, the Erlang +Q port limit, and open file descriptors via systemd LimitNOFILE or PAM limits."
sources:
  - https://raw.githubusercontent.com/apache/couchdb/main/src/docs/src/maintenance/performance.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Many databases or views can quickly exhaust OS defaults (often 1024 or 4096).

- `[couchdb] max_dbs_open` caps databases open at once (the page shows 100). Raise it where many databases replicate continuously.
- Erlang allows at most 65536 connections by default. Add `+Q 102400` to `etc/vm.args` to raise it. `ERL_MAX_PORTS` is ignored.
- Windows: Erlang will not go past 8192 descriptors. macOS may be as low as 1024.

**systemd**: run `systemctl edit couchdb` and add:

```
[Service]
LimitNOFILE=65536
```

Above 65536 you must also add `+Q` in `vm.args`.

**PAM, not systemd**: create `/etc/security/limits.d/100-couchdb.conf` with `couchdb hard nofile 65536` and `couchdb soft nofile 65536`. With the Debian/Ubuntu sysvinit script also raise the limits for `root`, and ensure `session required pam_limits.so` is in `/etc/pam.d/common-session` and `common-session-noninteractive`.

**No PAM**: `ulimit -n 65536` in a launch script.

## Checked

2026-11-04. Confirmed against the CouchDB maintenance/performance page (System Resource Limits): max_dbs_open, the 65536 Erlang default and +Q 102400, Windows 8192 and macOS 1024 notes, systemctl edit with LimitNOFILE, the limits.d file, root and pam_limits lines, ulimit -n, ERL_MAX_PORTS ignored. Nothing removed.

Method: documentation only; no commands were run.
