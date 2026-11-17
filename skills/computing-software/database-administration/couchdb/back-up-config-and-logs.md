---
id: computing-software.database-administration.couchdb.back-up-config-and-logs
name: back-up-config-and-logs
category: computing-software
field: database-administration
product: couchdb
tags: [backup, configuration, logs, log-rotation, ini-files]
level: practitioner
status: docs-checked
description: "Back up CouchDB configuration (etc/ ini chain) and log files, including the copy-then-truncate rule for log rotation and the Windows limitation."
sources:
  - https://raw.githubusercontent.com/apache/couchdb/main/src/docs/src/maintenance/backups.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Configuration.** Settings live in `.ini` files under the configuration directory (default `etc/`). Runtime changes are written to the very last file in the configuration chain. Back up the whole `etc/` directory to restore a consistent configuration.

You can skip this backup only if no configuration is changed at runtime through the HTTP API and every config file is managed by a configuration management system such as Ansible or Chef.

**Logs.** If CouchDB logs to a file, any backup solution works for those files.

Log rotation on UNIX-like systems:

- Use a copy-then-truncate approach: copy the log, then truncate the original to zero size in place.
- CouchDB does not recognise any signal telling it to close its log file and open a new one, so move-and-signal rotation will not work.

On Microsoft Windows there is no straightforward rotation solution other than periodic restarts of the CouchDB process, because of differences in file-handle behaviour.

## Checked

2026-11-04. Confirmed against the CouchDB maintenance/backups page (Configuration Backups, Log Backups): ini files under etc/, last file in the chain updated at runtime, when backup can be skipped, copy-then-truncate, no signal to reopen logs, Windows limitation. Nothing removed.

Method: documentation only; no commands were run.
