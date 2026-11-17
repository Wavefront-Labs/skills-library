---
id: computing-software.systems-network-administration.kopia.kopia-repository-backends
name: kopia-repository-backends
category: computing-software
field: systems-network-administration
product: kopia
tags: [repository-create, s3, azure, b2, gcs, sftp, webdav, rclone, filesystem]
level: practitioner
status: docs-checked
description: "Create Kopia repositories on S3, Azure, B2, GCS, Google Drive, WebDAV, SFTP, rclone and local storage, with the required options."
sources: ["https://kopia.io/docs/repositories/", "https://kopia.io/docs/advanced/consistency/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Use `kopia repository create <type>` once, then `kopia repository connect <type>` on each client. The password you enter is the repository encryption password, separate from the storage credentials, and should not equal them.

- **S3 and S3-compatible**: `kopia repository create s3 --bucket=... --access-key=... --secret-access-key=...`. For non-AWS providers also set `--endpoint` and maybe `--region`. Supports object locking and storage classes.
- **Azure Blob**, **Backblaze B2** (`kopia repository create b2`), **Google Cloud Storage** (`gcs --bucket NAME`, optionally `--credentials-file`; GCS also works through the S3 engine at `storage.googleapis.com`).
- **Google Drive**: native support is experimental and behaves differently from Drive via rclone; pick one and do not mix them.
- **WebDAV**: `--url`, `--webdav-username`, `--webdav-password`.
- **SFTP**: `--path --host --username` with `--sftp-password` or `--keyfile`; possibly `--known-hosts`. If connection fails, add `--external` to use an external `ssh` process.
- **Rclone** (experimental): `kopia repository create rclone --rclone-exe=/path/to/rclone --remote-path=my-remote:/some/path`. Only Dropbox, OneDrive and Google Drive are documented as tested. Kopia runs rclone itself after the remote is configured.
- **Local or network-attached**: `kopia repository create filesystem --path /path/to/repository` for any readable directory such as a USB drive, SMB or SSHFS mount.

Some settings, such as actions, can be enabled only at creation from the command line. Kopia needs full POSIX semantics from a filesystem repository; the Consistency page recommends a mature local filesystem and avoiding emulated, layered or networked filesystems that may not be fully compliant.

## Checked

2026-11-03. Confirmed against the fetched Kopia docs pages: Repositories page (create and connect commands and options per backend, experimental Google Drive and rclone, tested rclone remotes, actions/locking only at CLI creation) and Consistency (POSIX recommendation). Removed or corrected: the unsupported claim that network filesystems 'commonly' corrupt, replaced with the page's recommendation.
Method: documentation only; no commands were run.
