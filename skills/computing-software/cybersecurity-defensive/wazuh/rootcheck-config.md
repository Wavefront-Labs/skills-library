---
id: computing-software.cybersecurity-defensive.wazuh.rootcheck-config
name: rootcheck-config
category: computing-software
field: cybersecurity-defensive
product: wazuh
tags: [rootcheck, rootkit-files, rootkit-trojans, skip-nfs, check-pids, scanall]
level: practitioner
status: docs-checked
description: "Configure Wazuh rootcheck: frequency, rootkit signature files, check_* toggles, skip_nfs, scanall and readall defaults."
sources:
  - https://documentation.wazuh.com/current/user-manual/reference/ossec-conf/rootcheck.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The `<rootcheck>` block holds options for policy monitoring and anomaly detection.

Defaults and values:
- `disabled`: `no`.
- `frequency`: `43200` seconds (12 hours); allowed value is a positive number of seconds.
- `base_directory`: `/` on UNIX, the root of the C drive on Windows; a prefix for the rootkit, trojan, /dev and hidden-file checks.
- `rootkit_files`: `etc/shared/rootkit_files.txt`; `rootkit_trojans`: `etc/shared/rootkit_trojans.txt`. Paths may be relative to the Wazuh installation directory or full.
- `windows_audit`, `system_audit`, `windows_apps`, `windows_malware`: paths to definition files; default n/a.
- `scanall`: `no`; tells rootcheck to scan the entire system and may lead to some false positives.
- `readall`: `no`; with `no`, only a fixed list of folders is checked (/bin, /sbin, /usr/bin, /usr/sbin, /dev, /lib, /etc, /root, /var/log, /var/mail, /var/lib, /var/www, /usr/lib, /usr/include, /tmp, /boot, /usr/local, /var/tmp, /sys).
- `ignore`: one file or directory per line, type `sregex` (simple regex); valid for `check_sys`, `check_dev` and `check_files`. The default Unix configuration shows `<ignore type="sregex">^/etc/</ignore>`.
- `skip_nfs`: `yes`; works on Linux and FreeBSD and currently excludes files on CIFS or NFS mounts.
- Toggles all defaulting to `yes`: `check_dev`, `check_files`, `check_if`, `check_pids`, `check_ports`, `check_sys`, `check_trojans`, `check_unixaudit`, `check_winapps`, `check_winaudit`, `check_winmalware`.

Tuning notes:
- Set an individual `check_*` option to `no` to skip that check instead of disabling the whole module with `disabled`.
- `scanall` set to `yes` may add false positives.
- Leave `skip_nfs` at `yes` unless you deliberately want CIFS/NFS mounts scanned.

## Checked

2026-11-08: confirmed against the Wazuh ossec.conf reference page for rootcheck (read in full): every option name, default, allowed value, the readall folder list, ignore validity, skip_nfs behaviour and the default Unix configuration. Removed unsupported cost/slowness claims.
Method: documentation only; no commands were run.
