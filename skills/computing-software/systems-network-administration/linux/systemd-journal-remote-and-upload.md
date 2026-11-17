---
id: computing-software.systems-network-administration.linux.systemd-journal-remote-and-upload
name: systemd-journal-remote-and-upload
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, systemd, journald, journal-remote, systemd-journal-remote, systemd-journal-upload, centralised-logging, log-shipping, lpic-2, sysadmin]
level: practitioner
status: docs-checked
description: "Centralise journals natively: systemd-journal-remote receiver (HTTPS, per-host files), systemd-journal-upload sender with cursor state, TLS, and querying merged journals."
sources:
  - https://www.freedesktop.org/software/systemd/man/latest/systemd-journal-remote.service.html
  - https://www.freedesktop.org/software/systemd/man/latest/systemd-journal-upload.service.html
  - https://www.freedesktop.org/software/systemd/man/latest/journal-remote.conf.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ship journals with systemd-journal-remote/upload

**Goal:** collect structured journal entries (all fields, not flattened syslog text) from many
hosts onto one log server, without losing entries across restarts.

## 1. Packages
Both sides need the `systemd-journal-remote` and `systemd-journal-upload` programs (package names vary by distribution).

## 2. Receiver
```bash
# /etc/systemd/journal-remote.conf
[Remote]
SplitMode=host                  # one journal file set per sending host
ServerKeyFile=/etc/ssl/private/journal-remote.key
ServerCertificateFile=/etc/ssl/certs/journal-remote.pem
TrustedCertificateFile=/etc/ssl/certs/journal-ca.pem   # CA certificate used to verify the peer
```
```bash
systemctl enable --now systemd-journal-remote.socket     # default port 19532
ls /var/log/journal/remote/                              # remote-<host>.journal files
```
Plain HTTP: `--listen-http=` instead of `--listen-https=` (lab only); a negative number such as `-3` means a socket-activated file descriptor.

## 3. Sender
```bash
# /etc/systemd/journal-upload.conf
[Upload]
URL=https://logs.example.com:19532
ServerKeyFile=/etc/ssl/private/client.key
ServerCertificateFile=/etc/ssl/certs/client.pem
TrustedCertificateFile=/etc/ssl/certs/journal-ca.pem
```
```bash
systemctl enable --now systemd-journal-upload.service
journalctl -u systemd-journal-upload -f       # watch for TLS/connection errors
cat /var/lib/systemd/journal-upload/state     # cursor of last uploaded entry
```
Upload resumes from the saved cursor after network outages or reboots, so nothing is skipped
as long as the local journal hasn't rotated the entries away (size local journal accordingly).

## 4. Query on the server
```bash
journalctl -D /var/log/journal/remote -u sshd --since today
journalctl --file '/var/log/journal/remote/remote-web01*.journal' -p err
journalctl -m                               # interleave all available journals, including remote ones
```
Disk use: `MaxUse=`, `KeepFree=`, `MaxFileSize=` and `MaxFiles=` in `journal-remote.conf` (systemd 253 and later) limit what the receiver keeps.

## Gotchas
- The upload cursor lives in the state file; local journal retention must outlive a receiver outage.

## Verify
- [ ] `logger -t uploadtest hello` on a client appears in `journalctl -D /var/log/journal/remote -t uploadtest` within seconds.
- [ ] Stop the receiver, log a message, restart it: the message still arrives.

## Checked

2026-10-25, against the systemd v262.1 documentation (man pages and NEWS in the systemd/systemd repository, main branch). Confirmed: default port 19532; `--listen-http=`/`--listen-https=` take a negative file descriptor or a `ListenStream=` address; output under `/var/log/journal/remote/` as `remote-<host>.journal`; `journal-remote.conf` keys `SplitMode=host|none`, `ServerKeyFile=`, `ServerCertificateFile=`, `TrustedCertificateFile=`; `MaxUse=` etc. arrived in v253 (NEWS), not v249; `journal-upload.conf` `URL=` has no default; state file `/var/lib/systemd/journal-upload/state` with `--save-state`; `journalctl -m`, `-D`, `--file`. Removed distro package names, the firewalld command, the certificate-error text and the rsyslog comparison.

Method: documentation only; no commands were run.
