---
id: computing-software.systems-network-administration.linux.hardware-errors-mce-edac-rasdaemon
name: hardware-errors-mce-edac-rasdaemon
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, rasdaemon, edac, mce, machine-check, ecc-memory, ras-mc-ctl]
level: practitioner
status: docs-checked
description: "Diagnose hardware errors on Linux: machine check exceptions, EDAC corrected and uncorrected ECC errors, rasdaemon and ras-mc-ctl, mapping errors to DIMMs, and PCIe AER."
sources:
  - https://github.com/mchehab/rasdaemon
  - https://www.kernel.org/doc/html/latest/PCI/pcieaer-howto.html
  - https://github.com/mchehab/rasdaemon/blob/master/docs/ras-mc-ctl-python.rst
  - https://github.com/mchehab/rasdaemon/blob/master/docs/ras-mc-ctl-perl.rst
  - https://github.com/mchehab/rasdaemon/blob/master/misc/rasdaemon.env
  - https://github.com/prometheus/node_exporter/blob/master/collector/edac_linux.go
  - https://github.com/torvalds/linux/blob/master/Documentation/ABI/testing/sysfs-devices-edac
licence: Apache-2.0
version: 4
updated: 2026-11-17
---
# Hardware errors (MCE/EDAC/rasdaemon)

## Where errors show up
```bash
journalctl -k -p warning | grep -iE 'mce|machine check|edac|hardware error|aer|corrected'
dmesg -T | grep -iE 'mce|EDAC|Hardware Error'
```
- **MCE** (Machine Check Exception): CPU-reported errors (cache, memory controller, bus). `mce: [Hardware Error]: CPU 3: Machine Check: 0 Bank 7: ...`.
- **EDAC**: memory controller drivers count ECC errors: CE (corrected) and UE (uncorrected).
- **PCIe AER**: link and device errors: `pcieport 0000:00:1c.0: AER: Corrected error received`.
- **GHES/APEI**: firmware-first platforms report through ACPI ("[Hardware Error]: event severity: corrected").

## rasdaemon
```bash
dnf install rasdaemon       # apt install rasdaemon
systemctl enable --now rasdaemon
ras-mc-ctl dimm --status        # is an EDAC kernel module loaded?
ras-mc-ctl db --summary         # summary of recorded errors (needs rasdaemon running with --record)
ras-mc-ctl db --errors          # detailed list of recorded errors
ras-mc-ctl dimm --layout        # memory layout reported through EDAC sysfs
ras-mc-ctl dimm --error-count   # per-DIMM corrected/uncorrected counters
```
Current rasdaemon uses these subcommands (`db`/`database` and `dimm`/`mem`); the former Perl `ras-mc-ctl` used flat flags such as `--summary` and `--status`, and rasdaemon's `ras-mc-ctl-perl` page maps them.
Label DIMMs so reports name physical slots: `ras-mc-ctl dimm --print-labels`, add vendor board labels as files in `/etc/ras/dimm_labels.d/`, then `ras-mc-ctl dimm --register-labels` (root; writes the labels to EDAC sysfs).

## EDAC sysfs
```bash
grep . /sys/devices/system/edac/mc/mc*/dimm*/dimm_label /sys/devices/system/edac/mc/mc*/ce_count /sys/devices/system/edac/mc/mc*/ue_count 2>/dev/null
```
No `mc0`? The EDAC driver for your platform isn't loaded (for example `amd64_edac` on AMD) or firmware-first handling hides the errors; then rely on the BMC's event log.

## Interpreting
| Pattern | Action |
|---|---|
| Occasional CE on one DIMM | monitor; ECC is doing its job |
| CE rate climbing on one DIMM | schedule replacement; a rising rate is a warning sign |
| Any UE | replace DIMM; the affected process or the host may have crashed |
| CE spread across all DIMMs on one channel | memory controller/CPU socket or board issue |
| MCE bank errors on the same CPU repeatedly | CPU, microcode, or VRM; update BIOS/microcode first |
| AER corrected bursts on a NIC/NVMe slot | reseat, check riser and cable, update device firmware |

## Fleet monitoring
- node_exporter `edac` collector: `node_edac_correctable_errors_total`, `node_edac_uncorrectable_errors_total`; alert on rate increase per host.
- `kernel.panic_on_oops` and kdump help capture UE crashes; the BMC SEL survives reboots when the OS log doesn't.
- Memory page offlining: rasdaemon can offline pages with repeated CEs, controlled by `PAGE_CE_ACTION` (default `soft`) in its environment file (`rasdaemon.env` in the source tree; the installed path is distribution-specific).

## Verify
- [ ] `ras-mc-ctl dimm --status` reports drivers loaded; DIMM labels map to physical slots.
- [ ] Alert exists for CE rate and any UE; replaced DIMM shows zero counts afterwards.

## Checked

Checked against the rasdaemon sources (`docs/ras-mc-ctl-python.rst`, `docs/ras-mc-ctl-perl.rst`, `misc/rasdaemon.env`), the prometheus node_exporter `edac_linux.go` source and the Linux kernel documentation tree (torvalds/linux master, latest commit 2026-10-25) (ABI testing sysfs-devices-edac) on 2026-10-26. Confirmed: `ras-mc-ctl` subcommands `db --summary/--errors` and `dimm --status/--layout/--error-count/--print-labels/--register-labels`, label database drop-in directory `dimm_labels.d`, `PAGE_CE_ACTION` default soft, EDAC sysfs `mc*/ce_count`, `ue_count` and `dimm_label`, node_exporter metrics `node_edac_correctable_errors_total` and `node_edac_uncorrectable_errors_total`, `amd64_edac` driver. Stale: the flat `ras-mc-ctl --summary`-style flags belong to the former Perl implementation. Removed: the mcelog replacement claim, `mcelog --ascii`, Intel EDAC module names, CE-rate numbers, `/etc/sysconfig/rasdaemon` path, the 'Fatal machine check' panic text and `ipmitool` command.

Method: documentation only; no commands were run.
