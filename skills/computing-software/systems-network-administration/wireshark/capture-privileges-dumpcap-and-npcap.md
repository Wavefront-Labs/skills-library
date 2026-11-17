---
id: computing-software.systems-network-administration.wireshark.capture-privileges-dumpcap-and-npcap
name: capture-privileges-dumpcap-and-npcap
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, dumpcap-permissions, npcap, wireshark-group, setcap, capture-privileges, chmodbpf]
level: practitioner
status: verified
description: "Let non-root users capture safely: Linux wireshark group and dumpcap capabilities, macOS ChmodBPF, Windows Npcap admin-only and loopback options."
sources:
  - https://wiki.wireshark.org/CaptureSetup/CapturePrivileges
  - https://npcap.com/guide/npcap-users-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Capture privileges (dumpcap, Npcap)

Wireshark itself never needs root: only `dumpcap` opens interfaces. Running the whole GUI as
root/admin exposes hundreds of dissectors (parsing hostile packets) with full privileges.

## Linux
```bash
sudo dpkg-reconfigure wireshark-common      # Debian/Ubuntu: answer Yes
sudo usermod -aG wireshark "$USER"           # then log out and back in
getcap /usr/bin/dumpcap                      # expect cap_net_admin,cap_net_raw=eip
```
The Debian package's own README gives these three steps (`dpkg-reconfigure wireshark-common`, `usermod -a -G wireshark`,
log in again) and its post-install script runs `setcap cap_net_raw,cap_net_admin=eip` on dumpcap, falling back to
setuid if `setcap` fails.
Manual (other distros):
```bash
sudo groupadd -f wireshark
sudo chgrp wireshark /usr/bin/dumpcap
sudo chmod 750 /usr/bin/dumpcap
sudo setcap cap_net_raw,cap_net_admin=eip /usr/bin/dumpcap
```
Changing the group clears file capabilities, which is why `setcap` comes last (Wireshark wiki). Package upgrades can
reset capabilities; recheck with `getcap`. `CAP_NET_RAW` is the capability for RAW and PACKET sockets and `CAP_NET_ADMIN` for network configuration (capabilities(7)).


## macOS
The Wireshark installer's "ChmodBPF" launch daemon runs `chgrp access_bpf /dev/bpf*` and `chmod g+rw /dev/bpf*` (read
from the script in the Wireshark source); add the user to that group. Symptom without it: "You don't have permission to
capture on that device".

## Windows (Npcap)
- Installer option "Restrict Npcap driver's access to Administrators only" (`/admin_only`) needs UAC elevation for each
  capturing process (via `NpcapHelper.exe`); leave it off on analyst workstations, on for shared servers.
- Loopback: `\Device\NPF_Loopback` ("Adapter for loopback traffic capture") is built into current Npcap and worked with
  `dumpcap` here without any option. The installer's "Support loopback traffic" option (`/loopback_support`) now only installs
  the legacy Npcap Loopback Adapter for Nmap 7.80 and older and is "not needed for Wireshark" (Npcap guide).
- "Support raw 802.11 traffic (and monitor mode) for wireless adapters" (`/dot11_support`) for supported Wi-Fi adapters;
  frames get a Radiotap header.
- No interfaces listed: Npcap driver not running (`sc query npcap`, `net start npcap` from an Administrator prompt), or
  reinstall Npcap.

## Verify
```bash
dumpcap -D            # lists interfaces as a normal user
dumpcap -i eth0 -c 5 -w /tmp/t.pcapng
```
- [ ] Non-root user lists interfaces and captures; GUI not running as root/admin.

## Checked
Run on Windows with Wireshark 4.4.1/Npcap: `dumpcap -D` listed interfaces including `\Device\NPF_Loopback`, and a 4 second
capture on it wrote packets. Npcap users guide read for the installer options and `sc query npcap`/`net start npcap`.
Wireshark's CapturePrivileges wiki (GitLab copy) read for the setcap and chgrp order; the Debian `README.Debian` and
`wireshark-common.postinst`, and the macOS `ChmodBPF` script, read from the Wireshark source on GitLab. The Linux and macOS
commands follow those files and capabilities(7).
