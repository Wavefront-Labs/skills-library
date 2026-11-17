---
id: computing-software.general-digital-literacy.file-management.mapping-a-network-drive
name: mapping-a-network-drive
category: computing-software
field: general-digital-literacy
product: file-management
tags: [file-management, file-explorer, map-network-drive, connect-to-server, smb, nas]
level: intro
status: docs-checked
description: "Map a shared folder as a drive in Windows File Explorer and use Connect to Server on a Mac to reach shared computers and NAS devices."
sources:
  - https://support.microsoft.com/en-us/windows/map-a-network-drive-in-windows-10-29ce55d1-34e3-a7e2-4801-131475f9557d
  - https://support.apple.com/guide/mac-help/connect-mac-shared-computers-servers-mchlp1140/mac
  - https://support.apple.com/en-us/102650
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Map a network drive and connect to a server

## Windows
1. File Explorer > This PC > More (three dots) > **Map network drive** (also in the right-click menu on This PC).
2. Pick a drive letter and enter the folder path (for example the share on your NAS) or browse to it.
3. Tick the option to reconnect at sign-in.
- If it fails, the target computer may be off, or you may lack permission: ask the network administrator.

## Mac
1. Finder > Go > **Connect to Server** (`Command+K`), type the network address in the Server Address field and click Connect. Servers using protocols such as SMB are supported.
2. Choose Guest, Registered User or Apple Account as the connection type, enter credentials if asked, and select the shared folder or volume.
3. To browse instead, click **Network** under Locations in the Finder sidebar and double-click the computer.

## Verify
- [ ] The share opens in File Explorer or the Finder and files are readable.

## Checked
Date: 2026-10-27. Documentation: Microsoft Support "Map a network drive in Windows" (summary via Microsoft search result, direct fetch blocked) and Apple Mac User Guide "Connect your Mac to shared computers and servers" plus keyboard shortcuts (macOS 27 / Tahoe 26, 2026). Removed unconfirmed claims: net use commands, credential and error-message fixes, SMB1 advice, keychain and Login Items steps, address examples.
Method: documentation only; no commands were run.
