---
id: computing-software.cybersecurity-defensive.nessus.nessuscli-administration
name: nessuscli-administration
category: computing-software
field: cybersecurity-defensive
product: nessus
tags: [nessus, nessus-deployment, nessuscli, nessuscli-fix, plugin-update, backup, user-management, nessus-agent, troubleshooting]
level: practitioner
status: docs-checked
description: "Administer Nessus from the command line with nessuscli: updates, users, advanced settings, backups, bug reports and agent commands."
sources: ["https://docs.tenable.com/nessus/Content/NessusCLI.htm", "https://docs.tenable.com/nessus/command-line-reference/Content/BackupCommands.htm", "https://docs.tenable.com/nessus/command-line-reference/Content/LocalAgentsCommands.htm", "https://docs.tenable.com/nessus/command-line-reference/Content/UpdateThePluginsOnly.htm", "https://docs.tenable.com/nessus/Content/UpdatePluginsOffline.htm"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# nessuscli administration

**Goal:** manage a scanner headlessly and script the routine work (updates, settings, backups, diagnostics).

Location: `/opt/nessus/sbin/nessuscli` (Linux), `nessuscli.exe` in the Tenable Nessus folder under Program Files (Windows), `/Library/Nessus/run/sbin/nessuscli` (macOS). Run every command with administrative privileges. Agents have their own binary (Linux `/opt/nessus_agent/sbin/nessuscli`). `nessuscli help` and `nessuscli <cmd> help` list what your licence supports.

## Common commands (Nessus 10.12 CLI page)
| Task | Command |
|---|---|
| Update per the configured update options | `nessuscli update` |
| Force all components / plugins only | `nessuscli update --all` / `nessuscli update --plugins-only` |
| Offline plugin update from a TAR file | `nessuscli update <tar.gz filename>` (the Update Plugins Offline page also passes the `.tar.gz.sig` signature file) |
| Register online / check registration | `nessuscli fetch --register <Activation Code>` ; `nessuscli fetch --check` |
| Show the activation code in use | `nessuscli fetch --code-in-use` |
| Users | `nessuscli lsuser`, `adduser <username>`, `rmuser <username>`, `chpasswd <username>` |
| Advanced settings | `nessuscli fix [--secure] --list`, `--set <setting=value>`, `--get <setting>`, `--delete <setting>`; `nessuscli fix --show` lists all settings with defaults |
| Reset registration only | `nessuscli fix --reset` (deletes the secure preferences incl. linking keys; stop nessusd first) |
| Full reset | `nessuscli fix --reset-all` (deletes registration, settings, data and users; cannot be undone; Tenable says to contact Support first) |
| Backup / restore | `nessuscli backup --create <name>` (writes `<name>.<epoch>.zip`; `--targz`, `--include-backups` optional) ; `nessuscli backup --restore <path>` |
| Diagnostics archive | `nessuscli bug-report-generator` (`--quiet`, `--scrub`, `--full`, `--targz`) |

`nessuscli update` only works on standalone scanners, not those managed by Tenable One Vulnerability Management or Tenable Security Center. Offline mode (`fetch --register-offline`) disables commands that need the feed, including `nessuscli update`.

A backup contains your licence and settings but not scan results.

## Settings documented on the CLI page
`listen_address`, `path_to_java` (for PDF exports), `old_user_files_cleanup_hours`, `scanner_update_channel` (`ga`, `ea`, `stable`; Professional and TVM-managed scanners), and the password settings `passwd_complexity`, `xmlrpc_idle_session_timeout` (default 30 minutes), `user_max_login_attempt` (default 5, 0 disables), `min_password_len` (default 8) and `passwd_notifications` (System Administrator role needed). `max_hosts` is described in the Advanced Scan Settings page as capping hosts scanned at once.

## Agent CLI
```
nessuscli agent link --key=<key> --host=<host> --port=<port> [--name=... --groups=...]
nessuscli agent status
nessuscli agent unlink
```

## Gotchas
- `fix --reset-all` has no undo.
- Backups contain licence and settings: protect them.

## Verify
- [ ] A scripted `nessuscli update --plugins-only` runs on a schedule and logs success (standalone scanners only).
- [ ] A `nessuscli backup --create` file restores on a test host.

## Checked
2026-11-02. Confirmed from the Tenable Nessus 10.12 "Nessuscli" page, Command Line Reference pages "Backup Commands", "Local Agents Commands", "Update the Plugins Only", and "Update Plugins Offline". Removed (not found): `nessuscli -v`, `bug-report` details beyond the page, restart-after-`fix --set` rule, the settings `max_checks`, `global.max_scans`, `xmlrpc_listen_port`, `ssl_cipher_list`, `report_crashes`, `send_telemetry`, "Nessus 10.x" backup version claim, and root-permission error behaviour.

Method: documentation only; no commands were run.
