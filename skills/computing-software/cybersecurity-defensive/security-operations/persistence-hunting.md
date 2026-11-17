---
id: computing-software.cybersecurity-defensive.security-operations.persistence-hunting
name: persistence-hunting
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [threat-hunting, persistence-hunting, autoruns, scheduled-tasks, wmi-persistence, registry-run-keys, cron, systemd]
level: practitioner
status: docs-checked
description: "Hunt for persistence on Windows and Linux: run keys, services, scheduled tasks, WMI subscriptions, IFEO, cron, systemd, SSH keys, with Autoruns and Sysmon/Windows event sources."
sources: ["https://attack.mitre.org/tactics/TA0003/", "https://attack.mitre.org/techniques/T1547/001/", "https://attack.mitre.org/techniques/T1546/003/", "https://attack.mitre.org/techniques/T1546/012/", "https://attack.mitre.org/techniques/T1053/003/", "https://attack.mitre.org/techniques/T1098/004/", "https://attack.mitre.org/techniques/T1574/006/", "https://learn.microsoft.com/en-us/sysinternals/downloads/autoruns", "https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon", "https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4697", "https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4698"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Persistence hunting

**Goal:** find mechanisms an attacker installed to survive reboots and credential resets,
across the fleet, before or during incident response. ATT&CK tactic TA0003 (Persistence) lists
the techniques below; use its technique pages as the checklist.

## Windows locations
- Registry Run and RunOnce keys under HKLM and HKCU (`...\Windows\CurrentVersion\Run`,
  `RunOnce`), plus Startup folders (ATT&CK T1547.001). `RunOnceEx` exists but is not created by
  default on Vista and newer.
- Winlogon Helper DLL (T1547.004).
- Image File Execution Options: `Debugger` values under
  `HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\<executable>`
  (T1546.012); silent-exit monitors under `...\SilentProcessExit\`.
- AppInit DLLs (T1546.010), COM hijacking (T1546.015), services (T1543.003), scheduled tasks
  (T1053.005).
- WMI event subscriptions (T1546.003): filters, consumers and bindings that run code when an
  event fires; execution is proxied by `WmiPrvSe.exe` and can run as SYSTEM. Attackers may
  compile MOF files with `mofcomp.exe` to create them.
- Accounts: created accounts (T1136) and group changes (T1098).

## Linux locations
- Cron (T1053.003): crontab files live in OS-specific paths (for example
  `/var/spool/cron/crontabs/root` on ESXi); also review systemd timers (T1053.006).
- systemd services (T1543.002): ATT&CK's SysUpdate example places a script in
  `/usr/lib/systemd/system/` and sets `ExecStart` in the unit file.
- `~/.ssh/authorized_keys` (T1098.004): usually `<user-home>/.ssh/authorized_keys`; the SSH
  daemon config is usually `/etc/ssh/sshd_config`, where `PermitRootLogin`,
  `PubkeyAuthentication` may be changed. In cloud VMs, keys can be added through the provider
  CLI or API (for example the Google Cloud CLI `add-metadata` command).
- Dynamic linker hijacking (T1574.006): `LD_PRELOAD`, and `/etc/ld.so.preload` (modified by
  Hildegard and Rocke per ATT&CK).
- Unix shell configuration modification (T1546.004).

## Collect at scale
- **Autoruns** command line, per host, CSV for stacking: `autorunsc -a * -c -h -s -m`.
  Documented switches: `-a *` all entry types (selectors include `m` WMI entries, `s` services
  and drivers, `t` scheduled tasks, `w` Winlogon), `-c` CSV, `-h` file hashes, `-s` verify
  signatures, `-m` hide Microsoft entries, `-t` normalised UTC timestamps, `-z` offline
  system, and `*` as the user argument to scan all user profiles. Autoruns also has a
  "Hide Signed Microsoft Entries" option in the GUI.
- **Sysmon** events: 12 (registry object create and delete), 13 (registry value set),
  14 (key and value rename), 19, 20, 21 (WMI event filter, consumer, and consumer-to-filter
  activity), 1 (process creation).
- **Windows Security log:** 4697 (a service was installed), 4698 (a scheduled task was
  created), 4720 (a user account was created), 4732 (a member was added to a security-enabled
  local group). 4697 comes from the Audit Security System Extension subcategory and 4698 from
  Audit Other Object Access Events, so enable those subcategories.

## Analysis
Stack across similar hosts (rare entries first), then check each candidate: signer, path in a
user-writable folder, creation time near known incident activity, a command line with encoded
PowerShell or LOLBins (see lolbin-hunting), task or service names that imitate Microsoft ones.

## Gotchas
- Removing persistence before scoping lets the attacker notice and switch; coordinate with IR.
- Persistence can sit outside the host: cloud VM SSH keys (above) and identity-layer changes;
  hunt in the identity and cloud control plane too.
- Hunt with enough rights to read every user profile and registry hive; filtered views hide
  entries.

## Verify
Plant benign test persistence (a scheduled task and a run key) on a lab host; the hunt must
surface both.

## Checked
2026-11-08. Confirmed against ATT&CK TA0003 and the T1547.001, T1546.003, T1546.012,
T1053.003, T1098.004 and T1574.006 technique pages; the Autoruns/Autorunsc usage table; the
Sysmon event ID list (1, 12, 13, 14, 19-21); Microsoft Learn event pages 4697, 4698, 4720
and 4732. Removed: Velociraptor artifact names (the artifact reference page is a JavaScript
shell and could not be read), `-nobanner`, Event 7045 and `%SystemRoot%\System32\Tasks`,
Linux paths not on ATT&CK pages (`/etc/cron.*`, `rc.local`, `/etc/profile.d`, PAM, kernel
modules, sudoers), "UID 0" and `command=` advice, the task-name example, and OAuth/mailbox
rule/IAM key/federation claims.
Method: documentation only; no commands were run.
