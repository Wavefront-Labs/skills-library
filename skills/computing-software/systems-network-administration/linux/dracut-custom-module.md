---
id: computing-software.systems-network-administration.linux.dracut-custom-module
name: dracut-custom-module
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, dracut, dracut-custom-module, module-setup-sh, initramfs, early-userspace, dracut-hooks]
level: advanced
status: docs-checked
description: "Write a custom dracut module: modules.d/NNname layout, module-setup.sh check/depends/install functions, inst_hook stages, and testing it with lsinitrd and rd.break."
sources:
  - https://github.com/dracut-ng/dracut-ng/blob/main/doc_site/modules/ROOT/pages/developer/modules.adoc
  - https://github.com/dracut-ng/dracut-ng/blob/main/man/dracut.modules.7.adoc
  - https://github.com/dracut-ng/dracut-ng/blob/main/man/dracut.8.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Writing a custom dracut module

**Goal:** run your own code in the initramfs (unlock a device a custom way, fetch a key, fix a
device before root mounts) in a way that survives kernel updates.

## Layout
`/usr/lib/dracut/modules.d/90mymod/` (two-digit prefix = ordering):
```
module-setup.sh      # required, sourced by dracut at build time
mymod-hook.sh        # runtime script(s)
```
## module-setup.sh
```bash
#!/bin/bash
check() {            # see return codes below
    require_binaries curl jq || return 1
    return 255
}   # 0 include, 1 do not include, 255 include only if required or explicitly requested
depends() { echo network systemd; }      # other dracut modules needed
installkernel() { instmods vfat nls_cp437; }
install() {
    inst_multiple curl jq                 # binaries + their libs
    inst_simple "$moddir/mykey.conf" /etc/mykey.conf
    inst_hook pre-mount 50 "$moddir/mymod-hook.sh"
}
```
Hook stages (run order): `cmdline`, `pre-udev`, `pre-trigger`, `initqueue` (sub-hooks `initqueue/settled`, `initqueue/finished` and `initqueue/timeout`; `finished` scripts must return true for the loop to end), `pre-mount`, `mount`, `pre-pivot`, `cleanup`. Hook scripts are sourced, so end them with `return`, not `exit`.
Runtime helpers: `. /lib/dracut-lib.sh`; `getarg mymod.url=` reads kernel args; `warn`, `info`, `die`.

## Build and test
```bash
dracut -f --add mymod /boot/initramfs-$(uname -r).img $(uname -r)
lsinitrd /boot/initramfs-$(uname -r).img | grep mymod
echo 'add_dracutmodules+=" mymod "' > /etc/dracut.conf.d/mymod.conf   # make permanent (spaces matter)
```
Boot once with `rd.break=pre-mount rd.debug` to check your hook ran (`/run/initramfs/rdsosreport.txt` is written when you reach an emergency shell).

## Gotchas
- Always keep a known-good fallback kernel/initramfs before testing; a failing hook can stop boot.
- `return 255` from check() means `--add` is required — otherwise it silently is not included.
- Ship the module with your package so image rebuilds include it; in host-only mode `check()` should return 0 only if the module is really needed (the `$hostonly` variable tells it which mode applies).

## Verify
- [ ] `lsinitrd` lists your files; a test reboot logs your hook's messages and reaches root.

## Checked
Checked 2026-10-25 against the dracut-ng man page sources (dracut-ng/dracut-ng man/*.adoc and doc_site, main as of 2026-10-24; latest release 112). Confirmed: module directory `/usr/lib/dracut/modules.d`, `module-setup.sh` functions `check()` (0 include, 1 do not, 255 only if required or explicitly requested), `depends()`, `installkernel()`, `install()`, helpers `inst_multiple`, `inst_simple`, `instmods`, `inst_hook`, `require_binaries`, `$moddir`, hook directories and order including `initqueue/settled`, `initqueue/finished`, `initqueue/timeout`, sourced-hook rule, `getarg` and `dracut-lib.sh`, and `dracut --add`. Removed unconfirmed claims: the systemd unit installation lines (`$systemdsystemunitdir` is not documented in the pages read) and the claim about dracut-*.service ordering.

Method: documentation only; no commands were run.
