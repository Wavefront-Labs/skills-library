---
id: computing-software.systems-network-administration.wireshark.dumpcap-as-a-service
name: dumpcap-as-a-service
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, dumpcap, dumpcap-service, ring-buffer, systemd, continuous-capture]
level: practitioner
status: docs-checked
description: "Run dumpcap as a long-running systemd or Windows service with ring buffers, capture filters, rotation and disk monitoring for always-on capture."
sources:
  - https://www.wireshark.org/docs/man-pages/dumpcap.html
  - https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html
  - https://wiki.wireshark.org/CaptureSetup/CapturePrivileges
  - https://www.wireshark.org/docs/man-pages/capinfos.html
  - https://www.wireshark.org/docs/man-pages/mergecap.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Long-running dumpcap as a service

For intermittent problems, keep a rolling capture running so the evidence exists when the user calls.

## Command
```
dumpcap -i ens192 -f "not port 22" -s 256 -b filesize:200000 -b files:100 \
  -w /var/capture/core.pcapng -q
```
- `-b filesize:<KB>` switches file after that many kB (200000 is about 200 MB); `-b files:100` forms a
  ring of 100 files. `files` needs another criterion (`duration`, `interval` or `filesize`), and each
  `-b` takes exactly one criterion, so repeat `-b`.
- `-b duration:3600` switches after that many seconds; `-b interval:3600` switches when the clock
  time is an exact multiple (every hour on the hour).
- The `files` value must be below 100000, and very large file counts can strain some filesystems.
- `-s 256` limits each packet to 256 bytes: headers kept, less disk use and privacy exposure.
- `-B 64` raises the capture buffer (MiB, default 2) if you see drops on bursty links.
- `-f` is the capture filter; `-q` suppresses the packet counter output.

## systemd unit
```
[Unit]
Description=Rolling packet capture
After=network-online.target
[Service]
User=capture
ExecStart=/usr/bin/dumpcap -i ens192 -f "not port 22" -s 256 -b filesize:200000 -b files:100 -w /var/capture/core.pcapng -q
Restart=on-failure
[Install]
WantedBy=multi-user.target
```
Run as an unprivileged user, not root. Give the dumpcap binary capture rights with file capabilities,
per the Wireshark capture privileges page: `setcap cap_net_raw,cap_net_admin+eip` on the dumpcap path
(`/usr/sbin` or `/usr/bin` depending on the distro). Changing the file's group clears file
capabilities, so reapply setcap afterwards.

## Windows
Start dumpcap at boot from a scheduler or service wrapper writing to a capture folder. Note that
the Npcap installer option "Restrict Npcap driver's access to Administrators only" limits who can
capture, so the account running the job must have those rights.

## Operations
- Alert on disk usage and on the newest file's mtime getting old (capture died).
- After the incident, copy the relevant files out before rotation overwrites them; stop the unit if
  needed.
- `capinfos -a -e <files>` prints the earliest and latest packet timestamps of each file, to find the
  files covering the incident time.
- `mergecap -w incident.pcapng <file1> <file2>` merges inputs in chronological order by timestamp
  (unless `-a`, which concatenates).

## Verify
- [ ] Reboot the host and confirm new ring files appear and old ones are deleted at the limit.

## Checked
Method: docs-checked 2026-11-09 against the dumpcap, capinfos and mergecap man pages (option sections read), the Wireshark CapturePrivileges wiki page (setcap, Npcap restriction) and the systemd.service page (Restart=on-failure grepped). Dropped: AmbientCapabilities and Group lines, NSSM and the scheduled-task detail, and the "3.6+" version claim, none of which the pages confirm.
