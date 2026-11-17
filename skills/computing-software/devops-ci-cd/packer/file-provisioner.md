---
id: computing-software.devops-ci-cd.packer.file-provisioner
name: file-provisioner
category: computing-software
field: devops-ci-cd
product: packer
tags: [file, upload, download, destination, prov-file]
level: practitioner
status: docs-checked
description: "Upload or download files with the file provisioner, including directory trailing-slash rules and root-owned destinations."
sources:
  - "https://developer.hashicorp.com/packer/docs/provisioners/file/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The `file` provisioner uploads files to machines built by Packer (and downloads with `direction = "download"`). The recommended workflow is to upload with `file`, then use the `shell` provisioner to move files into place and set permissions.

```hcl
provisioner "file" {
  source      = "app.tar.gz"
  destination = "/tmp/app.tar.gz"
}
provisioner "file" {
  content     = "hello"
  destination = "/tmp/hello.txt"
}
```

Options:

- `source` is a local file or directory path, absolute or relative to the working directory Packer runs in. Mandatory unless `sources` is set.
- `sources` is a list used instead of `source`; the destination must then be a directory with a trailing slash, and all files keep their names.
- `destination` is required. It must be a writable location and its parent directories must already exist. If the file already exists it is overwritten.
- `content` is text to write to `destination`; if `destination` is a directory a file named `pkr-file-content` is created. It cannot be combined with `source` or `sources`.
- `direction` is `upload` (default) or `download`; with `download` the file `source` on the machine is downloaded locally to `destination`.
- `generated` (advanced, not recommended): if true, existence of the source is checked just before upload instead of at pre-build validation, so files created during the run can be uploaded.

Directory rules:

- The destination directory must already exist; otherwise the provisioner may succeed with undefined results. Create it with a shell provisioner just before.
- Source `/foo/` (trailing slash) with destination `/tmp` uploads the contents of `/foo` directly into `/tmp`.
- Source `/foo` (no trailing slash) with destination `/tmp` uploads the contents to `/tmp/foo`, which Packer creates.
- This follows rsync behaviour. Packer does not infer behaviour from the guest OS, so use a trailing forward slash for directories even on Windows guests.
- If the destination is a directory, end it with a trailing slash so Packer uses the source basename.

You can only upload to locations the provisioning user (generally not root) can access; otherwise you get "Permission Denied". Creating files in `/tmp` and moving them with a shell provisioner is the only way to reach root-owned locations:

```hcl
provisioner "shell" {
  inline = ["sudo mv /tmp/app.conf /etc/app.conf"]
}
```

Other documented behaviours:

- Symlinks: the Docker communicator preserves them; other communicators treat local symlinks as regular files. Use `tar` to preserve them.
- Large transfers over WinRM can be very slow; consider an SSH server and the ssh communicator.

## Checked

Method: docs-checked 2026-11-09 against the Packer file provisioner page and its generated required and optional configuration reference (both read in full as published page source).
