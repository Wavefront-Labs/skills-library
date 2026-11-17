---
id: computing-software.firmware-embedded-development.device-driver-development.yocto-wic-kickstart-images
name: yocto-wic-kickstart-images
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [wic-kickstart, yocto, wks-file, partition-layout, bmaptool, firmware-embedded-development]
level: practitioner
status: gated
description: "Define SD/eMMC disk images with Yocto WIC .wks files: raw bootloader offsets, boot and A/B rootfs partitions, WKS_FILE, wic ls/cp, and flashing with bmaptool."
sources:
  - https://docs.yoctoproject.org/dev-manual/wic.html
  - https://docs.yoctoproject.org/ref-manual/kickstart.html
  - https://github.com/openembedded/openembedded-core/blob/master/meta/classes-recipe/image_types.bbclass
  - https://github.com/yoctoproject/bmaptool
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WIC images and kickstart files

WIC assembles a partitioned disk image from build artefacts, described by an OpenEmbedded
kickstart (`.wks`) file.

## Example: i.MX-style eMMC with A/B rootfs
```
# meta-acme/wic/acme-emmc.wks.in
part u-boot --source rawcopy --sourceparams="file=imx-boot" --ondisk mmcblk --no-table --align 32
part /boot  --source bootimg_partition --ondisk mmcblk --fstype=vfat --label boot --active --align 4096 --size 64M
part /      --source rootfs --ondisk mmcblk --fstype=ext4 --label rootfsA --align 4096 --size 1024M
part        --ondisk mmcblk --fstype=ext4 --label rootfsB --align 4096 --size 1024M
part /data  --ondisk mmcblk --fstype=ext4 --label data --align 4096 --size 256M --fsoptions "noatime"
bootloader --ptable gpt
```
Key options:
- `--no-table` reserves space for the partition without adding it to the partition table; `--align` is in
  KBytes and `--offset` places the partition at an exact offset (default unit KiB; `s`, `M`, `G` also accepted).
- `--source rawcopy` with `--sourceparams="file=..."` copies a file such as a bootloader image, and
  `--source bootimg_partition` copies the files named by `IMAGE_BOOT_FILES` (kernel, DTBs, boot script)
  (gated: unconfirmed, source is paywalled or blocked); the Wic kickstart reference does not describe these two plugins.
- `--source bootimg_efi` and `--source bootimg_pcbios` (underscores) are the x86 boot plugins shown in the
  Wic manual; `--source rootfs` fills the partition from the image rootfs.
- `--size` (minimum size), `--fixed-size` (exact size, not combinable with `--size`), `--overhead-factor`
  (at least 1, default 1.3), `--extra-filesystem-space`, `--extra-partition-space`, `--part-type` (GPT type GUID),
  `--fsoptions`, `--label`, `--fstype`, `--ondisk`, `--active`.
- `bootloader --ptable gpt|msdos` (a `bootloader` option, not a `part` option).

## Select it
```bitbake
WKS_FILE = "acme-emmc.wks.in"
IMAGE_FSTYPES += "wic.zst wic.bmap"
IMAGE_BOOT_FILES = "Image imx8mp-acme.dtb boot.scr"
WKS_FILE_DEPENDS:append = " imx-boot"
```
`.wks.in` files may use `${VAR}` expansion.

## Inspect and modify without rebuilding
```sh
wic ls  acme-image.wic                 # partitions
wic ls  acme-image.wic:2/etc
wic cp  myconfig acme-image.wic:2/etc/acme.conf
wic rm  acme-image.wic:2/etc/junk
```
(If `wic` is not on your path, run it through `oe-run-native wic-native wic ...`.)

## Flashing
```sh
sudo bmaptool copy acme-image.wic.zst /dev/sdX       # uses .wic.bmap: writes only mapped blocks
```
The bmap file lets `bmaptool` copy only the mapped blocks and verify their checksums. Double-check `/dev/sdX`.

## Gotchas
- Raw bootloader offsets must match what the SoC ROM expects (see the SoC reference manual); overlapping
  the GPT header and entry table (the first 17 KiB with 512-byte sectors) with `--ptable gpt` breaks one or the other.
- Partition sizes too small for the rootfs fail the build; `--extra-filesystem-space` gives headroom.
- First-boot resize of the data partition needs a service in the image.

## Verify
- [ ] `wic ls` shows the intended layout; the board boots from the flashed image.
- [ ] Bootloader readable by the ROM (boot log shows SPL/U-Boot from the expected offset).

## Checked

2026-10-27, Yocto Project documentation (current), OpenEmbedded-Core master and the bmaptool README.
Confirmed in the Wic kickstart reference: --no-table, --align (KBytes), --offset (default unit k; s, M, G), --ondisk, --fstype, --label, --active, --size, --fixed-size, --overhead-factor (at least 1, default 1.3), --part-type, --fsoptions, --extra-filesystem-space, --extra-partition-space, and bootloader --ptable gpt or msdos. Confirmed in the Wic manual: wic ls, cp and rm with image.wic:N/path, oe-run-native wic-native wic, bmaptool or dd for writing, WKS_FILE and WKS_FILE_DEPENDS, bootimg_efi and bootimg_pcbios (underscore names), rootfs. Confirmed in image_types.bbclass: bmap and zst conversion types, so IMAGE_FSTYPES wic.zst and wic.bmap apply. Confirmed in the bmaptool README: bmaptool copy verifies checksums of mapped blocks. The rawcopy and bootimg_partition plugins and IMAGE_BOOT_FILES could not be confirmed (the wic sources are not in OE-core) and are marked gated. Corrected --extra-space (the options are --extra-filesystem-space and --extra-partition-space), the hyphenated bootimg plugin names and oe-run-native wic-tools. Removed --rootfs-dir, the i.MX offsets, the speed claim and growpart/systemd-repart. The 17 KiB GPT figure is 512 x (1 + 1 + 32) bytes.

Method: documentation only; no commands were run.
