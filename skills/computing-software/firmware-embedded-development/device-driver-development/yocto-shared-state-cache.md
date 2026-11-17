---
id: computing-software.firmware-embedded-development.device-driver-development.yocto-shared-state-cache
name: yocto-shared-state-cache
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [sstate-cache, yocto, sstate-mirrors, hash-equivalence, build-speed, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Speed up Yocto builds with shared state: SSTATE_DIR and SSTATE_MIRRORS for CI and developers, hash equivalence servers, DL_DIR mirrors, and diagnosing unexpected rebuilds."
sources:
  - https://docs.yoctoproject.org/overview-manual/concepts.html#shared-state-cache
  - https://github.com/openembedded/bitbake/blob/master/doc/bitbake-user-manual/bitbake-user-manual-ref-variables.rst
  - https://github.com/openembedded/openembedded-core/blob/master/meta/conf/bitbake.conf
  - https://github.com/openembedded/openembedded-core/blob/master/scripts/sstate-cache-management.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Shared state cache

BitBake stores the output of each task, keyed by a signature hash of its inputs, in the shared
state (sstate) cache. A clean build that finds matching sstate objects restores them instead of
recompiling.

## Configuration (site.conf or local.conf)
```bitbake
DL_DIR     = "/srv/yocto/downloads"         # source tarballs and git mirrors, share across builds
SSTATE_DIR = "/srv/yocto/sstate-cache"      # local cache directory
SSTATE_MIRRORS ?= "file://.* https://sstate.acme.example/scarthgap/PATH;downloadfilename=PATH"
BB_HASHSERVE = "auto"                        # local hash equivalence server (the OE-Core default)
BB_HASHSERVE_UPSTREAM = "hashserv.acme.example:8687"   # optional: local server queries this upstream one
# BB_SIGNATURE_HANDLER defaults to "OEEquivHash" in OE-Core; no need to set it
```
- CI builds populate the cache (write access to SSTATE_DIR, then sync to an HTTP server).
- Developers read via `SSTATE_MIRRORS` (read-only), keeping their own local `SSTATE_DIR`.
- Keep one cache per Yocto release, as in the `SSTATE_MIRRORS` URL above.
- Source mirrors: `BB_GENERATE_MIRROR_TARBALLS = "1"` in CI, `PREMIRRORS` / `own-mirrors` class for
  developers, `BB_NO_NETWORK = "1"` to prove the mirror is complete.

## Hash equivalence
Some changes alter a task's signature without changing its output (a comment in a recipe, a
dependency rebuilt identically). With hash equivalence the server records "these two hashes
produced the same output", and downstream tasks are reused instead of rebuilt.

## Why did this rebuild?
```sh
bitbake -S none acme-image                      # dump signature data without printing a diff
bitbake-diffsigs -t busybox do_compile          # compare the last two signatures of a task
bitbake-dumpsig tmp/stamps/.../busybox/*.do_compile.sigdata.*
```
Common culprits: variables with timestamps or absolute paths leaking into tasks, `DATE`/`TIME`
in a recipe, machine-specific variables in recipes that should be `allarch`, local patches with
changing content, `BB_BASEHASH_IGNORE_VARS` missing entries.

## Housekeeping
- `scripts/sstate-cache-management.py --remove-duplicated --cache-dir=<dir>` (`-d` is the short form) keeps only
  the newest sstate file of each package; `--stamps-dir` keeps only what given build directories use.
- Never share `TMPDIR` between builds; share DL_DIR and SSTATE_DIR only.
- `rm_work` class saves disk in CI (`INHERIT += "rm_work"`).

## Verify
- [ ] Fresh checkout on a developer machine: `bitbake acme-image` reports most tasks as "setscene" (restored from sstate).
- [ ] `bitbake-diffsigs` explains any unexpected rebuild after a no-op change.

## Checked

2026-10-27, BitBake and OpenEmbedded-Core master.
Confirmed in bitbake.conf: BB_SIGNATURE_HANDLER ?= "OEEquivHash", BB_HASHSERVE ??= "auto". Confirmed in the BitBake user manual variable reference: BB_HASHSERVE, BB_HASHSERVE_UPSTREAM (local server queries an upstream one), BB_BASEHASH_IGNORE_VARS, BB_NO_NETWORK, BB_GENERATE_MIRROR_TARBALLS (git tarballs), and in the intro the -S none option. Confirmed in own-mirrors.bbclass: SOURCE_MIRROR_URL feeding PREMIRRORS. Confirmed in sstate.bbclass: SSTATE_MIRRORS with PATH and downloadfilename. Confirmed in scripts/sstate-cache-management.py: --remove-duplicated (-d), --cache-dir, --stamps-dir; there is no .sh version. Confirmed in bitbake-diffsigs and bitbake-dumpsig: the -t/--task option. rm_work.bbclass exists. Corrected BB_SIGNATURE_HANDLER (OEEquivHash, not OEEquivBasicHash). Removed the hours-to-minutes claim, the NFS remark and the per-release rationale.

Method: documentation only; no commands were run.
