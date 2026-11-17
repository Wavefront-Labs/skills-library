---
id: computing-software.systems-network-administration.zabbix.upgrade-planning
name: upgrade-planning
category: computing-software
field: systems-network-administration
product: zabbix
tags: [upgrade, version-compatibility, proxy-upgrade, sqlite, packages, version]
level: practitioner
status: docs-checked
description: "Plan a Zabbix upgrade: order of components, proxy compatibility and direct upgrade paths."
sources:
  - https://www.zabbix.com/documentation/current/en/manual/installation/upgrade
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Upgrading page (current docs, Zabbix 8.0) has step-by-step instructions for Red Hat Enterprise Linux and Debian/Ubuntu packages, containers and sources, plus related pages for HA clusters (Upgrading HA cluster) and TimescaleDB (Upgrading TimescaleDB schema). Read the upgrade notes for every version you pass through before starting.

Components:
- Agents: upgrading is recommended, not mandatory.
- Proxies: highly recommended. The server fully supports proxies of the same major version as the server. It also supports proxies no older than the server's previous LTS release, with limited functionality: data collection, remote commands and immediate item value checks; configuration update is disabled and they work with old configuration. Proxies older than that, or newer than the server major version, are unsupported: the server ignores their data and communication fails with a warning.

Order to minimise downtime and data loss: stop, upgrade and start the server first, then stop, upgrade and start proxies one after another. Running proxies keep collecting while the server is down and send the data once it is up. Notifications for problems during server downtime are generated only after the upgraded server starts.

SQLite proxies: a missing database file is created on first start. If the existing file version is older than required, the proxy deletes it and creates a new one, so history stored in it is lost. If the proxy is older than the file, it logs an error and exits.

The database upgrade may take a long time depending on database size. The page states direct upgrade to 8.0.x is supported from versions 2.0.x; third-party integrations may break if the external software is not compatible with the new version. The upgrade notes table lists the notable changes per source version (for example raised minimum PHP and database versions).

## Checked

2026-11-09. Confirmed against the Upgrading page (components to upgrade, proxy compatibility, upgrade order, SQLite behaviour, direct upgrade range, related pages). Changed from the draft: the page now documents 8.0, so the 7.4 framing and the list of direct-upgrade source versions were replaced by the page's statement; removed the unfetched Debian/Ubuntu package page source and reference.
Method: documentation only; no commands were run.
