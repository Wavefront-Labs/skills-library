---
id: computing-software.firmware-embedded-development.device-driver-development.yocto-sdk-populate-sdk
name: yocto-sdk-populate-sdk
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [populate-sdk, yocto, cross-toolchain, esdk, environment-setup, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Build and use a Yocto SDK: bitbake -c populate_sdk, adding target and host packages, kernel module builds inside the SDK, and the extensible SDK."
sources:
  - https://docs.yoctoproject.org/sdk-manual/index.html
  - https://github.com/openembedded/openembedded-core/blob/master/meta/classes-recipe/populate_sdk_base.bbclass
  - https://github.com/openembedded/openembedded-core/blob/master/meta/files/toolchain-shar-extract.sh
  - https://github.com/openembedded/openembedded-core/blob/master/meta/classes-recipe/populate_sdk_ext.bbclass
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SDK generation with populate_sdk

The SDK gives developers a cross-toolchain and a sysroot matching the image, without running
BitBake.

## Build
```sh
bitbake acme-image -c populate_sdk          # standard SDK
bitbake acme-image -c populate_sdk_ext      # extensible SDK (includes devtool)
ls tmp/deploy/sdk/*.sh                       # self-extracting installer
```
The target sysroot contains headers and libraries for everything in the image. `SDKIMAGE_FEATURES` defaults
to `dev-pkgs dbg-pkgs src-pkgs` (plus `doc-pkgs` when the distro enables `api-documentation`).

## Add things to the SDK
```bitbake
# in the image recipe
TOOLCHAIN_TARGET_TASK:append = " libgpiod-dev protobuf-dev"     # target libraries/headers
TOOLCHAIN_HOST_TASK:append = " nativesdk-protobuf-compiler nativesdk-cmake"   # host tools
SDKIMAGE_FEATURES:append = " staticdev-pkgs"
```

## Use
```sh
./<sdk-name>-toolchain-<version>.sh -d ~/sdk/acme -y     # -y: answer yes, -d: install directory
source ~/sdk/acme/environment-setup-<target-sys>
echo $CC          # the cross compiler plus the options and --sysroot the SDK sets
$CC -o hello hello.c
cmake -B build        # use the CMake toolchain file shipped with the SDK (see the SDK manual)
```
Always use `$CC`, `$CFLAGS`, `$LDFLAGS` from the environment: calling `aarch64-poky-linux-gcc`
directly skips `--sysroot` and links against host headers.

## Kernel modules with the SDK
Add `kernel-devsrc` to the SDK (`TOOLCHAIN_TARGET_TASK:append = " kernel-devsrc"`; `populate_sdk_base`
also adds it when `SDK_FEATURES` contains `kernel-src`), then once per install prepare the kernel source
in the SDK sysroot:
```sh
cd <kernel-devsrc directory in the SDK sysroot> && make modules_prepare
make -C <kernel-devsrc directory> M=$PWD modules
```
The module must match the image's kernel version and config exactly (same build).

## Extensible SDK
Includes devtool, and can fetch updates from a server configured with `SDK_UPDATE_URL`. Larger than the
standard SDK but keeps developers in sync with recipe changes.

## Gotchas
- The SDK host architecture follows `SDKMACHINE`, which defaults to the build host's architecture; set it
  (for example to an aarch64 host) to build an SDK for another host.
- Rebuild and redistribute the SDK whenever image libraries change ABI.

## Verify
- [ ] A test app built with the SDK runs on the target image without missing library errors.
- [ ] An out-of-tree module built in the SDK loads on the target (`vermagic` matches).

## Checked

2026-10-27, OpenEmbedded-Core master.
Confirmed in populate_sdk_base.bbclass and bitbake.conf: SDKIMAGE_FEATURES default (dev-pkgs dbg-pkgs src-pkgs, doc-pkgs conditional), staticdev-pkgs, TOOLCHAIN_TARGET_TASK, TOOLCHAIN_HOST_TASK, SDK_DEPLOY = DEPLOY_DIR/sdk, the TOOLCHAIN_OUTPUTNAME pattern, kernel-devsrc added for the kernel-src SDK feature, SDKMACHINE ??= BUILD_ARCH. Confirmed in toolchain-scripts.bbclass: environment-setup-<target sys> scripts, OECORE_NATIVE_SYSROOT, SDKTARGETSYSROOT. Confirmed in toolchain-shar-extract.sh: installer options -y and -d. Confirmed in populate_sdk_ext.bbclass: extensible SDK and SDK_UPDATE_URL. Corrected the SDKMACHINE default, which was stated as x86_64. Removed the fixed installer file name, the OEToolchainConfig.cmake path, and the devtool build-image and sdk-update commands (not found). Confirmed in bitbake.conf: TOOLCHAIN_OPTIONS adds --sysroot. Confirmed in the Linux kbuild documentation: make modules_prepare prepares a tree for external modules (see out-of-tree-kernel-module-build).

Method: documentation only; no commands were run.
