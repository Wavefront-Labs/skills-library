---
id: computing-software.devops-ci-cd.nomad.logs-block
name: logs-block
category: computing-software
field: devops-ci-cd
product: nomad
tags: [nomad, log-rotation, logs, max-files, max-file-size, stdout, stderr, disable-log-collection, alloc-logs, hcl]
level: practitioner
status: docs-checked
description: "Control Nomad task log rotation with the logs block including max_files, max_file_size, disabled, rotated file naming and the ephemeral disk size validation rule."
sources: ["https://github.com/hashicorp/web-unified-docs/blob/main/content/nomad/v1.10.x/content/docs/job-specification/logs.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nomad logs block (log-rotation)

Nomad captures a task's stdout and stderr into files under the allocation's `alloc/logs/` directory named `<task-name>.<stdout|stderr>.<index>`. Writing starts at index 0; when a file reaches `max_file_size` a new index begins. Files are never rolled over in place: once more than `max_files` exist, the lowest index is deleted. Logging is on by default, so an empty configuration is normal.

```hcl
task "server" {
  logs {
    max_files     = 10
    max_file_size = 10
    disabled      = false
  }
}
```

## Parameters (defaults)
- `max_files` (`10`) - retained rotated files **per stream**; `2` means 4 files total (2 stdout, 2 stderr).
- `max_file_size` (`10`) - size in MB of each file. If the task's requested disk is smaller than `max_files` times `max_file_size` for both streams, job submission fails with a validation error.
- `disabled` (`false`) - when `true` the driver attaches output to `/dev/null` (`NUL` on Windows). Do this only if the app logs elsewhere (for example remote syslog). Afterwards `nomad alloc logs` and the log APIs return 404.

## Sizing example
`max_files = 3`, `max_file_size = 5` needs at least 30 MB (3 stderr plus 3 stdout, 5 MB each).

## Gotchas
- Logs live on the group's ephemeral disk, so raising log retention may require a larger `ephemeral_disk` size (`computing-software.devops-ci-cd.nomad.ephemeral-disk-block`).
- Some drivers, such as docker, have `disable_log_collection`; if set to `true` it overrides `disabled = false` here.
- Read logs with `computing-software.devops-ci-cd.nomad.alloc-logs`.

## Checked

2026-11-03. Confirmed against the Nomad 1.10 logs job specification page: file naming and rotation, max_files, max_file_size, disabled and the 404 effect, disable_log_collection override, the 30 MB example, ephemeral disk note. Nothing removed.

Method: documentation only; no commands were run.
