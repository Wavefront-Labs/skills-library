---
id: computing-software.digital-forensics-incident-response.evidence-handling.lightweight-triage-collection-with-cylr
name: lightweight-triage-collection-with-cylr
category: computing-software
field: digital-forensics-incident-response
product: evidence-handling
tags: [cylr, triage-collection, live-response, sftp-collection, dfir]
level: practitioner
status: docs-checked
description: "Collect a lightweight forensic triage package with CyLR on Windows, Linux and macOS: default artefact list, custom paths, SFTP upload, verification and processing."
sources: ["https://github.com/orlikoski/CyLR", "https://github.com/orlikoski/CyLR/blob/master/README.md", "https://github.com/orlikoski/CDQR"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Lightweight triage collection with CyLR

CyLR (Live Response) is a .NET Core collector that grabs key forensic artefacts from hosts with NTFS file systems using a raw file collection process (not the Windows API), zips them, and can upload straight to SFTP. Releases (2.0 and higher) include self-contained builds for Windows x86 and x64, Linux x64 and macOS x64. It needs administrative rights on the target (root, sudo or administrator).

## What it collects by default
The README's standard list (all paths case-insensitive; `CollectionPaths.cs` holds the full list). Windows: Tasks, Prefetch, SRU, winevt Logs, `Appcompat\Programs`, `setupapi.dev.log`, hosts file, the SAM, SOFTWARE and SECURITY hives with their LOG1/LOG2 files (SYSTEM is not in the README list), the all-users Startup folder, `$MFT`, `$LogFile`, Recycle Bin `$I*` files, per-user NTUSER.DAT and UsrClass.dat with logs, Recent, PowerShell `ConsoleHost_history.txt`, Firefox profiles, WebCache, Explorer, ConnectedDevicesPlatform, and Chrome and Edge `History`. `$UsnJrnl` is not default: add `--usnjrnl`. Linux: named `/etc` files (hosts, passwd, group, crontab, sudoers, resolv.conf and others) and directories such as `/etc/cron.*`, `/etc/pam.d`, `/etc/systemd.d`, `/var/log`, `/var/spool/cron`, GRUB `grub.cfg`, per-user shell history, rc files, `.ssh` config, known_hosts and authorized_keys, and Firefox and Chrome profile files. macOS: hosts, passwd, group, `/var/log`, StartupItems, LaunchAgents and LaunchDaemons, `.fseventsd`, shell history and Chrome and Firefox profile data; modern macOS may need Full Disk Access granted to the CyLR binary and its parent process (such as Terminal). To add paths use `-d`; the custom file is tab-delimited with pattern types `static`, `glob`, `regex` and `force` (force also collects alternate data streams such as `$Extend\$UsnJrnl:$J`), and the path separator must match the platform.

## Usage
```text
CyLR.exe -od <EVIDENCE_DRIVE>\triage                              # write zip to an attached evidence drive
CyLR.exe -u sftpuser -p <secret> -s 10.99.1.30:22 -os /cases/2026-0147/   # upload over SFTP
CyLR.exe -c custom_paths.txt -od <EVIDENCE_DRIVE>\triage          # custom collection list
```
Key options: `-od` output directory (default: current directory), `-of` output filename (default: host name), `-zp` zip password, `-zl` compression level (default 3; the help text says 1-9 in the description and 0-9 in the usage line), `-c` custom paths file only, `-d` custom paths plus the defaults, `--usnjrnl`, `--dry-run`, `--force-native` (skip raw NTFS read; always used on Unix), `--no-sftpcleanup` (keep the local zip after upload), `-l` log path (default `./CyLR.log`), `-q` disable logging, `-v` verbose. SFTP: `-u`, `-p`, `-s host[:port]` (22 default), `-os` remote directory. Check `CyLR --help` for the version in your kit; options changed across releases.

## Procedure
1. Run from removable media or a network share, not by copying the binary onto the suspect disk.
2. Record start time, host, user context (needs admin/root) and binary hash in the collection log.
3. Hash the resulting zip immediately and again after transfer.
4. Process with CDQR (uses Plaso and a streamlined parser list, by Alan Orlikoski, as is CyLR), Plaso directly, or individual parsers (EZ Tools, RegRipper).

## Gotchas
- The README's `-h` output shows version 2.2.0.0 and its tested-OS list is older builds (Windows 10 build 1909, macOS 10.14, Debian 10, Ubuntu 18.04, CentOS 8.1, RedHat 8.1). Validate the tool on current OS builds before relying on it.
- The packed single-file binary unpacks into a cache on first run (for example `%LOCALAPPDATA%\warp\packages` on Windows), which writes to the host.
- No memory capture: collect RAM separately first (order of volatility).
- Uploading over SFTP with a password on the command line exposes it in process listings and EDR logs; use a dedicated, short-lived collection account.

## Verify
The zip opens, contains the expected hives and `$MFT`, its hash matches between endpoint and server, and Plaso parses it without missing-source errors.

## Checked
Confirmed against the CyLR README (help output, default collection paths, examples, custom path format, tested-OS list, warp cache note) and the CDQR README (Plaso-based). Removed the KAPE-licensing rationale, the "SYSTEM presumably" guess and the Amcache/jump list/LNK claim, none of which the README supports; corrected the Linux and macOS default lists to the files the README names. The SFTP password-exposure advice is general practice, not from the README.

Method: docs-only read of cited pages, 2026-11-08
