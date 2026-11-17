---
id: computing-software.systems-network-administration.bash.shebang-posix-sh-dash
name: shebang-posix-sh-dash
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, shebang-posix-sh-dash, sh-vs-bash, shell-scripting]
level: practitioner
status: draft
description: "Decide between #!/bin/sh and #!/usr/bin/env bash for scripts, and what breaks when sh is dash or busybox ash."
sources:
  - https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html
  - https://www.gnu.org/software/bash/manual/bash.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Choosing /bin/sh versus bash in the shebang
**Goal:** pick the interpreter that matches the syntax used.
```bash
#!/bin/sh              # POSIX only: portable, faster startup (dash), minimal containers
#!/usr/bin/env bash    # bash features: arrays, [[ ]], process substitution, find bash on PATH
#!/bin/bash            # fixed path: fine on Linux, absent on NixOS/some BSDs
```
- Debian/Ubuntu `sh` is dash; Alpine `sh` is busybox ash; RHEL/macOS `sh` is bash in POSIX mode (macOS bash is 3.2).
- A `.sh` extension says nothing: the shebang decides, and `sh script.sh` ignores the shebang and uses sh.
- Declaring `#!/bin/sh` but using bashisms is the commonest portability bug; test with `dash -n` and `checkbashisms`.
- Alpine/distroless images may have no bash: install it or write POSIX.
- Self-check: `shellcheck` picks the dialect from the shebang and flags SC2039/SC3xxx issues.
