---
id: computing-software.firmware-embedded-development.device-driver-development.out-of-tree-kernel-module-build
name: out-of-tree-kernel-module-build
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [linux-kernel-module, kbuild-out-of-tree, obj-m, modules-prepare, cross-compile, vermagic, insmod, modinfo, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Build a Linux kernel module outside the kernel tree with Kbuild for a cross-compiled embedded target, and fix vermagic, symbol-version and missing-headers errors."
sources:
  - https://docs.kernel.org/kbuild/modules.html
  - https://docs.kernel.org/kbuild/kbuild.html
  - https://docs.kernel.org/admin-guide/module-signing.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Out-of-tree kernel module build

**Goal:** a `.ko` that loads on the target's exact kernel, built from a separate repo.

## Minimal module
```c
// hello.c
#include <linux/module.h>
#include <linux/init.h>
static int __init hello_init(void) { pr_info("hello: loaded\n"); return 0; }
static void __exit hello_exit(void) { pr_info("hello: unloaded\n"); }
module_init(hello_init);
module_exit(hello_exit);
MODULE_LICENSE("GPL");          /* non-GPL modules can't use GPL-only exported symbols */
MODULE_DESCRIPTION("demo");
```
```make
# Kbuild (or Makefile)
obj-m := hello.o
hello-y := hello_main.o hello_hw.o   # for multi-file modules use a different module name
```
```make
# Makefile
KDIR ?= /lib/modules/$(shell uname -r)/build
all:
	$(MAKE) -C $(KDIR) M=$(CURDIR) modules
clean:
	$(MAKE) -C $(KDIR) M=$(CURDIR) clean
```

## Cross-compiling for the target
```
make -C ~/linux-target ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- M=$PWD modules
```
`KDIR` must be the **configured and prepared** source/build tree of the exact kernel the target
runs: same version and same `.config`. `make modules_prepare` prepares a tree for external modules but
does not build `Module.symvers`, so with `CONFIG_MODVERSIONS` a full kernel build is needed. In Yocto,
build the module from a recipe that inherits the module class.

## Load errors and causes
| Error | Cause |
|---|---|
| `Invalid module format` (dmesg shows a version magic mismatch) | built against a different kernel version or config |
| `disagrees about version of symbol X` | `CONFIG_MODVERSIONS` CRCs differ: wrong `Module.symvers` |
| `Unknown symbol X` | depends on another module not loaded (use `modprobe` with `depmod`), or GPL-only symbol with non-GPL license |
| load rejected for a missing or unknown signature | kernel enforces module signing (`CONFIG_MODULE_SIG_FORCE`): sign with the kernel's key (`scripts/sign-file`) |

## Install
`make -C $KDIR M=$PWD INSTALL_MOD_PATH=<rootfs> modules_install` then run `depmod` for the target kernel version. On target: `modprobe hello`, `modinfo hello.ko` to check vermagic and parameters.

## Verify
- [ ] `modinfo hello.ko` vermagic equals `uname -r` + flags on target.
- [ ] `insmod`/`rmmod` cycle 100 times without warnings in dmesg (catches leaks in exit path).

## Checked

2026-10-27, Linux kernel documentation (mainline v7.3).
Confirmed in Documentation/kbuild/modules.rst: make -C <kernel dir> M=$PWD [modules|modules_install|clean], obj-m with <module>-y for multi-file modules, the modules_prepare target and the note that it does not build Module.symvers so a full build is needed for CONFIG_MODVERSIONS, INSTALL_MOD_PATH, KBUILD_EXTRA_SYMBOLS. Confirmed in kbuild.rst: ARCH and CROSS_COMPILE. Confirmed in module-signing.rst: CONFIG_MODULE_SIG_FORCE and scripts/sign-file. Corrected the claim that modules_prepare produces Module.symvers. Removed the Yocto SDK path and the vermagic field list and the exact error string. The hello example module is illustrative.

Method: documentation only; no commands were run.
