---
id: computing-software.firmware-embedded-development.device-driver-development.yocto-devtool-modify-workflow
name: yocto-devtool-modify-workflow
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [devtool, yocto, devtool-modify, devtool-finish, deploy-target, kernel-development, workspace-layer, extensible-sdk, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Iterate on kernel or driver source in Yocto with devtool: modify into a workspace, build, deploy-target to the board, then finish into patches in your BSP layer."
sources:
  - https://docs.yoctoproject.org/ref-manual/devtool-reference.html
  - https://docs.yoctoproject.org/dev-manual/devtool.html
  - https://docs.yoctoproject.org/kernel-dev/intro.html
  - https://docs.yoctoproject.org/sdk-manual/extensible.html
  - https://github.com/openembedded/openembedded-core/blob/master/scripts/lib/devtool/standard.py
  - https://github.com/openembedded/openembedded-core/blob/master/scripts/lib/devtool/deploy.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# devtool modify workflow

**Goal:** edit-build-test a recipe's source (kernel, U-Boot, a driver module) in a normal git
tree, then turn the changes into patches in your layer with no hand-written bbappends.

## Loop
```sh
devtool modify linux-vendor                 # or virtual/kernel; checks out source + recipe patches
cd build/workspace/sources/linux-vendor     # a git repo, branch "devtool", patches as commits
# edit drivers/iio/..., optionally: devtool menuconfig linux-vendor
git commit -am "iio: foo: fix scale"
devtool build linux-vendor
devtool deploy-target linux-vendor root@192.168.1.50     # copies installed files over ssh
```
- devtool creates `workspace/` as a layer with a bbappend pointing the recipe at your source
  tree (externalsrc); bitbake now builds from there.
- `deploy-target` copies the recipe's installed files to the target (an SSH server, or a local
  pseudo-managed rootfs path). For a kernel recipe, check on the target whether the kernel image
  and device tree the bootloader actually reads were updated (they may live on a separate boot
  partition); if not, rebuild and flash the image (`devtool build-image`).
- `deploy-target` does not interact with the target's package manager (RPM, opkg); do not mix the
  two on one device.
- `devtool undeploy-target <recipe> <target>` restores the files that were overwritten and removes
  the files the recipe deployed; `-a` undeploys everything.
- `devtool build-image myboard-image` builds an image including all workspace recipes.

## Finish into your layer
```sh
devtool finish linux-vendor ../meta-myboard
```
- Writes each new commit as a patch and creates/updates a bbappend in `meta-myboard`
  (`recipes-kernel/linux/linux-vendor_%.bbappend` with `SRC_URI` entries), and saves config
  changes as a kernel config fragment (from `devtool menuconfig`) where supported.
- Then removes the recipe from the workspace. Use `devtool update-recipe -a ../meta-myboard`
  to write the changes to a bbappend in that layer but keep working.
- Review the generated bbappend: add machine overrides (`SRC_URI:append:myboard`) if the
  change is board-specific; devtool writes unconditional entries.

## Other useful commands
| Command | Use |
|---|---|
| `devtool add mydrv https://git.example.com/mydrv.git` | create a new recipe from source |
| `devtool upgrade <recipe> -V 2.1` | move a recipe to a new upstream version, rebasing patches |
| `devtool status` | what is in the workspace |
| `devtool reset <recipe>` | drop the workspace entry (source tree kept unless `-r`/`--remove-work`) |
| `devtool search` / `devtool find-recipe` / `devtool edit-recipe` | search recipes, locate and open a recipe file |

## Gotchas
- Leaving recipes in the workspace silently changes what images build; `devtool status` before
  release builds, and never ship from a workspace.
- Only committed changes become patches; uncommitted edits are lost on finish.
- If the recipe's patches do not apply cleanly in `modify`, fix them first (it stops with a
  conflict in the source tree).

## Verify
- [ ] `devtool status` empty after finish; clean `bitbake` of the image reproduces the change.
- [ ] Generated patches apply in a fresh build without the workspace layer.

## Checked

Yocto Project documentation (docs.yoctoproject.org, development tip 6.1 after the 6.0 release) and OE-Core devtool sources, read 2026-10-27.
Confirmed: workspace sources under `build/workspace/sources`; `modify` checks out a branch named `devtool` by default (`-b`); modified recipes build from the workspace via externalsrc; `deploy-target recipe target` over SSH, `undeploy-target` restoring backed-up files (and `-a`), and no package-manager integration (dev-manual/devtool); `finish` turns committed changes into patches and writes either the recipe or a bbappend depending on the destination layer, and updates a kconfig fragment (standard.py); `update-recipe -a LAYERDIR` writes a bbappend; `upgrade -V` and `reset -r/--remove-work` flags; subcommands search, find-recipe, edit-recipe, status, build-image, add.
Removed the unsupported statement that deploy-target copies the kernel image; the docs only describe it as deploying the recipe's output files.

Method: documentation only; no commands were run.
