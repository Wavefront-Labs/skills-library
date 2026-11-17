---
id: computing-software.cybersecurity-defensive.security-operations.macos-forensic-artefacts
name: macos-forensic-artefacts
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [digital-forensics, macos-forensics, unified-logs, launchagents, quarantine-events, fseventsd, aftermath, mac-apt, uac]
level: advanced
status: docs-checked
description: "Investigate a compromised Mac: triage collection with Aftermath or UAC, then parse quarantine, TCC, FSEvents, persistence and unified-log evidence with mac_apt."
sources: ["https://github.com/jamf/aftermath", "https://github.com/ydkhatri/mac_apt", "https://github.com/tclahr/uac"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# macOS forensic artefacts

## Collection
Collect live with a triage tool, then analyse offline.
- **Aftermath** (Jamf, Swift, open source, MIT): `sudo ./aftermath` runs the collection modules. It must run as root with Full Disk Access, which can be granted to the Terminal it runs in. Output goes to `/tmp` unless `-o` / `--output` says otherwise. Run `sudo ./aftermath --analyze <path_to_collection_zip>` on the resulting archive to get parsed databases, a timeline of file creation, last accessed and last modified dates, and a storyline of file metadata, database changes and browser information.
- Useful Aftermath options: `--deep` (time-intensive and memory-consuming file system scan), `--collect-dirs`, `--logs` (text file of extra unified log predicates, one per line as `name: predicate`), `--es-logs` (Endpoint Security events; defaults create, exec, mmap), `--disable` (switch off collection that may include personal data: browsers, databases, filesystem, proc-info, slack, ul) and `--cleanup`. `eslogger` and `tcpdump` run on extra threads and stop when Aftermath exits, so the last line of their output may be truncated.
- **UAC** (Unix-like Artifacts Collector): runs on macOS and many other Unix-like systems with no installation. `./uac -p ir_triage /tmp` collects the artefacts of the `ir_triage` profile. It follows the order of volatility, hashes running processes and executables, and can build a bodyfile.
- Deploy Aftermath from MDM where possible; the project ships a signed, notarized `Aftermath.pkg` that installs the binary to `/usr/local/bin/`.

## What Aftermath collects
Configuration profiles, log files, the LSQuarantine database, shell history and profiles (bash, csh, fish, ksh, zsh), the TCC database, the XProtect Behavioral Service (XBS) database, browser data (Arc, Brave, Chrome, Edge, Firefox, Safari), file timestamps from common directories, active network connections, persistence (BTM database, cron, emond, launch agents and daemons, login hooks and items, launchd and MDM overrides, periodic scripts, system extensions), a process tree built with TrueTree, install history, installed applications and users, MRT, XProtect and XProtect Remediator versions, and a security assessment (SIP, Gatekeeper, firewall, FileVault, remote login, screen sharing, login history). Its default unified log predicates are failed_sudo, login, manual_configuration_profile_install, screensharing, ssh, tcc and xprotect_remediator.

## Parsing with mac_apt
mac_apt is a macOS (and iOS) artefact parsing tool (Python, MIT). Plugins relevant to an intrusion:
- `AUTOSTART`: programs, daemons and services set to start at boot or login.
- `QUARANTINE`: the quarantine database and the `.LastGKReject` file.
- `TCC`: the Transparency, Consent and Control database.
- `FSEVENTS`: file system event logs from `.fseventsd`.
- `INSTALLHISTORY`: software installation history.
- `TERMSESSIONS` (Terminal bash and zsh history and sessions), `SUDOLASTRUN` (last sudo use), `RECENTITEMS`, `SCREENSHARING`, `NETUSAGE`, `XPROTECT` (XProtect diagnostic files and the Behavior Service database), `BIOME`, `SAFARI`, `CHROMIUM`, `FIREFOX`, `USERS`, `BASICINFO`.
- The mac_apt `UNIFIEDLOGS` plugin was removed because better options exist; `UNIFIEDLOGEXPORT` exports the unified logs and associated files for external processing. The README lists a KnowledgeC plugin as "coming soon".
- mac_apt includes code from the Chainbreaker project to read keychain files, which may be flagged as malware by AV or EDR products.

## Gotchas
- Collection tools will not see everything without Full Disk Access.
- Timestamps in these databases differ by source; state the source and convert to UTC in the report.
- Check the XProtect and XProtect Remediator data for what the platform already removed.
- Unified log, `log`, `sfltool`, plist and SQLite command usage is not covered here: use Apple's documentation and the tool help for the exact macOS version under investigation.

## Verify
Build the timeline in UTC and confirm the initial download (quarantine record) precedes the first persistence item and outbound connections seen in EDR or network logs.

## Checked
2026-11-08. Read in full: the Aftermath README (usage, options, collection list, default predicates, release package, TrueTree), the mac_apt README (plugin table, unified-log removal, Chainbreaker warning) and the UAC README (supported systems, `ir_triage` example, order of volatility, bodyfile). Removed as unconfirmed: all hand-run macOS commands and paths (`sfltool dumpbtm`, `log show`/`log collect` examples, `profiles show -all`, `systemextensionsctl list`, `plutil`, `sqlite3`), the specific plist and database locations (QuarantineEventsV2, knowledgeC.db, TCC.db, `/.fseventsd/`, `/var/db/receipts`), plist key names, "Full disk images are hard on Apple Silicon", "memory acquisition is limited", unified-log retention and Mac absolute time claims, the XProtect/MRT deletion claim, and the SANS macOS poster source (404). The UAC example output path was changed to the README form.
Method: documentation only; no commands were run.
