---
id: computing-software.systems-network-administration.duplicati.duplicati-smb-destination
name: duplicati-smb-destination
category: computing-software
field: systems-network-administration
product: duplicati
tags: [smb-destination, cifs-destination, smb-transport, directtcp, netbios, auth-domain]
level: practitioner
status: draft
description: "Back up to Windows and other SMB shares with Duplicati using the smb URL, domain credentials and the DirectTCP or NetBIOS transport."
sources: ["https://docs.duplicati.com/backup-destinations/standard-based-destinations/cifs-aka-smb-destination"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# SMB (CIFS) destination

The SMB backend gives native access to Windows shares and other SMB-compatible network resources. Use `smb://`; `cifs://` is deprecated and kept only for existing configurations. The UI needs server, share name, path, username, password and transport.

URL: `smb://<hostname>/<share>/<path>?auth-username=<user>&auth-password=<password>&transport=directtcp`. If the account belongs to a Windows domain, enter the domain in the UI or add `&auth-domain=<domain>`.

Transport:
- `directtcp`: port 445, faster, modern, lower overhead, preferred for newer systems.
- `netbios`: port 139, legacy, compatible with older systems, extra overhead and slower, uses the NetBIOS naming service.

The share name is the first path segment after the host, so in `smb://fileserver/backups/laptop` the share is `backups` and the backup folder is `laptop`. Each backup needs its own folder, as with every destination. SMB is the preferred choice over the file destination for Windows network shares, since Duplicati then authenticates itself instead of relying on a mounted drive.

Advanced options include `--read-buffer-size` and `--write-buffer-size` in bytes for SMB operations; they are capped by the negotiated SMB values and values below 10000 bytes are ignored.
