---
id: computing-software.messaging-and-integration.mosquitto.persistence-settings
name: persistence-settings
category: computing-software
field: messaging-and-integration
product: mosquitto
tags: [persistence, persistence-location, mosquitto-db, persistence-file]
level: practitioner
status: docs-checked
description: "Enable built-in persistence and choose where and under what name mosquitto.db is written."
sources:
  - https://mosquitto.org/man/mosquitto-conf-5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: keep subscriptions and messages across broker restarts.

```
persistence true
persistence_location /path/to/data/
persistence_file mosquitto.db
```

- `persistence true|false` enables built-in persistence; default false (in memory only). The page recommends a plugin based persistence instead. Connection, subscription and message data is written to `mosquitto.db` and reloaded on restart. Data is written when the broker closes, at intervals set by `autosave_interval`, or when it receives SIGUSR1.
- `persistence_file file name` defaults to `mosquitto.db`.
- `persistence_location path` is where plugins should store persistence data and where built-in persistence stores its data. If not given, the current directory is used.

All three apply globally and are reloaded on the reload signal.

The persistence file format may change in a new version. The broker can read all old formats but only saves in the latest. It should be safe to upgrade, but cautious users may copy the persistence file before installing a new version so they can roll back.

When run as root, `user` (default mosquitto) must have read/write access to the persistence database if it is to be written.

## Checked

Method: 2026-11-08 docs-only. Read the cited man page in full and compared each claim. Claims checked against mosquitto.conf(5). Removed the unsupported default packaged path; other claims unchanged.
