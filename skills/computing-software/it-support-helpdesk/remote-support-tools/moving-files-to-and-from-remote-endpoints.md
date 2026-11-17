---
id: computing-software.it-support-helpdesk.remote-support-tools.moving-files-to-and-from-remote-endpoints
name: moving-files-to-and-from-remote-endpoints
category: computing-software
field: it-support-helpdesk
product: remote-support-tools
tags: [it-support-helpdesk, remote-support-tools, remote-file-transfer, scp, sftp, copy-item, admin-share, file-transfer]
level: practitioner
status: draft
description: "Move files to and from remote endpoints safely: PowerShell session copy, admin shares, scp/sftp, RMM and remote-tool file managers, resumable copies and hash checks."
sources:
  - "https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/copy-item"
  - "https://man.openbsd.org/scp"
  - "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/robocopy"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# moving-files-to-and-from-remote-endpoints

## Pick the channel already open
| Channel | Command / place |
|---|---|
| PowerShell remoting | `$s = New-PSSession PC01; Copy-Item .\tool.zip -Destination '<SUPPORT_DIR>' -ToSession $s` (and `-FromSession` to fetch) |
| Admin share (LAN, admin rights) | `robocopy .\src \\PC01\C$\ProgramData\Support /Z /J /R:2 /W:5` |
| SSH | `scp file admin@host:/tmp/`, `sftp admin@host` for browsing |
| Remote tool | TeamViewer/AnyDesk/RMM file manager while in session |
| RMM / Intune | Package as a Win32 app or RMM script attachment for anything sent to many devices |

`<SUPPORT_DIR>` is a path on the remote machine, e.g. a Support folder under ProgramData.

## Large or flaky transfers
- `robocopy /Z` restartable mode and `/J` unbuffered I/O for large files.
- Split or compress logs first: `Compress-Archive` on the remote end, then copy one file.
- BITS (`Start-BitsTransfer`) resumes across network drops for downloads.

## Integrity and handling
- Hash both ends: `Get-FileHash file -Algorithm SHA256` (Windows), `shasum -a 256` (macOS),
  `sha256sum` (Linux).
- Stage in a support folder (e.g. under ProgramData), never on the user's desktop, and
  delete after use.
- User data or logs with personal data leave the device only under your data-handling
  policy; record what was copied in the ticket.

## Gotchas
- Admin shares are often disabled or firewalled on laptops; PowerShell session copy works
  over WinRM alone.
- Double-hop: from a remote session you cannot reach a third file server with your
  credentials (Kerberos double hop); copy to your machine first.
- Antivirus may quarantine diagnostic tools on arrival; use signed tools.

## Verify
Hashes match, the file is in the intended folder with expected permissions, and
temporary copies are removed at session end.
