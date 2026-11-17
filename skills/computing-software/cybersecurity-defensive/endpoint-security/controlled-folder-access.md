---
id: computing-software.cybersecurity-defensive.endpoint-security.controlled-folder-access
name: controlled-folder-access
category: computing-software
field: cybersecurity-defensive
product: endpoint-security
tags: [controlled-folder-access, ransomware-protection, defender-antivirus, protected-folders, allowed-applications, windows-endpoint-protections]
level: practitioner
status: docs-checked
description: "Deploy Defender Controlled Folder Access against ransomware: audit mode, protected folders, allowing legitimate apps, block event analysis and rollout pitfalls."
sources: ["https://learn.microsoft.com/en-us/defender-endpoint/controlled-folders", "https://learn.microsoft.com/en-us/defender-endpoint/enable-controlled-folders", "https://learn.microsoft.com/en-us/defender-endpoint/customize-controlled-folders"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Controlled folder access

Only trusted applications may modify files in protected folders (Documents, Pictures, Desktop, etc.,
plus folders you add). Untrusted processes - such as ransomware - get blocked.

## Rollout
1. **Audit mode** first: `Set-MpPreference -EnableControlledFolderAccess AuditMode` (or Intune ASR policy "Enable Controlled Folder Access" = Audit). Collect events for a full business cycle.
2. Review: Event 1124 (audited), 1123 (blocked) in `Microsoft-Windows-Windows Defender/Operational`; Defender advanced hunting can also surface them.
3. **Allow apps** that legitimately write: `Add-MpPreference -ControlledFolderAccessAllowedApplications "%ProgramFiles%\App\app.exe"` (Intune: allowed applications list). Microsoft-known good apps are allowed automatically.
4. Add protected folders (file shares mapped locally, project folders): `Add-MpPreference -ControlledFolderAccessProtectedFolders "<DATA_DIR>\Projects"`.
5. Enforce (`Enabled`) for pilot then broad; or "Block disk modification only" mode for minimal friction.

## Gotchas
- Line-of-business and developer tools, backup agents, sync clients writing to Documents get blocked; audit long enough to capture monthly jobs.
- Allowing by path: if the path is user-writable, malware can be placed there - allow only Program Files-type paths.
- Users see toast notifications for blocks; helpdesk must know the process.
- It protects local folders; ransomware encrypting network shares from another machine is not stopped.

## Checked
2026-10-28. Confirmed in the Controlled folder access enable and evaluate pages: `EnableControlledFolderAccess` modes (AuditMode, Enabled, BlockDiskModificationOnly), events 1123 (blocked) and 1124 (audited) in the Windows Defender Operational log. Removed: the advanced hunting query and the 2-4 week figure.
Method: documentation only; no commands were run.

## Verify
- [ ] Test with Microsoft's test tool / an unsigned script writing to Documents: blocked, event 1123 logged.
- [ ] Block rate per week low and investigated.
