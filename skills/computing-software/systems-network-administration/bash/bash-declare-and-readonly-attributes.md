---
id: computing-software.systems-network-administration.bash.bash-declare-and-readonly-attributes
name: bash-declare-and-readonly-attributes
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, declare-builtin, readonly, typeset, export-f, declare-p, variable-attributes]
level: practitioner
status: gated
description: "Use declare/typeset attributes (-r -i -l -u -x -a -A -n -g), readonly constants, declare -p for inspection and export -f to pass functions to child bash processes."
sources:
  - https://www.gnu.org/software/bash/manual/html_node/Bash-Builtins.html#index-declare
  - https://www.gnu.org/software/bash/manual/html_node/Bourne-Shell-Builtins.html#index-readonly
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# declare and readonly attributes

## Attributes
| Flag | Effect |
|---|---|
| `-r` | read-only (like `readonly`) |
| `-i` | integer: assignments evaluated arithmetically (`declare -i n; n=5*3` → 15) |
| `-l` / `-u` | lowercase / uppercase on assignment |
| `-x` | export to child environment |
| `-a` / `-A` | indexed / associative array |
| `-n` | nameref |
| `-g` | inside a function: create/modify a global |
| `-f` / `-F` | functions (with bodies / names only) |
| `+x` etc. | remove attribute |

```bash
readonly CONF_DIR=/etc/myapp          # constant; reassigning errors (and exits under set -e)
declare -u ENV_NAME=prod              # → PROD
declare -A limits=([cpu]=2 [mem]=4G)
declare -p limits                     # prints a re-usable definition — great for debugging and serialising state
declare -F                            # list function names
```

## Passing functions to subprocesses
```bash
log() { printf '%s %s\n' "$(date +%T)" "$*"; }
export -f log
find . -name '*.tmp' -exec bash -c 'log "removing $1"; rm -- "$1"' _ {} \;
parallel log ::: a b c                # GNU parallel picks up exported functions (gated: unconfirmed, source is paywalled or blocked; GNU parallel not installed here)
```
Exported functions travel in `BASH_FUNC_log%%` env vars — only bash children understand them (gated: unconfirmed, source is paywalled or blocked; no dash available here, and `sh` on this MSYS box is bash). The variable shows up in `env` as `BASH_FUNC_log%%=() { ... }` (run).

## Gotchas
- `-i` silently turns non-numeric strings into 0 (`n=abc` gave 0) or evaluates them as variable names (with `abc=7` it gave 7): avoid on untrusted input. Verified on bash 5.2.37.
- `readonly` can't be undone in the running shell; don't use it for things tests need to override.
- `declare` inside a function makes a local unless `-g`.

## Verify
- [ ] `declare -p VAR` shows expected attributes; `bash -c 'type log'` works after `export -f`.
