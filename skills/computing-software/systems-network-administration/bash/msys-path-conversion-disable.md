---
id: computing-software.systems-network-administration.bash.msys-path-conversion-disable
name: msys-path-conversion-disable
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, msys-path-conversion-disable, msys-no-pathconv, shell-scripting]
level: advanced
status: draft
description: "Stop Git Bash and MSYS2 from rewriting Unix-looking arguments into Windows paths using MSYS_NO_PATHCONV and MSYS2_ARG_CONV_EXCL."
sources:
  - https://www.msys2.org/docs/filesystem-paths/
  - https://gitforwindows.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Disabling MSYS path conversion
**Goal:** pass `/path` style arguments to native Windows programs untouched.
```bash
MSYS_NO_PATHCONV=1 docker run -v /data:/data img      # Git for Windows: disable all conversion
export MSYS2_ARG_CONV_EXCL='*'                         # MSYS2: exclude all (or list prefixes)
MSYS2_ARG_CONV_EXCL='/c;/k' cmd //c dir                # exclude specific args
cmd //c echo hi                                        # double slash avoids /c conversion
cygpath -w /c/<DIR> ; cygpath -u '<DRIVE>:\<DIR>'      # explicit conversion
```
- Conversion applies when launching native (non-MSYS) programs: arguments that look like POSIX paths (`/foo`, `-I/foo`, `VAR=/foo:/bar`) are rewritten to a Windows-style path under the MSYS root.
- Typical casualties: docker `-v`, `kubectl exec -- /bin/sh`, `cmd /c`.
- Env var names differ: Git for Windows uses `MSYS_NO_PATHCONV`; MSYS2 documents `MSYS2_ARG_CONV_EXCL` and `MSYS2_ENV_CONV_EXCL`.
- Self-check: `MSYS_NO_PATHCONV=1 echo /tmp` vs without, using a native `.exe` that prints its args.
