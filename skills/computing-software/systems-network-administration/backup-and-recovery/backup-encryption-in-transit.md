---
id: computing-software.systems-network-administration.backup-and-recovery.backup-encryption-in-transit
name: backup-encryption-in-transit
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [encryption-in-transit, tls, backup-encryption]
level: practitioner
status: docs-checked
description: "Encrypt backup traffic in transit with restic: rest and s3 over HTTPS, certificate verification and --cacert, SFTP over SSH, and rclone."
sources:
  - https://restic.readthedocs.io/en/stable/030_preparing_a_new_repo.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Encryption in transit for backups (restic)

**Goal:** backup data crossing networks (LAN segments, WAN, internet) cannot be read or tampered with.

## Choose the transport
- **REST server**: use the `rest:https://` scheme, not `rest:http://`. Depending on your REST server setup you can use HTTPS, a unix socket, password protection and multiple repositories. Set the server username and password with `RESTIC_REST_USERNAME` and `RESTIC_REST_PASSWORD` rather than putting them in the URL.
- **S3 and S3-compatible storage**: for a non-Amazon server, specify the URL as `s3:https://server:port/bucket_name`.
- **SFTP**: `sftp:user@host:/srv/restic-repo` runs over SSH. SFTP servers close connections when no data is received by the client, which can happen while restic processes large amounts of unchanged data; the restic page suggests `ServerAliveInterval 60` and `ServerAliveCountMax 240` in the client's `.ssh/config`.
- **rclone**: `rclone:<remote>:<path>`; restic starts and stops rclone. With a remote rclone over SSH, all data except credentials is encrypted and decrypted locally.

## TLS certificate checks
With TLS, restic verifies the server certificate against the system's CA certificates and refuses to proceed with an error if verification fails. For a self-signed or custom CA, pass the certificate file with `--cacert`; the system CA certificates are then not considered at all.

## Verify
Confirm the repository URL scheme in your scripts is `rest:https`, `s3:https` or `sftp`, and that a deliberate bad certificate makes restic exit with an error. A packet capture of a job (for example with tcpdump) is a further check that no readable file contents cross the wire.

## Checked

2026-11-09. Confirmed against the restic "Preparing a new repository" page (REST server schemes and TLS verification, `--cacert`, S3-compatible URL form, SFTP keep-alive settings, rclone backend). Removed (not on the cited page): all Veeam network traffic rules, Bacula/Bareos TLS directives and TLS-PSK default, Hyper-V Replica and storage replication claims, IPsec advice, the claim that restic's TLS "adds transport integrity", and the tcpdump command line.

Method: documentation only; no commands were run.
