---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.userassist-gui-execution-evidence
name: userassist-gui-execution-evidence
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [userassist, evidence-of-execution, ntuser, rot13, windows-forensics, dfir]
level: practitioner
status: draft
description: "Decode UserAssist entries in NTUSER.DAT for GUI program execution: ROT13 names, GUIDs, run count, focus time and last run time, and their limits."
sources: ["https://www.sans.org/posters/windows-forensic-analysis/", "https://ericzimmerman.github.io/", "https://github.com/keydet89/RegRipper3.0"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# UserAssist GUI execution evidence

**Goal:** show that a user launched a program through the Windows shell (Explorer, Start
menu, desktop shortcut), how often and when last.

## Location
`NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\UserAssist\{GUID}\Count`
- `{CEBFF5CD-ACE2-4F4F-9178-9926F41749EA}`: executable launches.
- `{F4E57C4B-2036-45F0-A9AB-443BCFE33D9F}`: shortcut (LNK) launches.
Value names are **ROT13** encoded paths, often with Known Folder GUIDs
(`{6D809377-6AF0-444B-8957-A3773F02200E}` = Program Files).

## Data (Windows 7+, 72-byte structure)
Run count (offset 4), focus count (offset 8), focus time in ms (offset 12), last run
FILETIME (offset 60).

## Parse
Registry Explorer decodes it (UserAssist plugin); RegRipper `userassist`; RECmd batch.

## Interpretation
- Only shell-launched GUI programs; command-line execution (cmd, PowerShell, services,
  scheduled tasks, remote execution) does not appear.
- Run counts are unreliable across Windows versions; prefer last run time and presence.
- Attribution: entries are per user hive, so they tie execution to the profile.
- Disabled if `Start_TrackProgs` = 0 under `Explorer\Advanced`.

## Typical findings
Attacker opening `mstsc.exe`, `procexp.exe`, archive tools (7zFM.exe), browsers to download
tools, or a renamed tool from the Desktop during an RDP session.

## Verify
Correlate with RDP logon session times (4624 type 10, TerminalServices logs) to confirm the
interactive session that produced the launches.
