---
id: computing-software.systems-network-administration.restic.non-root-backup-capabilities
name: non-root-backup-capabilities
category: computing-software
field: systems-network-administration
product: restic
tags: [restic, non-root, capabilities, cap-dac-read-search, systemd, setcap]
level: advanced
status: docs-checked
description: "Back up the whole system without running restic as root using the CAP_DAC_READ_SEARCH capability via setpriv, systemd ambient capabilities or setcap."
sources:
  - https://restic.readthedocs.io/en/stable/080_examples.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Backing up without root

Reading every file only needs the Linux capability `CAP_DAC_READ_SEARCH`, not full root.

```
useradd --system --create-home --shell /sbin/nologin restic
```

## Ambient capabilities (recommended)

```
setpriv --no-new-privs --reuid=$(id -u restic) --regid=$(id -g restic) \
  --init-groups --reset-env --inh-caps +DAC_READ_SEARCH \
  --ambient-caps +DAC_READ_SEARCH \
  restic backup --exclude={/dev,/media,/mnt,/proc,/run,/sys,/tmp,/var/tmp} /
```

### With systemd

In the service's `[Service]` section:

```
DynamicUser=yes
AmbientCapabilities=CAP_DAC_READ_SEARCH
CapabilityBoundingSet=CAP_DAC_READ_SEARCH
```

No separate user is needed. Run `systemctl daemon-reload` after editing the unit.

## File capabilities

Copy the binary where only a dedicated user and root can run it, then set the capability:

```
chown root:restic /path/to/bin/restic
chmod 750 /path/to/bin/restic
setcap cap_dac_read_search=+ep /path/to/bin/restic
```

Anyone who can execute that binary can read most of the system, so restrict permissions. `restic self-update` or any replacement of the binary removes the capability; rerun `setcap`. See capabilities(7).

## Checked

Checked 2026-11-08 against the restic Examples page (080_examples), read in full. Confirmed: CAP_DAC_READ_SEARCH, the useradd command, the setpriv ambient capabilities command, the systemd directives DynamicUser, AmbientCapabilities and CapabilityBoundingSet, daemon-reload, the file capability permissions warning, chown and chmod 750, setcap, and the loss of capabilities after self-update. Removed: the trial-run advice, which the page does not state.

Method: documentation only; no commands were run.
