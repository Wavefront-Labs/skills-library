---
id: computing-software.firmware-embedded-development.bootloader-development.u-boot-fit-images
name: u-boot-fit-images
category: computing-software
field: firmware-embedded-development
product: bootloader-development
tags: [u-boot, fit-image, its-file, mkimage, kernel-dtb-ramdisk, configurations, dtb-overlay, bootm, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Package kernel, device trees and initramfs into a U-Boot FIT image with an .its file and mkimage, select configurations per board, and boot it with bootm."
sources:
  - https://docs.u-boot.org/en/latest/usage/fit/index.html
  - https://docs.u-boot.org/en/latest/usage/fit/source_file_format.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# U-Boot FIT images

**Goal:** one file holding the kernel, every board variant's DTB and optional initramfs, with
hashes, so U-Boot loads a consistent set and can verify it.

## The .its source
```dts
/dts-v1/;
/ {
    description = "Product kernel";
    #address-cells = <1>;
    images {
        kernel-1 {
            data = /incbin/("Image.gz");
            type = "kernel"; arch = "arm64"; os = "linux";
            compression = "gzip";
            load = <0x40480000>; entry = <0x40480000>;
            hash-1 { algo = "sha256"; };
        };
        fdt-revb {
            data = /incbin/("board-revb.dtb");
            type = "flat_dt"; arch = "arm64"; compression = "none";
            hash-1 { algo = "sha256"; };
        };
        fdt-revc { data = /incbin/("board-revc.dtb"); type = "flat_dt"; arch = "arm64";
                   compression = "none"; hash-1 { algo = "sha256"; }; };
        ramdisk-1 { data = /incbin/("initramfs.cpio.gz"); type = "ramdisk"; arch = "arm64";
                    os = "linux"; compression = "none"; hash-1 { algo = "sha256"; }; };
    };
    configurations {
        default = "conf-revc";
        conf-revb { kernel = "kernel-1"; fdt = "fdt-revb"; ramdisk = "ramdisk-1"; };
        conf-revc { kernel = "kernel-1"; fdt = "fdt-revc"; ramdisk = "ramdisk-1"; };
    };
};
```
Build: `mkimage -f fit.its fitImage`. Inspect: `mkimage -l fitImage` (both shown in the U-Boot FIT how-to).

## Booting
```
load mmc 0:1 ${loadaddr} fitImage
bootm ${loadaddr}#conf-${board_rev}
```
`bootm <addr>#<config>` selects a configuration; without it the `default` is used. Board
revision can come from GPIO straps or an EEPROM read in U-Boot board code.

## Gotchas
- Make sure `${loadaddr}` (where the FIT sits) doesn't overlap the kernel's load or
  decompression target.
- Use `sha256` hashes, not `crc32`; they're the basis for signing later (verified boot).
- DT overlays can be FIT images too (`type = "flat_dt"` + configurations listing the base and
  overlays: `fdt = "fdt-1", "fdt-2";`, as in the U-Boot overlay FIT page).

## Verify
- [ ] `mkimage -l` lists all images with hashes and the right configurations.
- [ ] Each configuration boots on its board revision.

## Checked

2026-10-28. Confirmed in the U-Boot FIT how-to (doc/usage/fit/howto.rst) and overlay FIT page (overlay-fdt-boot.rst): `/incbin/` image nodes, `type = "flat_dt"`, `algo = "sha256"` hash nodes, `mkimage -f its itb`, `mkimage -l`, `bootm <addr>#<config>`, several `fdt` entries in one configuration.
Removed: `dumpimage -l`, `CONFIG_SYS_BOOTM_LEN` and the "Image too large" message, `mkimage -E`, Yocto variable names, and the exact "Verifying Hash Integrity" log text (not in fetched pages).

Method: documentation only; no commands were run.
