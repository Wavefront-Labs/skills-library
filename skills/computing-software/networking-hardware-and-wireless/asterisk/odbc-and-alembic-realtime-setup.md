---
id: computing-software.networking-hardware-and-wireless.asterisk.odbc-and-alembic-realtime-setup
name: odbc-and-alembic-realtime-setup
category: computing-software
field: networking-hardware-and-wireless
product: asterisk
tags: [networking-hardware-and-wireless, asterisk, odbc, res-odbc, alembic, realtime, func-odbc, database, schema, migration]
level: practitioner
status: docs-checked
description: "Connect Asterisk to a database via res_odbc.conf, verify with odbc show, and create or upgrade realtime tables with Alembic (config.ini, sqlalchemy.url)."
sources:
  - https://docs.asterisk.org/Configuration/Interfaces/Back-end-Database-and-Realtime-Connectivity/ODBC/Configuring-res_odbc/
  - https://docs.asterisk.org/Configuration/Interfaces/Back-end-Database-and-Realtime-Connectivity/Managing-Realtime-Databases-with-Alembic/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ODBC and Alembic for realtime
**res_odbc**: build with menuselect so `func_odbc`, `res_odbc` (required) and `res_odbc_transaction` (required) are included. In `res_odbc.conf`:
```
[asterisk]
enabled => yes
dsn => your-configured-dsn-name
username => your-database-username
password => insecurepassword
pre-connect => yes
```
At the CLI, `odbc show` lists configured DSNs and connection state. If the `odbc` command is missing, check the module file and permissions, that `modules.conf` has not set it to noload, and startup debug output (configured in `logger.conf`). If it shows "Connected: No", test the DSN with another tool such as `isql`. Verify real queries with `func_odbc`.

**Alembic** manages realtime schemas (scripts under `contrib/ast-db-manage` in the Asterisk source):
1. `pip install alembic`.
2. Copy `config.ini.sample` to `config.ini`.
3. Set `sqlalchemy.url` (for example a `mysql://` URL) and `script_location`: `config` (realtime schemas) or `voicemail` (ODBC voicemail).
4. Run `alembic -c config.ini upgrade head`.

It creates tables for all supported objects, so prune unwanted ones. Re-run the upgrade within a release series. Across series (for example 13.x to 15.x) data loss is possible: back up first and read the CHANGES and UPGRADE files.

## Checked
2026-11-09: read the Configuring res_odbc and Managing Realtime Databases with Alembic pages in full and confirmed the required modules, the res_odbc.conf example, odbc show and its troubleshooting, the Alembic steps, config and voicemail script_location values, and the cross-series data-loss warning. Nothing removed; every claim was confirmed.

Method: documentation only; no commands were run.
