---
id: computing-software.cloud-infrastructure-engineering.docker.desktop-bind-mount-ownership-on-wsl-and-macos
name: desktop-bind-mount-ownership-on-wsl-and-macos
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, docker-desktop, wsl-mount-permissions, mac-file-ownership, bind-mount-permissions, virtiofs, wsl2, drvfs, file-permissions, chmod]
level: practitioner
status: docs-checked
description: "Why bind-mount permissions behave differently on Docker Desktop: Windows shares fixed at 0777, WSL filesystem placement, macOS VirtioFS and case-insensitivity, and the fixes."
sources: ["https://docs.docker.com/desktop/troubleshoot-and-support/troubleshoot/topics/", "https://docs.docker.com/desktop/features/wsl/best-practices/", "https://docs.docker.com/desktop/settings-and-maintenance/settings/", "https://learn.microsoft.com/en-us/windows/wsl/file-permissions", "https://learn.microsoft.com/en-us/windows/wsl/wsl-config"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Desktop bind-mount permissions on WSL and macOS

Docker Desktop runs containers in a Linux VM; host folders reach it through a file-sharing
layer. Behaviour depends on **where the files live**.

## Windows
- Sharing files from Windows: Desktop sets permissions on shared volumes to a default of
  `0777`, and the docs state these defaults are **not configurable**. So `chmod` inside the
  container will not give you restrictive modes on a Windows-path bind mount. The docs'
  fixes: use a non-host-mounted (named) volume, or make the application work with the default
  permissions.
- Docker's WSL best practice: keep bind-mounted source and data **in the Linux filesystem**
  (`docker run -v ~/my-project:/sources <image>`), not under `/mnt/c`. Reasons given:
  much higher performance, and Linux containers only receive file-change (inotify) events
  when the files live in the Linux filesystem, which breaks auto-reload workflows otherwise.
- Line endings: Windows `\r\n` in shell scripts makes `docker run` fail with syntax errors.
  Convert with `dos2unix script.sh` or set the editor to LF.
- In WSL itself, Windows drives mounted without metadata get permissions derived from the
  Windows user's effective rights, applied identically to user, group and other. Metadata is
  disabled by default; enable it in `/etc/wsl.conf`:
  ```ini
  [automount]
  options = "metadata,uid=1000,gid=1000,umask=022"
  ```
  `uid`, `gid`, `umask` and `fmask` only apply when the drive is mounted with metadata. This
  governs WSL processes; Docker documents the 0777 default for what Desktop presents on shares.

## macOS
- File sharing implementation: **VirtioFS** (default) or gRPC FUSE, selectable in Settings
  when using the Apple Virtualization framework VMM.
- Mac file systems are case-insensitive by default while Linux is case-sensitive, so
  `test` and `Test` are one file on the Mac and an app can pass locally and fail in Linux CI.
- Projects outside your home directory need file sharing enabled (Settings, Resources, File
  sharing); otherwise you see "file not found" or "access denied" on mounts. On Windows the
  setting is under Shared Folders.

## Rules of thumb
1. Databases and anything permission-sensitive: **named volumes**, not Windows-path binds.
2. Source code: Linux filesystem inside WSL on Windows.
3. Native Linux Docker Engine does no uid mapping (see the matching-host-uids skill).

## Verify
```bash
docker run --rm -v "$PWD":/w alpine sh -c 'touch /w/t && ls -ln /w/t && chmod 600 /w/t && ls -ln /w/t'
# Windows share: stays 777 per the documented default; compare with a path in the WSL filesystem
```

## Checked
Date: 2026-10-26. Documentation: docker/docs main (last commit 2026-10-23) troubleshooting
topics, WSL best practices, Settings; MicrosoftDocs/WSL file-permissions and wsl-config pages.
Confirmed: 0777 non-configurable default, WSL filesystem placement and inotify reasoning,
dos2unix fix, DrvFs metadata default and `automount options`, VirtioFS/gRPC FUSE, macOS
case-insensitivity, file-sharing requirement. Removed as unconfirmed: container-visible
owner mapping on macOS and Linux Desktop, specific app error strings, `safe.directory`
advice, "WSL ext4 keeps real uid/gid" table row, "chown in entrypoint is slow" claim.
Method: documentation only; no commands were run.
