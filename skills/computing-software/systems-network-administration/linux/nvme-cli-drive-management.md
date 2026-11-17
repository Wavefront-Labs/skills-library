---
id: computing-software.systems-network-administration.linux.nvme-cli-drive-management
name: nvme-cli-drive-management
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, nvme-cli, nvme, smart-log, nvme-format, namespaces, sanitize, ssd-health]
level: advanced
status: docs-checked
description: "Manage NVMe SSDs with nvme-cli: list and identify controllers, smart-log health and wear, error logs, namespaces, format/sanitize for secure erase, and firmware updates."
sources:
  - https://github.com/linux-nvme/nvme-cli/tree/master/Documentation
  - https://github.com/linux-nvme/nvme-cli/blob/master/Documentation/nvme-format.txt
  - https://github.com/linux-nvme/nvme-cli/blob/master/Documentation/nvme-sanitize.txt
  - https://github.com/linux-nvme/nvme-cli/blob/master/Documentation/nvme-fw-commit.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# nvme-cli drive management

## Inventory
```bash
nvme list                              # devices, model, serial, namespace usage, format, firmware
nvme id-ctrl /dev/nvme0 -H | less      # capabilities (sanitize, format, namespace management)
nvme id-ns /dev/nvme0n1 -H | grep -E 'LBA Format|in use'   # sector size options (512 vs 4096)
```
`/dev/nvme0` = controller (char device), `/dev/nvme0n1` = namespace 1 (block device), `p1` partitions.

## Health
```bash
nvme smart-log /dev/nvme0
#  reports the SMART / health log page: critical warning, temperature, available spare, percentage used,
#  media errors, error log entries, unsafe shutdowns and data units read/written (see the NVMe specification for units)
nvme error-log /dev/nvme0 | head
smartctl -a /dev/nvme0                 # smartmontools also understands NVMe
```
Alert on `critical_warning != 0`, `available_spare < available_spare_threshold`, rising `media_errors`.

## Erase / reformat (destroys data)
```bash
nvme format /dev/nvme0n1 --lbaf=1 --ses=1    # apply LBA format index 1 (from id-ns; or --block-size=4096) + user data erase
nvme sanitize /dev/nvme0 --sanact=2          # start-block-erase (if supported); --sanact=4 is start-crypto-erase, 3 overwrite
nvme sanitize-log /dev/nvme0                 # progress
```
`--ses` values: 0 no secure erase, 1 user data erase, 2 cryptographic erase. `--lbaf` defaults to 0 and conflicts with `--block-size`.
Reformat before partitioning.

## Namespaces (enterprise drives)
`nvme create-ns /dev/nvme0 --nsze=... --ncap=... --flbas=0`, `nvme attach-ns /dev/nvme0 -n 2 -c 0`,
`nvme ns-rescan /dev/nvme0`. Namespace management needs controller support (check `nvme id-ctrl -H`).

## Firmware
`nvme fw-log /dev/nvme0`; `nvme fw download /dev/nvme0 --fw=fw.bin` then `nvme fw commit /dev/nvme0 --slot=1 --action=1`
(action 0 replace only, 1 replace and activate at next reset, 2 set-active, 3 replace and activate immediately); the dashed
forms `fw-download`/`fw-commit` still work as deprecated aliases. Or `fwupdmgr` for LVFS-supported models.

## Gotchas
- Power-state (APST) problems on some drives: the kernel parameter `nvme_core.default_ps_max_latency_us=0` disables the power-saving latency allowance (kernel source documents it as a workaround for a quirked drive).

## Verify
- [ ] `nvme smart-log` captured into monitoring; after format, `nvme id-ns` shows the chosen LBA format `(in use)`.

## Checked

Checked 2026-10-26 against linux-nvme/nvme-cli master (last commit 2026-10-25) Documentation/nvme-format, nvme-sanitize, nvme-fw-commit, nvme-fw-download, nvme-create-ns, nvme-attach-ns and nvme-list, and drivers/nvme/host/core.c in torvalds/linux. Confirmed: format --lbaf, --block-size and --ses values, sanitize --sanact values, fw commit slot and action values, the deprecated dashed fw-download alias, create-ns and attach-ns options, the nvme_core.default_ps_max_latency_us parameter. Removed: the unconfirmed 512,000-byte data-unit figure, the 4K performance claim, the laptop frozen-sanitize claim and the consumer-drive namespace claim.

Method: documentation only; no commands were run.
