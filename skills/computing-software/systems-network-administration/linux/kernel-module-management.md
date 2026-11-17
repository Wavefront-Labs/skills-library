---
id: computing-software.systems-network-administration.linux.kernel-module-management
name: kernel-module-management
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, kernel-module, modprobe, insmod, rmmod, depmod, dkms, blacklist, modinfo, lsmod, module-parameters, out-of-tree-module, kernel-upgrade, sysadmin, modprobe-d, modules-load-d, module-options]
level: advanced
status: docs-checked
description: "Load, blacklist, parameterize and rebuild kernel modules safely: modprobe vs insmod, depmod, module params, and DKMS across kernel upgrades."
sources:
  - https://github.com/kmod-project/kmod/blob/master/man/modprobe.8.scd
  - https://github.com/kmod-project/kmod/blob/master/man/modprobe.d.5.scd
  - https://github.com/kmod-project/kmod/blob/master/man/depmod.8.scd
  - https://github.com/dell/dkms
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Kernel module management — load, tune, and survive a kernel upgrade

**Goal:** load/unload modules correctly (with dependencies resolved, not
just the one file), blacklist a module that's causing problems, pass boot-
or load-time parameters, and keep an out-of-tree module (Nvidia, VirtualBox,
ZFS) working across a kernel upgrade instead of breaking boot.

## 1. `modprobe` vs `insmod` — almost always want modprobe
```bash
lsmod | grep <name>                  # is it currently loaded, and what depends on it
modinfo <name>                        # description, parameters, license, which .ko file, version
modprobe <name>                       # loads it AND its dependencies, using the module database
insmod /path/to/exact.ko              # loads exactly that file, no dependency resolution — rarely what you want
rmmod <name>                          # unload; fails with EBUSY if something still depends on it or has it open
modprobe -r <name>                    # unload, and also remove now-unused dependencies modprobe pulled in
```
`insmod` is the low-level primitive; `modprobe` is what almost every real
task should use because it reads `/lib/modules/$(uname -r)/modules.dep` to
pull in dependencies automatically and respects blacklist/alias/options
config. Reach for `insmod` only when loading a module file that isn't (yet)
installed into the standard module tree — e.g. testing a freshly built
`.ko` before `make modules_install`.

## 2. depmod — keeping the dependency database current
```bash
depmod -a                      # rebuild modules.dep for the running kernel after installing new modules
depmod -a $(uname -r)           # explicit kernel version, if managing modules for a kernel not currently booted
```
A module copied into `/lib/modules/$(uname -r)/` without a subsequent
`depmod -a` is invisible to `modprobe` (not in the dependency map yet) even
though the file is physically present — "the module exists but modprobe
says not found" is almost always a missing `depmod -a` step, not a path problem.

## 3. Module parameters — compile-time flexibility without a rebuild
```bash
modinfo -p <name>                          # lists every parameter the module accepts, with description
modprobe <name> paramname=value             # one-off, lost on next load unless persisted
```
```
# /etc/modprobe.d/mymodule.conf
options mymodule paramname=value another=1
```
Config in `/etc/modprobe.d/*.conf` is what `modprobe` reads automatically
on every future load (including the one baked into the initramfs if the
module is needed at boot — see the boot-process skill for when a module
needs to be IN the initramfs rather than just loadable after boot). Runtime
parameter changes for an already-loaded module usually need
`/sys/module/<name>/parameters/<param>` (only works for parameters marked
writable at runtime by the module itself) or a full unload/reload — most
parameters only take effect at load time.

## 4. Blacklisting — preventing autoload, not removing the file
```
# /etc/modprobe.d/blacklist-local.conf
blacklist nouveau
install nouveau /bin/false      # belt-and-suspenders: even an explicit modprobe call does nothing
```
`blacklist` only makes modprobe ignore the module's own aliases, so it stops **automatic**
loading by device match — an explicit `modprobe nouveau` still loads it unless the
`install ... /bin/false` override is also present (the `mask` keyword in modprobe.d(5)
prevents loading directly or through any alias), or unless the module is additionally excluded
from the initramfs (`dracut --omit-drivers`/equivalent) for cases where
something in early boot would otherwise pull it in before
`/etc/modprobe.d/` config is even consulted. The classic Nvidia-proprietary-
driver-vs-nouveau conflict needs both the blacklist and an initramfs rebuild
to actually take effect at boot, not just the blacklist file alone.

## 5. DKMS — out-of-tree modules that survive a kernel upgrade
```bash
dkms status                           # which out-of-tree modules are registered, for which kernel versions
dkms install -m <module> -v <version> -k $(uname -r)
dkms autoinstall                       # rebuild everything registered for the currently running kernel
```
A plain `make && make install` of an out-of-tree module (Nvidia proprietary
driver, VirtualBox kernel modules, ZFS-on-Linux on some distros) builds a
`.ko` tied to the *exact* kernel version headers it was compiled against —
the next kernel update leaves the old `.ko` orphaned and the module fails
to load (`modprobe: FATAL: Module ... not found` for the new kernel
version) until it's rebuilt. DKMS automates exactly that rebuild as a
post-kernel-install hook — register the module source once with DKMS and
every subsequent `apt`/`dnf` kernel upgrade triggers an automatic rebuild
instead of leaving the system silently missing that driver until someone
notices (often first observed as "my GPU/VM stopped working after an
update").

## Gotchas
- A module that's `rmmod`-resistant (`EBUSY`) often has an open file handle
  or a dependent module, not literally "in use" in an obvious way —
  `lsmod | grep <name>` shows a "Used by" count and names; address those
  first (`rmmod` the dependents, or find/kill the process holding a device
  file open) rather than retrying the same `rmmod`.
- Signed kernels (Secure Boot enabled, see the boot-process skill) reject
  unsigned out-of-tree modules outright (the `dmesg` line names a signature or lockdown failure) — DKMS alone
  doesn't fix this; the module must be signed with a key the kernel trusts
  (`dkms generate_mok` is DKMS's helper for a Machine Owner Key; see dkms(8) and your
  distribution's Secure Boot guide), or Secure Boot must be disabled.
- Kernel module versioning (`vermagic` in `modinfo` output) is
  checked at load time — a `.ko` built for one kernel release normally refuses to
  load under another unless `modprobe --force-vermagic` (the man page warns the check
  exists for your protection) or a proper rebuild for the new version is done.
- `/etc/modules-load.d/*.conf` (one module name per line) is for modules
  that must load **at boot** unconditionally — different from
  `/etc/modprobe.d/` (which configures *how* a module loads when
  triggered, not *whether* it loads automatically at boot).

## Verify
- [ ] `modinfo <name>` resolves and shows the expected version/description before and after any kernel upgrade — confirms the module exists for the running kernel.
- [ ] `lsmod | grep <name>` shows the module loaded with the expected "Used by" dependents, matching intent.
- [ ] A blacklisted module does not reappear in `lsmod` after a reboot, confirmed by testing the actual reboot, not just reading the config file.
- [ ] `dkms status` shows every registered out-of-tree module built successfully for the currently running kernel version — checked immediately after any kernel upgrade, before assuming the driver still works.

## Checked

Checked 2026-10-27 against kmod man pages (modprobe(8), depmod(8), modprobe.d(5)), dkms(8), dracut man page and systemd modules-load.d(5), current development branches, 2026-10-27. Confirmed: modprobe -r removing unused dependencies, --force-vermagic, blacklist alias semantics, install and mask keywords, softdep, depmod -a, DKMS install/autoinstall/status actions and autoinstaller service, dracut --omit-drivers, modules-load.d(5) paths. Removed or softened: the exact Lockdown message, mokutil command, example kernel versions and DKMS example version.

Method: documentation only; no commands were run.
