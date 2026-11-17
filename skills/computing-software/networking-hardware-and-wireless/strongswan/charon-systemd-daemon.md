---
id: computing-software.networking-hardware-and-wireless.strongswan.charon-systemd-daemon
name: charon-systemd-daemon
category: computing-software
field: networking-hardware-and-wireless
product: strongswan
tags: [networking-hardware-and-wireless, strongswan, charon-systemd, systemd, journal, service-unit]
level: practitioner
status: docs-checked
description: "Run strongSwan natively under systemd with charon-systemd: configure flags, the strongswan service unit, and journal logging with custom fields in the charon-systemd section."
sources:
  - https://docs.strongswan.org/docs/latest/daemons/charon-systemd.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# charon systemd daemon
charon-systemd is the IKE daemon like charon but built for systemd, using the systemd libraries and a simple service file. It is configured through the swanctl backend.

**Build.** `--enable-systemd --enable-swanctl`. To drop the legacy ipsec backend also add `--disable-charon --disable-stroke`. The unit directory is found by pkg-config, or set `--with-systemdsystemunitdir=`.

**Service.** The unit is named `strongswan`. Enable it once with `systemctl enable strongswan`, then use `systemctl start`, `stop` and `status`. After a reboot systemd starts it and runs `swanctl --load-all --noprompt` (the sample status shows this as ExecStartPost) to load connections, pools and credentials.

**Configuration.** Options in the `charon` section of strongswan.conf are inherited by charon-systemd, so most charon options apply. A section `charon-systemd` holds specific settings, notably `journal`, the native journal logger, configured like syslog loggers:

```
charon-systemd {
  journal {
    default = 1
    ike = 2
    knl = 3
  }
}
```

Logs go to the systemd journal by default (view with `journalctl`). Traditional `syslog` and `filelog` loggers may also be defined in this section. `default = -1` silences the journal logger.

**Journal fields.** LEVEL, GROUP, THREAD, IKE_SA_UNIQUE_ID and IKE_SA_NAME, plus MESSAGE and a per-message-type MESSAGE_ID. PRIORITY maps level 0 to LOG_NOTICE, 1 to LOG_INFO and anything higher to LOG_DEBUG.

## Checked
2026-11-04. Confirmed against the charon-systemd page: configure flags, unit name `strongswan`, systemctl commands, the ExecStartPost swanctl load, the `journal` section, `default = -1`, and the journal fields and PRIORITY mapping.

Method: documentation only; no commands were run.
