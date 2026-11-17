---
id: computing-software.cybersecurity-defensive.nessus.nessusd-troubleshooting
name: nessusd-troubleshooting
category: computing-software
field: cybersecurity-defensive
product: nessus
tags: [nessus, nessus-deployment, nessusd-troubleshooting, nessusd-messages, backend-log, debug-logging, plugin-compilation, nessuscli-bug-report]
level: practitioner
status: draft
description: "Diagnose a misbehaving Nessus scanner: log locations, debug logging, stuck plugin compilation, scans hanging or aborting, port 8834 issues and generating a bug report."
sources: ["https://docs.tenable.com/nessus/Content/NessusLogs.htm", "https://docs.tenable.com/nessus/Content/NessusCLI.htm", "https://docs.tenable.com/nessus/Content/AdvancedSettings.htm"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Troubleshooting nessusd

## Log locations
- Linux: `/opt/nessus/var/nessus/logs/`
- Windows: `%ProgramData%\Tenable\Nessus\nessus\logs\`
- macOS: `/Library/Nessus/run/var/nessus/logs/`
Files: `nessusd.messages` (service and scan events), `backend.log` (web/backend, licensing,
plugin updates), `www_server.log` (UI/API access), `nessusd.dump` (plugin errors during scans).

## More detail
Settings > Advanced > Logging, or CLI:
```
/opt/nessus/sbin/nessuscli fix --set log_details=true
/opt/nessus/sbin/nessuscli fix --set log_whole_attack=yes   # per-plugin attack log; very verbose, turn off after
/opt/nessus/sbin/nessuscli fix --set dumpfile=/opt/nessus/var/nessus/logs/nessusd.dump
```
Restart nessusd after changes (`systemctl restart nessusd`). Per-scan debug: scan policy >
Advanced > Debug settings "Enable plugin debugging" and "Log scan details to server".

## Symptom guide
- **UI says "Nessus is initializing / compiling plugins" for hours**: plugin DB rebuild. Check disk
  space and memory (compilation needs several GB); `nessuscli fix --reset` is not the fix. Watch
  `backend.log` for progress. A full rebuild: stop service, `nessusd -R`, start.
- **Plugin updates fail**: `nessuscli update --all` output and `backend.log`; proxy settings
  (`nessuscli fix --set proxy=...`), TLS inspection breaking `plugins.nessus.org`, expired activation.
- **Scan stuck at a percentage**: one host or plugin hanging. `nessusd.messages` shows
  "<host> is taking long"; set `max_checks`/`plugins_timeout`, exclude the host, or enable
  "Stop scanning hosts that become unresponsive".
- **Scan aborted / scanner crashed**: OOM killer on Linux (`dmesg | grep -i kill`); reduce `max_hosts`.
- **Cannot reach 8834**: `ss -ltnp | grep 8834`, host firewall, `nessuscli fix --show | grep listen`,
  certificate problems in `www_server.log`.
- **Credentialed checks failing**: not a daemon issue; check plugins 19506, 21745, 104410, 110385.

## Bug report bundle
```
/opt/nessus/sbin/nessuscli bug-report-generator --quiet --full
```
Produces an archive with logs and config for Tenable support (review for sensitive data first).

## Housekeeping
- Logs rotate by size (`logfile_rot`, `logfile_max_size`, `logfile_max_files` advanced settings).
- Old scan results fill disk; set "Remove scan history after" under scan settings.

## Verify
After a fix: `nessuscli fetch --check`, a small test scan completes, and `nessusd.messages` shows
the scan start and finish without errors.
