---
id: computing-software.systems-network-administration.ceph.config-set-runtime-and-show
name: config-set-runtime-and-show
category: computing-software
field: systems-network-administration
product: ceph
tags: [ceph, config, ceph-config, tell, runtime, central-config]
level: practitioner
status: docs-checked
description: "Use the Ceph central config database: config set/get/show, tell for runtime overrides, and finding options with config help."
sources:
  - https://docs.ceph.com/en/latest/rados/configuration/ceph-conf/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Persistent settings live in the monitor config database:

```
ceph config set osd.1701 debug_ms 20
ceph config set mgr mgr/<module>/<option> <value>
ceph config ls | grep ^osd_recovery
ceph config help log_file
```

Runtime override on running daemons without persisting:

```
ceph tell osd.1701 config set debug_osd 20
ceph tell osd.* config set debug_osd 20
ceph daemon osd.4 config set debug_osd 20
```

Inspect what a daemon uses:

```
ceph config show osd.1701
ceph config show osd.1701 debug_osd
ceph config show-with-defaults osd.1701
ceph daemon osd.1701 config diff
```

Rules:

- `ceph daemon` connects to the admin socket on the host where the daemon runs; `ceph tell` and `ceph daemon` overrides are ephemeral and revert when the daemon restarts.
- A `ceph.conf` file is mainly for bootstrap options such as monitor addresses; prefer the database for everything else.
- Manager module options need the `mgr/<module>/` prefix.

Precedence, lowest to highest: compiled-in default, the monitor central database, the local configuration file, environment variables, command-line arguments, and runtime overrides through the admin socket or injection; the last value wins. So an option customised in a local `ceph.conf` makes the central setting be ignored. Options can have a mask, for example `osd/rack:foo` for OSDs under the `foo` rack bucket, and masks can also use a device class. Log levels range from 0 to 20. `ceph config get <who>` shows only compiled-in defaults and may differ from `ceph config show`; use `ceph config dump` to see what is in the monitor database. Move an old file into the database with `ceph config assimilate-conf -i <input_file> -o <output_file>`, which writes unrecognised settings to the output file.

## Checked

2026-11-09. Confirmed against the Ceph docs page Configuring Ceph (rados/configuration/ceph-conf): config set/ls/help/show/show-with-defaults/dump/assimilate-conf, tell and daemon injection examples, mgr/<module>/ option form, masks, the precedence list, log level range 0-20, and local file overriding the central database. Removed the unconfirmed `ceph config get global` error claim and the claim that `ceph tell` goes through the monitors.

Method: documentation only; no commands were run.
