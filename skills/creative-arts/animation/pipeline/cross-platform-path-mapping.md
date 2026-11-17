---
id: creative-arts.animation.pipeline.cross-platform-path-mapping
name: cross-platform-path-mapping
category: creative-arts
field: animation
product: pipeline
tags: [path-mapping, storage, data-management, unc-paths, dirmap, deadline-path-mapping, relative-paths, windows-linux-mac, render-farm-paths]
level: advanced
status: draft
description: "Make scene files resolve on Windows, Linux and macOS: one logical root, OS-specific mounts, dirmap in Maya, Deadline path mapping, and relative paths in Blender/Nuke."
sources:
  - https://docs.thinkboxsoftware.com/products/deadline/10.3/1_User%20Manual/manual/cross-platform.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cross-platform path mapping

**Goal:** a file saved on a Windows workstation renders on a Linux farm node and opens on an artist's Mac,
without broken texture or reference paths.

## One logical root

Pick one root per storage volume and mount it consistently:
| OS | Mount |
|---|---|
| Windows | `<DRIVE>:\` (mapped drive) or `\\server\projects` |
| Linux | `/mnt/projects` |
| macOS | `/Volumes/projects` |
Store the mapping in one place (pipeline config / Ayon roots / environment `PROJECT_ROOT`).

## Per tool

- **Maya**: `dirmap` command at startup:
  `cmds.dirmap(en=True); cmds.dirmap(m=("<DRIVE>:/", "/mnt/projects/"))`; or use project-relative paths and
  environment variables in file paths (`$PROJECT_ROOT/assets/...`), which Maya expands.
- **Blender**: relative paths (`//textures/wood.png`) by default for files inside the project; for shared
  libraries use a path mapping step or File - External Data - Make Paths Relative.
- **Nuke**: Preferences "Path substitutions" or `nuke.addFilenameFilter()` in `init.py` to rewrite prefixes
  per OS.
- **Houdini**: use `$JOB`/`$HIP` variables in paths.
- **Deadline**: Repository Configuration - Mapped Paths (Windows/Linux/Mac replacements), applied to job
  files and, with supporting plugins, inside scene files.

## Rules

- Forward slashes everywhere; most DCCs accept them on Windows.
- Never let drive letters differ between machines; never use local user-profile paths for shared files
  (validators should reject them).
- Case sensitivity: Linux is case-sensitive; `Textures/` vs `textures/` breaks on the farm.

## Verify

Open a scene on each OS and on a farm node: File - missing files check reports none; render one frame on
Linux from a Windows-saved scene.
