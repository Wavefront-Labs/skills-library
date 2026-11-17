---
id: computing-software.systems-network-administration.icinga-2.top-down-config-sync-zones-d
name: top-down-config-sync-zones-d
category: computing-software
field: systems-network-administration
product: icinga-2
tags: [systems-network-administration, icinga-2, config-sync, zones-d, accept-config, global-zone, replay-log, config-master]
level: practitioner
status: docs-checked
description: "Sync Icinga 2 config to satellites with zones.d zone directories, accept_config, global zones, and the single config master rule."
sources:
  - https://icinga.com/docs/icinga-2/latest/doc/06-distributed-monitoring/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# top down config sync (zones.d)
The master syncs object configuration files within zones; satellites run their own scheduler and send results back. Advantages: validation and restart happen automatically, checks run on the child scheduler, a replay log covers dropped connections, and a global zone shares templates. Disadvantages: a `zones.d` directory per zone, extra zone and endpoint config, and the replay log replicated on reconnect may overload the connection.

Only configuration text files sync. Do not sync binaries (checksums may trigger reload loops); distribute plugins with packages, Puppet or Ansible.

Steps: define Endpoint and Zone objects on both nodes; on the satellite set `accept_config = true` in `/etc/icinga2/features-enabled/api.conf`; on the master create `/etc/icinga2/zones.d/<zone name>/` with Host and Service objects. A host object can use `zone = "master"` to sync the object while forcing the master to execute its check.

The flow: the master validates, copies the config into its zone store in `/var/lib/icinga2/api/zones`, sends a config update to endpoints in the same or direct child zones; the satellite populates its store, validates and restarts automatically.

Only one config master per zone may hold files in `zones.d`; multiple are not supported.

**Global zones** (`global = true`) deliver common config such as check commands to every node. The wizards create `global-templates` and `director-global`; use the first, but leave `director-global` to Icinga Director. Create `zones.d/global-templates/`, add e.g. a CheckCommand, restart receiving endpoints before their parents, then validate and restart the master. The `conf.d` examples can be copied into `global-templates`.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Read the full page https://icinga.com/docs/icinga-2/latest/doc/06-distributed-monitoring/. No commands were run.
