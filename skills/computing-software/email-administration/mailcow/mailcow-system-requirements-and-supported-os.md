---
id: computing-software.email-administration.mailcow.mailcow-system-requirements-and-supported-os
name: mailcow-system-requirements-and-supported-os
category: computing-software
field: email-administration
product: mailcow
tags: [system-requirements, supported-os, ram-sizing, virtualization, skip-clamd, skip-fts, time-sync]
level: intro
status: docs-checked
description: "Check hardware, OS, virtualisation and clock requirements before installing mailcow dockerized, including RAM sizing for ClamAV, FTS and SOGo ActiveSync."
sources: ["https://docs.mailcow.email/getstarted/prerequisite-system/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# mailcow system requirements and supported OS

The documented minimum is 1 GHz CPU, 6 GiB RAM plus 1 GiB swap (default configuration), 20 GiB disk without mail, on x86_64 or ARM64. Full virtualisation (KVM, ESX, Hyper-V) is supported; OpenVZ, Virtuozzo, LXC and NAS devices (Synology, QNAP) are not.

RAM is driven by ClamAV, the Flatcurve FTS engine and SOGo. A single SOGo worker can use about 350 MiB before it is purged and the default spawns 20 workers, so more ActiveSync connections need more RAM. The docs give 8 GiB as recommended for roughly 5 to 10 users and 16 GiB for a company with 15 ActiveSync phones and about 50 concurrent IMAP connections. To save memory, set `SKIP_CLAMD=y` and `SKIP_FTS=y` in `mailcow.conf`.

Officially tested operating systems (as of August 2025): Debian 11 to 13, Ubuntu 22.04 or newer, Alma Linux 8 and 9, Rocky Linux 9 (all fully compatible) and Alpine 3.19 or newer (limited, needs manual adjustments). Other systems may work but are untested. After a Debian 12 to 13 upgrade, remove the `exim` package, which can end up blocking port 25 on the host.

Clock: check `timedatectl status` for `NTP enabled: yes` and `NTP synchronized: yes`. Enable with `timedatectl set-ntp true` and set `NTP=` servers in `/etc/systemd/timesyncd.conf`. A correct clock matters for TOTP two-factor authentication.

## Checked

2026-11-04. Confirmed on the Prepare your system page: minimum CPU, RAM plus swap, disk and architectures, unsupported platforms and supported full virtualisation, SKIP_CLAMD/SKIP_FTS, the ~350 MiB SOGo worker and 20 default workers, the 8 GiB and 16 GiB sizing examples, the OS table as of August 2025, the Debian 12 to 13 exim note, and the timedatectl/NTP steps. No changes needed.

Method: documentation only; no commands were run.
