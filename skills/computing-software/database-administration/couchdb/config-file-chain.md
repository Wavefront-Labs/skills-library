---
id: computing-software.database-administration.couchdb.config-file-chain
name: config-file-chain
category: computing-software
field: database-administration
product: couchdb
tags: [configuration, default-ini, local-ini, couch-ini, vm-args]
level: practitioner
status: docs-checked
description: "The CouchDB configuration file load order, where to make local changes, and how -couch_ini, COUCHDB_ARGS_FILE and COUCHDB_SYSCONFIG_FILE override it."
sources:
  - https://raw.githubusercontent.com/apache/couchdb/main/src/docs/src/config/intro.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
CouchDB reads, in order, with later settings overriding earlier ones:

1. `etc/default.ini`
2. `etc/default.d/*.ini`
3. `etc/local.ini`
4. `etc/local.d/*.ini`

Files in `*.d/` directories load sorted by name (`00-shared.ini` before `10-server-specific.ini`). Paths are relative to the install directory (`/opt/couchdb` recommended on UNIX-like systems).

`default.ini` may be overwritten on upgrade or reinstall, so put local changes in `local.ini` or `local.d`.

**Changing the chain:**

```
export ERL_FLAGS="-couch_ini /path/to/my/default.ini /path/to/my/local.ini"
```

or put `-couch_ini ..` in `etc/vm.args`. The environment variable (or command-line flag) overrides `vm.args`, and both completely stop CouchDB searching the default locations. Use only when necessary and track changes to `default.ini`.

**Other files:**

```
export COUCHDB_ARGS_FILE="/path/to/my/vm.args"
export COUCHDB_SYSCONFIG_FILE="/path/to/my/sys.config"
```

## Checked

2026-11-04. Confirmed against the CouchDB docs page config/intro (Configuration files): load order, name sorting of *.d files, the default.ini upgrade warning, -couch_ini via ERL_FLAGS or vm.args, precedence of the environment variable, COUCHDB_ARGS_FILE and COUCHDB_SYSCONFIG_FILE. Nothing removed.

Method: documentation only; no commands were run.
