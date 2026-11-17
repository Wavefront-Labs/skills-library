---
id: computing-software.systems-network-administration.duplicati.duplicati-sftp-destination
name: duplicati-sftp-destination
category: computing-software
field: systems-network-administration
product: duplicati
tags: [sftp-destination, ssh-key-authentication, ssh-fingerprint, host-key-pinning, ssh-agent, ssh-keyfile]
level: practitioner
status: docs-checked
description: "Back up over SFTP with Duplicati using password or key authentication and pin the SSH host key fingerprint to block man-in-the-middle attacks."
sources: ["https://docs.duplicati.com/backup-destinations/standard-based-destinations/sftp-ssh-destination"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# SFTP (SSH) destination

SFTP uses SSH through the SSH.NET library. The UI needs server, port, folder path and username, and usually a password or a private key in the advanced options.

URL: `ssh://<hostname>/<path>?auth-username=<user>&auth-password=<password>&ssh-fingerprint=<fingerprint>`. Give a non-standard port in the host (`ssh://hostname:2222/folder`). The path is absolute on the server (`ssh://hostname/backup` means `/backup`); set `--ssh-relative-path` to resolve it relative to the login folder, usually the user's home.

Keys: from Duplicati 2.2 pass a key file with `--ssh-keyfile=/path/to/key` or an inline key with `--ssh-key=` (URL-encoded, with the `sshkey://` prefix). In the UI you can drop the file or paste its contents. If the key is encrypted, supply its passphrase with `--auth-password`. With neither password nor key, a running `ssh-agent` is used automatically; `--ssh-disable-agent=true` stops that. On macOS the keychain is queried for the passphrase. Use a dedicated identity and key for the backup user so a compromise grants no more than needed.

Host key validation: on first connection Duplicati throws an error explaining how to trust the host and showing its fingerprint; pass it with `--ssh-fingerprint`. If the key changes you get a different message with the new key. `--ssh-accept-any-fingerprints=true` disables man-in-the-middle protection and should be used for testing only. In the UI the Test now button guides you through this.

Timeouts: the generic `--read-write-timeout` (30s) and related options guard against a malfunctioning server that would otherwise hang operations.

## Checked

2026-11-04. Confirmed against the SFTP (SSH) Destination page. Nothing removed.

Method: documentation only; no commands were run.
