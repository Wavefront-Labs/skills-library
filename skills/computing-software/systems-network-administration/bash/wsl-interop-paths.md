---
id: computing-software.systems-network-administration.bash.wsl-interop-paths
name: wsl-interop-paths
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, wsl-interop-paths, wslpath, shell-scripting]
level: practitioner
status: draft
description: "Convert and share paths between WSL and Windows from bash with wslpath, /mnt/c and Windows executables, plus line-ending traps."
sources:
  - https://learn.microsoft.com/en-us/windows/wsl/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# WSL wslpath and Windows interop
**Goal:** mix Linux and Windows tools in scripts.
```bash
wslpath -u '<DRIVE>:\<DIR>\file.txt'    # /mnt/<drive>/<DIR>/file.txt
wslpath -w ~/project                  # \\wsl$\Ubuntu\home\me\project   (name varies)
wslpath -m ~/x                        # mixed C:/ style
explorer.exe .                        # open current dir in Explorer
powershell.exe -NoProfile -Command 'Get-Date'
cmd.exe /c echo %USERPROFILE%
```
- Windows programs print CRLF: strip with `| tr -d '\r'` before using values in bash.
- Files under `/mnt/c` are slow and have no real Unix permissions (unless metadata mounts are on); keep projects in the Linux filesystem.
- Fix script line endings with `dos2unix` or `git config core.autocrlf input`.
- `/etc/wsl.conf` controls automount and interop; check `$WSL_DISTRO_NAME`.
- Self-check: `wslpath -w "$PWD"` round-trips with `wslpath -u`.
