---
id: computing-software.systems-network-administration.duplicati.duplicati-ftp-and-webdav-destinations
name: duplicati-ftp-and-webdav-destinations
category: computing-software
field: systems-network-administration
product: duplicati
tags: [ftp-destination, webdav-destination, ftp-encryption-mode, ftp-data-connection-type, accept-specified-ssl-hash, webdav-authentication]
level: practitioner
status: docs-checked
description: "Connect Duplicati to FTP and WebDAV servers, choosing connection and encryption modes, authentication methods and certificate pinning for self-signed servers."
sources: ["https://docs.duplicati.com/backup-destinations/standard-based-destinations/ftp-destination", "https://docs.duplicati.com/backup-destinations/standard-based-destinations/webdav-destination"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# FTP and WebDAV destinations

FTP is widely supported but is considered a legacy protocol with security issues, so prefer SFTP or another destination where you can. The UI needs server, port, path, username and password. URL: `ftp://<hostname>/<path>?auth-username=<user>&auth-password=<password>`; a non-standard port goes in the host.

FTP needs several connections per transfer. The default `AutoPassive` data mode suits most setups and leaves firewall configuration to the server; set `--ftp-data-connection-type` if it does not work. Encryption: `--ftp-encryption-mode` is `None` (default, unencrypted), `Implicit` (TLS from the start), `Explicit` (starts unencrypted and upgrades) or `Auto`, the most compatible but insecure since it continues unencrypted if the upgrade fails. `--ftp-ssl-protocols` limits accepted protocols; because of .NET naming, `None` there means use the system defaults.

WebDAV extends HTTP, so TLS and certificate verification work like websites. The UI needs server, path, username and password. URL: `webdav://<hostname>/<path>?auth-username=<user>&auth-password=<password>`, with the port in the host (`webdav://hostname:8080/path`). Authentication: Basic is the default and sends the password in plain text, so insecure without TLS; `--force-digest-authentication=true` uses Digest; `--integrated-authentication=true` works for some Windows hosts. Check your server's documentation for the supported method. Add `--use-ssl=true` for HTTPS.

Certificates for both: `--accept-specified-ssl-hash=<sha1>` trusts one self-signed certificate, a form of pinning (the UI Test now button offers to pin an untrusted certificate); `--accept-any-ssl-certificate` disables validation and is for testing only; `--ignore-revocation-failure` (2.4.0.0 and later) tolerates an offline revocation server.

## Checked

2026-11-04. Confirmed against the FTP Destination and WebDAV Destination pages. Nothing removed.

Method: documentation only; no commands were run.
