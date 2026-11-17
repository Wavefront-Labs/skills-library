---
id: computing-software.cybersecurity-defensive.endpoint-security.clamav-on-linux-servers
name: clamav-on-linux-servers
category: computing-software
field: cybersecurity-defensive
product: endpoint-security
tags: [antimalware, clamav, freshclam, clamd, clamonacc, linux-antivirus, file-upload-scanning, mail-scanning]
level: practitioner
status: docs-checked
description: "Run ClamAV on Linux servers where it fits (file uploads, mail, shared storage): freshclam updates, clamd, on-access scanning, and its limits versus EDR."
sources: ["https://docs.clamav.net/manual/Installing/Packages.html", "https://docs.clamav.net/manual/Usage/Scanning.html", "https://docs.clamav.net/manual/OnAccess.html", "https://docs.clamav.net/manual/Usage/Configuration.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ClamAV on Linux servers

**Goal:** scan files that cross trust boundaries (uploads, mail, shared drives serving Windows
clients) for known malware, with realistic expectations.

## Install and update
```
apt install clamav clamav-daemon        # or dnf install clamav clamd clamav-update
```
Debian-family packages: `clamav-daemon` is the scanner daemon (clamd) and `clamav-freshclam` the
signature updater; on RPM systems `clamav-update` provides the updater. Run `freshclam` to download
signatures, and check it succeeds. Behind a proxy, set `HTTPProxyServer` in `freshclam.conf`.
Configure `clamd.conf` with a local (Unix) socket, the preferred option, or a TCP socket.

## Scan
```
clamdscan --fdpass --multiscan /srv/uploads                  # via the daemon
clamscan -r --log=/var/log/clamav/scan.log /home             # standalone
```
`--fdpass` has `clamdscan` open each file and pass the descriptor to the daemon (Unix socket only,
not TCP); use `--stream` over TCP. `--multiscan` lets directory scans use several daemon threads.
Quarantine actions (`--move`, `--copy`, `--remove`) are performed by `clamdscan`, not `clamd`; pick
one per scan.

## On-access scanning
`clamonacc` (with clamd) uses Linux fanotify, which needs kernel 3.8 or newer and a distribution that
has not disabled it. In `clamd.conf`:
```
OnAccessIncludePath /srv/uploads
OnAccessPrevention yes
OnAccessExcludeUname clamav
```
- `OnAccessExcludeUname` must name the user clamd runs as, or clamonacc triggers events endlessly.
- `OnAccessIncludePath` does not accept `/`; keep the scope to upload and shared directories.
- `OnAccessPrevention` cannot be combined with `OnAccessMountPath`.
- Pass `--log=FILE` to `clamonacc`, otherwise it runs silently.
- Test with an EICAR file in the path: reading it should fail with "Operation not permitted".

## Limits
ClamAV is signature-based and not an EDR. For servers at risk of intrusion, use an EDR; ClamAV fits
content scanning.

## Verify
- [ ] EICAR in the upload path is detected and blocked.
- [ ] Signature updates are monitored (alert when `freshclam` fails).

## Checked
2026-11-01 against the ClamAV manual (Packages, Scanning, OnAccess, Configuration): confirmed package names, `--fdpass`/`--multiscan`/`--stream` behaviour, quarantine actions done by clamdscan, `--log`, fanotify and kernel 3.8, the On-Access options and restrictions, `HTTPProxyServer`, and the EICAR test. Removed: `--infected`, the INSTREAM and `StreamMaxLength` upload guidance, archive limit option names, the clamd memory figure, `sigtool --info` and cvdupdate advice, update frequency and the 24 h signature-age target, and the CIS and PCI DSS citations (not fetched).
Method: documentation only; no commands were run.
