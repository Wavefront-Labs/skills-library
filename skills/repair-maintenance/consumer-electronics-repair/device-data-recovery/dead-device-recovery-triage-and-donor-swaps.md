---
id: repair-maintenance.consumer-electronics-repair.device-data-recovery.dead-device-recovery-triage-and-donor-swaps
name: dead-device-recovery-triage-and-donor-swaps
category: repair-maintenance
field: consumer-electronics-repair
product: device-data-recovery
tags: [device-data-recovery, data-recovery, hdd-recovery, hard-drive, clicking-drive, head-swap, pcb-swap, rom-chip, adaptives, stiction, clean-bench, ddrescue, disk-imaging, write-blocker, pc-3000, ssd-recovery, nvme, chip-off, nand-reader, monolith, usb-flash-drive, sd-card, phone-data-recovery, board-revival, file-based-encryption, secure-enclave, bitlocker, filevault]
level: advanced
status: draft
description: "Triage dead HDDs, SSDs, flash media and phones for data recovery: decide what's safe to try, image first with ddrescue, PCB/ROM and head-swap limits, chip-off vs board revival under encryption."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dead-device recovery triage and donor swaps

**Goal:** give the data the best chance — choose the least destructive route for the
failure type, make one good image before anything else, and recognise early when a
job needs a lab (or is impossible because of encryption).

## 1. Ground rules
- **Every power-on of a failing drive can be the last.** No CHKDSK, fsck, "repair"
  tools, or reinstalling the OS on the source. Work on a copy.
- Agree with the owner which files matter most (photos folder, one database) — it
  decides how you image.
- Record serials, model, firmware and PCB numbers before you touch anything.
- Data recovery is not a backup strategy; once done, point the user to
  computing-software.systems-network-administration.backup-and-recovery.backup-design-and-restore-drills.

## 2. Spinning hard drives (HDD)
| Symptom | Likely cause | Action |
|---|---|---|
| Not detected, no spin, maybe burnt smell | PCB (TVS diode, motor controller) | PCB swap with ROM transfer |
| Spins, clicks repeatedly | Heads failed or media damage | Stop. Head swap = clean bench / lab |
| Buzzes, doesn't spin | Stuck heads (stiction) or seized motor | Lab |
| Spins, detected, slow/hangs | Weak heads or bad sectors | Careful imaging |
1. **PCB swap:** a matching donor board alone usually fails, because each drive's
   calibration ("adaptives") lives in the ROM/serial flash chip on the PCB. Move the
   8-pin ROM chip (or read/write it with a programmer) from patient to donor. Check
   board number, firmware and the TVS diodes on the 5 V/12 V input first — a shorted
   TVS diode is often the whole fault.
2. **Imaging:** connect via a write-blocker or a dedicated imager; on Linux use GNU
   ddrescue with a mapfile so it can resume:
   `ddrescue -d -n /dev/sdX patient.img patient.map` (fast pass, skip bad areas), then
   `ddrescue -d -r3 /dev/sdX patient.img patient.map` to retry the gaps.
   Image to a healthy drive larger than the patient.
3. **Head swaps** need a matched donor (model, firmware, head map, often date code),
   a laminar-flow clean bench, head combs and usually tools like PC-3000 to handle
   firmware modules. Opening a drive on a desk contaminates platters and makes later
   lab recovery harder or impossible. If clicking, refer out.

## 3. SSDs and flash media
- **SSD:** no PCB swap — data is tied to the controller and usually hardware-encrypted
  with keys inside it. Dead SSD with a shorted input cap or regulator: repair that
  rail board-level and image straight away. Controller-dead or firmware-locked
  drives need vendor-specific lab tools (PC-3000 SSD class), with limited support.
- **TRIM:** deleted files on an SSD are usually gone within minutes; tell the owner.
- **USB sticks and SD cards:** if the controller or connector is dead, chip-off: lift
  the TSOP/BGA NAND, read it in a NAND reader and rebuild the controller's XOR,
  interleave and ECC with software. **Monolith** cards have no separate NAND —
  scrape to the test pads under a microscope and solder fine wires to a reader pinout.
  (Draft note: pinouts and rebuild steps are device-specific.)

## 4. Phones and encrypted devices
- Modern iPhones and Android phones with file-based encryption tie the key to the
  **SoC / Secure Enclave plus the user passcode**. Chip-off of the NAND gives only
  ciphertext. The only route is to revive the **original board** enough to boot and
  unlock it — swap the failed parts (charge IC, PMIC rail, shorted cap) or move CPU
  and NAND together to a donor board, which needs the matching security chips.
  See repair-maintenance.consumer-electronics-repair.board-level-microsoldering.microscope-ic-swap-and-pad-jumper-repair.
- Laptops with BitLocker/FileVault or soldered SSDs: need the recovery key or the
  original board running. Ask for the key at intake.
- Older unencrypted phones/eMMC devices: eMMC can be read in an adapter after
  removal or via ISP test points.

## Gotchas
- Freezing drives, tapping them or swapping platters at home destroys recoverable data.
- The cheapest moment to refer a clicking drive to a lab is **before** your attempt.
- Never write recovered files back to the patient device.
- Owner consent and proof of ownership before recovery; respect privacy of the data.

## Verify
- [ ] Original device unchanged except documented part swaps; serials recorded.
- [ ] Image file and mapfile saved; ddrescue reports no unread areas (or they are listed).
- [ ] Priority files open correctly (photos display, documents open, databases mount).
- [ ] Recovered data delivered on new media, checksummed, with a file list.
- [ ] Owner advised on backup, encryption keys and safe disposal of the dead device.
