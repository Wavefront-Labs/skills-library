---
id: computing-software.networking-hardware-and-wireless.asterisk.pjsip-realtime-database
name: pjsip-realtime-database
category: computing-software
field: networking-hardware-and-wireless
product: asterisk
tags: [networking-hardware-and-wireless, asterisk, pjsip, realtime, sorcery, odbc, mysql, alembic, extconfig]
level: advanced
status: docs-checked
description: "Store PJSIP endpoints, auths, aors and identifies in a database: Alembic tables, res_odbc, sorcery.conf realtime wizard lines and extconfig.conf ps_ tables."
sources:
  - https://docs.asterisk.org/Configuration/Channel-Drivers/SIP/Configuring-res_pjsip/Setting-up-PJSIP-Realtime/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pjsip realtime database
Steps from the tutorial (MySQL via ODBC):
1. Install ODBC packages and Alembic; make sure `res_config_odbc`, `res_odbc` and the `res_pjsip_*` modules are built.
2. Create the database, then in `contrib/ast-db-manage/` copy `config.ini.sample` to `config.ini`, set `sqlalchemy.url`, and run `alembic -c config.ini upgrade head`. This creates tables such as `ps_endpoints`, `ps_auths`, `ps_aors`, `ps_contacts`, `ps_domain_aliases`, `ps_endpoint_id_ips`.
3. Configure the ODBC DSN, then `res_odbc.conf` (`enabled`, `dsn`, `username`, `password`, `pre-connect`). Check with the CLI command `odbc show`.
4. In `sorcery.conf`, map objects: `endpoint=realtime,ps_endpoints`, `auth=...`, `aor=...`, `domain_alias=...`, `contact=...` under `[res_pjsip]`, and `identify=realtime,ps_endpoint_id_ips` under `[res_pjsip_endpoint_identifier_ip]`.
5. In `extconfig.conf` `[settings]`, add lines like `ps_endpoints => odbc,asterisk`.

Other allowed tables: `ps_systems`, `ps_globals`, `ps_transports`, `ps_registrations`. To read both realtime and file data, list two lines for an object, e.g. `endpoint=realtime,ps_endpoints` and `endpoint=config,pjsip.conf,criteria=type=endpoint`; order sets which is read first.

## Checked

2026-11-09. Confirmed against the Asterisk Setting up PJSIP Realtime page: package and module requirements, Alembic steps in contrib/ast-db-manage, tables created, res_odbc.conf options and odbc show, sorcery.conf object mappings and the identifier_ip section, extconfig.conf lines, the extra allowed tables and the two-source sorcery lines. Nothing changed.
Method: documentation only; no commands were run.
