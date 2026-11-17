---
id: computing-software.systems-network-administration.samba.ad-dc-time-sync
name: ad-dc-time-sync
category: computing-software
field: systems-network-administration
product: samba
tags: [systems-network-administration, samba, ad-dc-time-sync, ntp-signd, chrony, ntpd, kerberos, time-synchronisation]
level: advanced
status: docs-checked
description: "Configure signed NTP on a Samba AD DC with chrony or ntpd using ntpsigndsocket, set ntp_signd directory permissions, and know the 5 minute Kerberos skew."
sources:
  - https://wiki.samba.org/index.php/Time_Synchronisation
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ad dc time sync
Requirements: ntpd 4.2.6+ or chrony 3.0+, built with signed NTP support (`--enable-ntp-signd`). ntpsec will not work with Samba.

chrony lines (`/etc/chrony/chrony.conf`):
```
bindcmdaddress 192.168.0.2
allow 192.168.0.0/24
ntpsigndsocket  /usr/local/samba/var/lib/ntp_signd
```
(plus lines for your external time servers, `rtcsync`, `makestep 1 3`).

ntpd lines (`restrict default ... mssntp` is the key one):
```
ntpsigndsocket  /usr/local/samba/var/lib/ntp_signd/
restrict default kod nomodify notrap nopeer limited mssntp
```
On VMs append `tinker panic 0`.

Socket directory permissions (created after Samba first starts; some distributions use `/var/lib/samba/ntp_signd/`):
- ntpd: `chown root:ntp <dir>` and `chmod 750 <dir>`
- chrony: `chown root:_chrony <dir>` and `chmod 750 <dir>`
Verify `ls -ld <dir>` shows `drwxr-x---`.

Notes: the default maximum AD time deviation is 5 minutes. Recommended layout on the wiki: the PDC emulator DC syncs with an internet time server and other DCs and workstations follow; set up a time server on all DCs. Windows clients default to NT5DS; if the DC is not set up for mssntp, use Type NTP instead.

## Checked

2026-11-04. Confirmed against the Samba wiki page Time Synchronisation: ntpd 4.2.6+ and chrony 3.0+ with --enable-ntp-signd, the ntpsec warning, chrony and ntpd example lines, ntp_signd directory ownership and mode for ntp and _chrony, the alternate /var/lib/samba/ntp_signd path, tinker panic 0 for VMs, the 5 minute deviation, the PDC emulator layout, and NT5DS versus Type NTP. Removed the `server ... iburst` fragment (not on the page).
Method: documentation only; no commands were run.
