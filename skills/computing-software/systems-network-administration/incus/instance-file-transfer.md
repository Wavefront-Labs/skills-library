---
id: computing-software.systems-network-administration.incus.instance-file-transfer
name: instance-file-transfer
category: computing-software
field: systems-network-administration
product: incus
tags: [incus, file, push, pull, edit, delete, recursive, incus-agent]
level: intro
status: docs-checked
description: "Copy and edit files in Incus instances with incus file pull, push, edit and delete, including recursive transfers and piping to stdout."
sources:
  - https://raw.githubusercontent.com/lxc/incus/main/doc/howto/instances_access_files.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Instance file transfer

```
incus file edit <instance>/<path_to_file>
incus file delete <instance>/<path_to_file>
incus file pull <instance>/<path_to_file> <local_file_path>
incus file pull my-instance/var/log/syslog - | less
incus file pull -r <instance>/<dir> <local_location>
incus file push <local_file_path> <instance>/<path_to_file>
incus file push -r <local_location> <instance>/<dir>
```

- `edit` needs the file to exist already.
- A `-` as the pull target writes to stdout.
- Containers: always works, handled directly by Incus.
- Virtual machines: the `incus-agent` process must be running inside the VM.

## Checked

2026-11-04: confirmed against the Incus access-files how-to (edit, delete, pull, push, recursive flag, stdout pull, container and VM requirements). Nothing removed.

Method: documentation only; no commands were run.
