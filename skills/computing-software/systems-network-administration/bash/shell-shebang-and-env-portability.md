---
id: computing-software.systems-network-administration.bash.shell-shebang-and-env-portability
name: shell-shebang-and-env-portability
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, sh-shebang, env-bash, script-permissions, line-endings, crlf]
level: intro
status: draft
description: "Write a correct shebang, make scripts executable and avoid CRLF and PATH portability pitfalls."
sources: ["https://www.gnu.org/software/bash/manual/", "https://pubs.opengroup.org/onlinepubs/9799919799/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Shebang and portability

- First line `#!/bin/sh` for POSIX-only scripts; `#!/usr/bin/env bash` finds bash on PATH (needed on macOS, NixOS, BSD, where bash is not in `/bin`). The kernel passes only one argument on the shebang line on Linux (`#!/usr/bin/env -S bash -e` needs GNU env 8.30+ `-S`).
- `chmod +x script.sh` and track the executable bit in git (`git update-index --chmod=+x`).
- Windows line endings (CRLF) cause `bad interpreter: /bin/bash^M` or `$'\r': command not found`. Fix with `dos2unix`/`sed -i 's/\r$//'` and enforce LF with `.gitattributes` (`*.sh text eol=lf`).
- A script run as `sh script.sh` ignores the shebang's interpreter; `bash script.sh` ignores `sh`-ness.
- macOS ships bash 3.2 and BSD userland (`sed -i ''`, `date -d` missing, no `readlink -f` before macOS 12.3): use `#!/usr/bin/env bash` with Homebrew bash, or stay POSIX.
- Use `#!/bin/sh` only if the script is truly POSIX (check with `shellcheck -s sh`, `checkbashisms`, and run under `dash`).
