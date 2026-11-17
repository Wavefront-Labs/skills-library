---
id: computing-software.it-support-helpdesk.desktop-support.linux-desktop-users-networking-and-printing
name: linux-desktop-users-networking-and-printing
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, nmcli, networkmanager, cups, lpadmin, linux-desktop]
level: practitioner
status: docs-checked
description: "Administer Linux desktop networking with nmcli and printing with CUPS: add IPP Everywhere printers with lpadmin, list drivers and backends, share printers, enable debug logging."
sources:
  - "https://networkmanager.dev/docs/api/latest/nmcli.html"
  - "https://www.cups.org/doc/admin.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# linux-desktop-users-networking-and-printing

## Networking with nmcli
```bash
nmcli device status                          # status of all devices
nmcli connection show                        # all connections; --active for active ones
nmcli dev wifi                               # Wi-Fi access points NetworkManager knows
nmcli con up "Home Wi-Fi"                    # reuse an existing profile
nmcli con mod "Wired connection 1" ipv4.method manual ipv4.addresses 10.0.0.50/24 ipv4.dns "10.0.0.10"
nmcli con mod "Wired connection 1" ipv4.method auto
```
- First connection to a new SSID: `nmcli dev wifi con "<SSID>" password "<password>" name "<profile>"` creates a
  profile; next time use `nmcli con up id "<profile>"` so no extra profile is created.
- `nmcli device up` differs from `nmcli connection up`: the device form lets NetworkManager pick a suitable connection
  (and creates a default profile if none is compatible); the default wait timeout is 90 seconds.
- `nmcli dev down <dev>` disconnects and stops autoconnecting until autoconnect is set TRUE or you activate a connection.
- `nmcli dev modify` changes are temporary; `nmcli con mod` changes the saved profile.
- `--ask` (`-a`) makes nmcli prompt for missing values.

## CUPS printing (command line)
- Web interface at `http://localhost:631`; most operating systems also provide a GUI.
- `lpadmin -p <name>` creates or modifies a printer: `-E` enables it and accepts jobs, `-v` sets the device URI,
  `-m` sets the driver/model, `-D` description, `-L` location, `-o option=value`, `-x <name>` deletes it.
- `lpinfo -m` lists available drivers; `lpinfo -v` lists backends and discovered printers (use the reported URIs for
  USB and other direct devices).
- The `everywhere` driver (IPP Everywhere) suits nearly all network printers sold since about 2009:
  `lpadmin -p printername -E -v ipp://<printer-ip>/ipp/print -m everywhere`.
- Legacy printers can use the CUPS sample drivers, for example `-v socket://<printer-ip> -m drv:///sample.drv/laserjet.ppd`,
  which give only basic capability.
- Backends: dnssd, ipp, ipps (mandatory encryption), lpd, socket (AppSocket/JetDirect), usb.
- Per-printer options: `-o printer-error-policy=` (`abort-job`, `retry-job`, `retry-current-job`, `stop-printer`),
  `-o printer-is-shared=true|false`, `-u allow:` / `-u deny:` user lists.
- Sharing: `cupsctl --share-printers` and then `-o printer-is-shared=true` per printer.
- Troubleshoot: `cupsctl --debug-logging`, undo with `cupsctl --no-debug-logging`.

## Verify
The device has the expected address and DNS, and a test page prints.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed on the nmcli manual and the CUPS command-line administration page. The Red Hat SSSD page was blocked (403),
so the realmd/SSSD section was removed. Also removed as not on the cited pages: the local users and groups commands,
`ipv4.gateway` example, netplan advice, `lpstat`, `lpoptions`, `cancel`, the cups restart command and log paths.
