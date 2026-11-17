---
id: computing-software.systems-network-administration.bash.shell-git-bash-and-msys-on-windows
name: shell-git-bash-and-msys-on-windows
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, sh-git-bash, msys2, windows-paths, cygpath, wsl]
level: practitioner
status: draft
description: "Run shell scripts on Windows with Git Bash/MSYS2 or WSL and handle path translation, line endings and tool differences."
sources: ["https://www.gnu.org/software/bash/manual/", "https://pubs.opengroup.org/onlinepubs/9799919799/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Shell on Windows

- Git Bash and MSYS2 give a POSIX shell on Windows: a drive path appears as `/c/dir`; convert with `cygpath -u "$WINPATH"` (to POSIX) and `cygpath -w /c/dir` (to Windows). Use forward slashes in scripts.
- MSYS rewrites arguments that look like POSIX paths when calling native Windows programs (`/c/foo` becomes a Windows drive path, and `/?` style switches may be mangled). Disable per command with `MSYS_NO_PATHCONV=1` (Git for Windows) or `MSYS2_ARG_CONV_EXCL='*'`.
- Line endings: configure `core.autocrlf` and `.gitattributes` (`*.sh text eol=lf`), or scripts fail with `\r` errors.
- Symlinks need `MSYS=winsymlinks:nativestrict` and Developer Mode or admin; processes and signals are emulated, so `kill`, `fork` heavy loops and `ps` behave differently and are slow.
- WSL runs a real Linux; access Windows files under `/mnt/c` (slower I/O, no Unix permissions by default); run Windows executables from WSL by name with `.exe`; keep repos inside the Linux filesystem for speed.
- PowerShell is the native Windows automation shell; use it for registry, services and Windows-only APIs, and shell for portable text pipelines.
