---
id: computing-software.systems-network-administration.dns-dhcp.kea-configuration-backend
name: kea-configuration-backend
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dhcp, kea, config-backend, cb-cmds, mysql, postgresql]
level: practitioner
status: verified
description: "Store Kea DHCP configuration in a MySQL/PostgreSQL config backend: enabling it, cb_cmds API, server tags, polling, and what stays in the JSON file."
sources:
  - https://kea.readthedocs.io/en/latest/arm/hooks.html#libdhcp-cb-cmds-so-configuration-backend-commands
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Kea configuration backend

With many Kea servers sharing subnets, editing JSON on each is error-prone. The configuration
backend (CB) keeps subnets, shared networks, pools, options, option definitions and global
parameters in a database; servers poll it.

## Enable
```json
"Dhcp4": {
  "server-tag": "dc1-a",
  "config-control": {
    "config-databases": [{ "type": "mysql", "name": "kea", "user": "kea", "password": "...", "host": "db.example.internal" }],
    "config-fetch-wait-time": 20
  },
  "hooks-libraries": [
    { "library": "libdhcp_mysql.so" },        // 3.0+ (consolidated in 2.7.4); older Kea used libdhcp_mysql_cb.so
    { "library": "libdhcp_cb_cmds.so" }        // optional on servers that only fetch config; see the note below
  ]
}
```
`config-databases` takes exactly one database today, `config-fetch-wait-time` defaults to 30 s, and the
backend library must match the database `type` (`libdhcp_pgsql.so` for PostgreSQL) or the config
load fails. Initialise the schema with `kea-admin db-init mysql -u kea -p ... -n kea` (flags `-u`
user, `-p` password, `-n` database name; see `kea-admin` man page).

`libdhcp_cb_cmds.so` is available only to ISC customers with a paid support contract. The ARM says
the CB is "not plug-and-play": the only supported way to populate the database is that hook's API,
and `config-databases` should not be set until the preparation is done.

## Managing config
cb_cmds API over the control channel (the `service` key is only needed through a Control Agent, Kea 3.0.x and earlier):
```
{ "command": "remote-subnet4-set", "service": ["dhcp4"], "arguments": {
    "remote": { "type": "mysql" }, "server-tags": ["all"],
    "subnets": [{ "id": 100, "subnet": "10.20.30.0/24", "pools": [{ "pool": "10.20.30.50-10.20.30.200" }],
                  "shared-network-name": null }] } }
remote-subnet4-list, remote-option4-global-set, remote-server4-set ...
```
Server tags (`all` or specific) decide which servers receive each object; the server definition
(`remote-server4-set`) must exist before objects are tagged for it, except that servers using the
`all` tag need none. Stork updates subnets in the CB when `libdhcp_cb_cmds` is loaded (see the Stork
ARM; loading `subnet_cmds` and `cb_cmds` together is not recommended).

## What stays local
Interfaces, control sockets, lease database, hooks, logging, HA config: keep in the JSON file.
Do not define the same objects both locally and in the backend. Where they conflict the database
wins: file subnets with overlapping ids or prefixes are superseded by those from the database.
Keep each object in one place, ideally all subnets in the database and none in the file.

## Operations
- Changes apply at the next poll (`config-fetch-wait-time`, measured from the end of the last
  poll); `config-backend-pull` forces an immediate poll. Polling too often loads the database.
- Replicate the database: the configuration is fetched from it at startup and reconfiguration.

## Verify
- [ ] `config-get` on each server shows the subnet created via cb_cmds, and clients in it get leases.
