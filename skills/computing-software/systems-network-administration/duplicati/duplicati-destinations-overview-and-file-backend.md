---
id: computing-software.systems-network-administration.duplicati.duplicati-destinations-overview-and-file-backend
name: duplicati-destinations-overview-and-file-backend
category: computing-software
field: systems-network-administration
product: duplicati
tags: [backup-destinations, destination-url, destination-timeouts, file-destination, use-move-for-put, separate-folder-per-backup]
level: practitioner
status: docs-checked
description: "Choose a Duplicati storage destination, pass its options in the URL, tune the shared timeouts and use the file destination efficiently."
sources: ["https://docs.duplicati.com/backup-destinations/destination-overview", "https://docs.duplicati.com/backup-destinations/standard-based-destinations/file-destination"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Duplicati destinations overview and the file destination

Duplicati stores backup data at a destination (backend). Where a provider offers both a generic protocol and a specific implementation, the provider-specific one is usually the better pick. Options are best given in the URL-like destination string, for example `&use-ssl=true`, but can also be passed as regular command-line options. Each backup must have its own folder; two backups sharing a destination folder keep breaking each other.

Categories:
- Duplicati Storage: integrated with the Duplicati Console, needs no configuration but a console-connected machine.
- Standard based: file path, S3-compatible, FTP, SFTP (SSH), WebDAV, OpenStack, Rclone (needs the binary) and SMB (CIFS, Windows shares).
- Provider specific: for example Backblaze B2 and Amazon S3, built on the provider's API or libraries.

Shared timeouts guard against a stalled connection: `--short-timeout` (30s; deleting a file, creating a folder), `--list-timeout` (10m; listing) and `--read-write-timeout` (30s; reset whenever data moves, so it fires only after inactivity; not supported by the Rclone destination).

File destination: stores backups anywhere reachable by the filesystem, such as a fixed disk, removable media or a mounted network share (use the SMB destination for Windows shares). The URL is `file://` plus the path, for example `file:///path/to/backup` or `file://\\server\share\folder`; the prefix is optional but clarifies intent. By default Duplicati writes a temporary file then copies it, giving retries and progress. For speed on local filesystems set `--use-move-for-put` together with `--disable-streaming-transfers` so the OS moves the file. The length verification after copy can be turned off with `--disable-length-verification`.

## Checked

2026-11-04. Confirmed against the Destination overview and File Destination pages. Nothing removed.

Method: documentation only; no commands were run.
