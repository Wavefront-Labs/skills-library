---
id: computing-software.digital-forensics-incident-response.log-analysis.sysmon-filedelete-archiving
name: sysmon-filedelete-archiving
category: computing-software
field: digital-forensics-incident-response
product: log-analysis
tags: [sysmon-filedelete, sysmon, file-recovery, defence-evasion, dfir]
level: practitioner
status: docs-checked
description: "Use Sysmon FileDelete (23) and FileDeleteDetected (26) to catch attacker-deleted files: ArchiveDirectory behaviour, System-only ACL access, and disk growth risk."
sources: ["https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sysmon FileDelete archiving (events 23 and 26)

- **Event 23 FileDelete (File Delete archived)**: a file was deleted; besides logging the event, Sysmon saves
  the deleted file in the ArchiveDirectory.
- **Event 26 FileDeleteDetected (File Delete logged)**: a file was deleted; the event is logged without
  saving the file.

Attackers delete droppers, scripts and tools after use; event 23 keeps a copy for analysis.

## ArchiveDirectory
- The configuration entry `ArchiveDirectory` is the name of a directory at volume roots into which
  copy-on-delete files are moved. Default: `Sysmon`.
- The directory is protected with a System ACL; the Sysinternals page says you can use PsExec to reach it
  with `psexec -sid cmd`.
- Rules for FileDelete and FileDeleteDetected are set in the configuration like other events; the
  event reference is on the Sysmon page. Scope the rules narrowly.

## Gotchas
- Under normal operating conditions the archive directory might grow to an unreasonable size. Monitor disk
  use and limit what you archive (event 26 gives the logging without the copies).
- Treat the archive as live malware and never execute from it. AV exclusion decisions need care.

## Verify
- [ ] Deleting a test file that matches your rule produces event 23 and a copy in the archive directory (read via an elevated System context).

## Checked
2026-11-01. Confirmed against the Sysinternals Sysmon page: event 23 and 26 names and behaviour, the unbounded-growth warning, `ArchiveDirectory` meaning, default and System ACL with the PsExec access hint.
Removed: the XML rule example, version gate for event 26, archive file naming by hash, event field names, Velociraptor/KAPE collection, and the secure-delete claim, because the page does not state them.
Method: documentation only; no commands were run.
