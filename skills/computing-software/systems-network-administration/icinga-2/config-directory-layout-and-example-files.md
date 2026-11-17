---
id: computing-software.systems-network-administration.icinga-2.config-directory-layout-and-example-files
name: config-directory-layout-and-example-files
category: computing-software
field: systems-network-administration
product: icinga-2
tags: [systems-network-administration, icinga-2, icinga2-conf, constants-conf, conf-d, zones-conf, include-recursive, nodename]
level: intro
status: docs-checked
description: Walk through /etc/icinga2 - icinga2.conf includes, constants.conf, zones.conf, the conf.d example files and how to use your own objects.d tree.
sources:
  - https://icinga.com/docs/icinga-2/latest/doc/04-configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# config directory layout and example files
`/etc/icinga2/icinga2.conf` is the entry point. It supports C/C++-style comments and uses:
- `include "constants.conf"` and `include "zones.conf"`
- `include <itl>`, `<plugins>`, `<plugins-contrib>`, `<manubulon>`, plus `<windows-plugins>` and `<nscp>` (needed on a master when a client is a command endpoint)
- `include "features-enabled/*.conf"` for features turned on with `icinga2 feature enable` (they are symlinks from `features-available`)
- `include_recursive "conf.d"`

**constants.conf** must set `PluginDir` (location of the Monitoring Plugins; used by built-in check commands) and `NodeName` (defaults to the FQDN, and should match the API certificate common name). `ZoneName` and `TicketSalt` are needed for remote clients and distributed setups; the `node setup`/`node wizard` tools populate them. `ManubulonPluginDir` is also defined.

**zones.conf** holds Zone and Endpoint objects for distributed monitoring plus several global zones. Replace names with real FQDNs.

**conf.d** is example configuration for monitoring the local host: hosts.conf, services.conf, users.conf, notifications.conf, commands.conf, groups.conf, templates.conf, downtimes.conf, timeperiods.conf, api-users.conf and app.conf. hosts.conf imports the `generic-host` template (check command `hostalive`).

**Own tree:** remove `include_recursive "conf.d"`, create e.g. `/etc/icinga2/objects.d` and add `include_recursive "objects.d"` (the approach used by the Icinga 2 Puppet module). Distributed setups use `zones.d`.

Tip: list generated objects with `icinga2 object list --type Host` after validation.

## Checked

2026-11-04. Confirmed against the Icinga 2 configuration chapter: icinga2.conf includes, constants.conf constants, objects.d own-tree approach used by the Puppet module.

Method: documentation only; no commands were run.
