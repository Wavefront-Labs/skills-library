---
id: computing-software.cybersecurity-defensive.falco.fs-path-fields
name: fs-path-fields
category: computing-software
field: cybersecurity-defensive
product: falco
tags: [fs-path, fs-path-name, fs-path-source, fs-path-target, file-paths]
level: advanced
status: docs-checked
description: "Use the fs.path.* fields (Falco 0.36 and later) to read file paths consistently across syscalls, with raw variants and limits."
sources:
  - https://falco.org/docs/concepts/rules/fspath/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Syscalls expose file paths under different arguments such as `evt.rawarg.path` or `evt.rawarg.pathname`. Falco 0.36 added the `fs.path.*` fields to normalise them.

Fields:
- `fs.path.name`: for operations on a single path such as open, unlink and rmdir.
- `fs.path.source` and `fs.path.target`: for operations with two paths, such as cp, symlink, link and mv.
- `fs.path.nameraw`, `fs.path.sourceraw`, `fs.path.targetraw`: the original path text, which may be relative.

The non-raw fields convert relative paths to absolute using the thread's current working directory.

Limits:
- They are populated only for syscalls that read, write or modify a file system object and take a path argument.
- They work only for exit events and return a value only if the syscall succeeds.
- Other path fields remain separate, such as `proc.exepath`, `proc.pexepath`, `proc.aexepath` and the `container.mount.*` fields.

Several event identifiers can map to one syscall (for example MKDIR and MKDIR_2), because older libs defined a new event when arguments changed.

The docs example rule watches paths under a list with `fs.path.name pmatch (file_operation_paths) or fs.path.source pmatch (file_operation_paths) or fs.path.target pmatch (file_operation_paths)`, combined with a macro of file operations such as `mkdir or rename or remove or open_write or create_symlink`.

Mapping notes: the fields draw on different underlying arguments per syscall (for example `evt.rawarg.path` for mkdir, `evt.rawarg.name` for open, `fd.name` for fchmod and fchown). For link and symlink, `fs.path.source` is the new link name and `fs.path.target` the existing path, whereas for rename `source` is the old path; check the mapping tables before relying on direction.

Gotcha: the fields return nothing for failed syscalls or enter events.

## Checked

2026-11-08. Read the fs.path page in full including mapping tables. Replaced an invented example condition and an unsupported fd.name gotcha with the documented example and mapping notes, including the reversed source/target for link and symlink.

Method: documentation only; no commands were run.
