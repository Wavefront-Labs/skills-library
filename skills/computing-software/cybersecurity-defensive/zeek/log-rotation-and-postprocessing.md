---
id: computing-software.cybersecurity-defensive.zeek.log-rotation-and-postprocessing
name: log-rotation-and-postprocessing
category: computing-software
field: cybersecurity-defensive
product: zeek
tags: [cybersecurity-defensive, zeek, log-rotation, rotation-interval, postprocessor, zeek-archiver]
level: practitioner
status: docs-checked
description: "Control Zeek log rotation: Log::default_rotation_interval, per-filter interv, rotation_format_func naming, and rotation postprocessor commands with their six arguments."
sources: ["https://docs.zeek.org/en/current/frameworks/logging.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# log rotation and postprocessing

Rotation renames an active log (for example `conn.log` to `conn_21-01-03_14-05-00.log`) and starts a fresh one. Set the interval globally with `Log::default_rotation_interval` (default 0secs disables it) or per filter via `interv`:

```
local f = Log::get_filter(Conn::LOG, "default");
f$interv = 1 min;
Log::add_filter(Conn::LOG, f);
```

Under ZeekControl the option is set from its configuration.

**Naming**: the redef-able `Log::rotation_format_func` receives a `Log::RotationFmtInfo` and returns a `Log::RotationPath` with output directory and base name. The directory defaults to `Log::default_rotation_dir` (or `Log::default_logdir` if that is in use), and the timestamp format comes from `Log::default_rotation_date_format`.

**Postprocessing**: if `Log::default_rotation_postprocessor_cmd` is set, `Log::run_rotation_postprocessor_cmd` runs it on each rotated log with six extra arguments: the rotated file name, original base name, creation timestamp, rotation timestamp, 1 if Zeek is terminating (else 0), and the writer name.

Zeek ignores non-zero exit codes of the shell command. A custom postprocessor function that returns F makes that log writer instance shut down, so do that only when the writer cannot continue. Zeek ships SCP and SFTP postprocessors, and the project provides `zeek-archiver` for compression outside the Zeek process.

## Checked

2026-11-04: read against the official Zeek documentation page(s) listed in sources; the claims, names, values and examples in this skill match the page text. Nothing else was added.

Method: documentation only; no commands were run.
