---
id: computing-software.systems-network-administration.icinga-2.master-setup-node-wizard
name: master-setup-node-wizard
category: computing-software
field: systems-network-administration
product: icinga-2
tags: [systems-network-administration, icinga-2, node-wizard, master-setup, ca, global-zones, conf-d, api-users]
level: practitioner
status: docs-checked
description: Set up an Icinga 2 master with icinga2 node wizard - parameters asked, what it changes (api feature, CA, zones.conf, conf.d disabled) and why to back up the CA key.
sources:
  - https://icinga.com/docs/icinga-2/latest/doc/06-distributed-monitoring/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# master setup with the node wizard
Install the package and plugins first. Windows is not supported for a master node. Run `icinga2 node wizard` and answer `n` to "satellite/agent setup" to install a master.

Parameters:
- Common name (CN): required, the FQDN by default.
- Master zone name: defaults to `master`.
- Global zones: in addition to the defaults `global-templates` and `director-global`.
- API bind host and port: advanced only; changing default port 5665 must be done everywhere.
- Disable conf.d: defaults to `y`, removing the `include_recursive "conf.d"` directive except for `api-users.conf`, because master configuration should be managed in zones.

The wizard:
- enables the `api` feature,
- generates a certificate authority in `/var/lib/icinga2/ca` if missing,
- creates a node certificate signed by that CA,
- updates `zones.conf`, the ApiListener and constants,
- updates `icinga2.conf` to disable `conf.d` and include `api-users.conf`.

Then restart the daemon. Keep `/var/lib/icinga2/ca` secure and in your backups: if the CA private key is lost you must create a new CA and re-create signed certificates for all existing nodes.

The master can then act as the primary CSR auto-signing master (see the certificate signing skill). All certificates must be signed by the same CA, which should be the same on all master instances.

## Checked

2026-11-04. Confirmed against the Icinga 2 distributed monitoring chapter: wizard parameters and defaults, Windows unsupported for masters, steps performed, CA key loss consequence.

Method: documentation only; no commands were run.
