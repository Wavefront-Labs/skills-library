---
id: computing-software.it-support-helpdesk.troubleshooting-methodology.no-post-beep-codes-and-cmos-clearing
name: no-post-beep-codes-and-cmos-clearing
category: computing-software
field: it-support-helpdesk
product: troubleshooting-methodology
tags: [it-support-helpdesk, troubleshooting-methodology, post-beep-codes, clear-cmos, cpu-troubleshooting, visual-inspection, no-post, motherboard-diagnostics]
level: practitioner
status: draft
description: "Diagnose PCs that power on but don't POST: visual inspection, beep and LED codes, clearing CMOS, minimum-configuration testing, and CPU fault signs."
sources:
  - "https://www.comptia.org/en/certifications/a/"
  - "https://www.dell.com/support/kbdoc/en-us/000125179/dell-computer-will-not-turn-on-or-boot"
  - "https://support.hp.com/us-en/document/ish_4094225-4094272-16"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# no-post-beep-codes-and-cmos-clearing

## Visual and sensory inspection first
- Unplug; open the case (ESD precautions). Look for swollen or leaking capacitors (domed
  tops, brown residue), burn marks, melted connectors, loose RAM or GPU, bent CPU socket
  pins, debris or liquid damage, dust blocking heatsinks.
- Smell: burnt electronics smell usually means a failed PSU or VRM; stop and replace,
  don't keep powering it.
- Check every power connector is fully seated (24-pin, CPU 8-pin, GPU).

## Beep and LED codes
Codes are vendor-specific; always look up the exact model.
| Vendor | Method | Example |
|---|---|---|
| Dell | Power/diagnostic LED blink pattern (amber/white counts) | 2 amber, 3 white = memory failure on many models |
| HP | Caps Lock/Num Lock LED blinks, or beeps | Count long/short blinks; HP doc lists per model |
| Lenovo | Beep codes / error codes on screen | Use Lenovo's beep code list |
| Desktop boards (AMI/Award) | Beeps; debug LEDs (CPU, DRAM, VGA, BOOT) or 2-digit Q-codes | Q-code tables in the board manual |
- Record the pattern exactly (count long and short) before touching anything.

## Clearing CMOS
- Resets BIOS settings to defaults; fixes failed overclock/bad settings and some
  no-POST after BIOS changes.
- Methods: board jumper (CLR_CMOS) for 10 s with power removed; clear CMOS button on the
  rear I/O; remove the coin cell for several minutes; laptops may have a key combo or
  require removing the internal battery and RTC battery.
- After clearing: reapply baseline settings (UEFI mode, Secure Boot, TPM, SATA mode
  AHCI/RAID as before). Changing SATA mode stops Windows booting; changing TPM state can
  trigger BitLocker recovery.

## Minimum configuration test
1. Disconnect everything except CPU, one RAM stick, PSU, (onboard graphics or one GPU).
2. Try each RAM stick in the primary slot.
3. If it POSTs, add components back one at a time.
4. Still nothing: swap PSU (test with a tester), then board vs CPU.

## CPU faults
Rare compared to RAM, PSU and board. Signs: CPU debug LED stays lit, no POST with known-
good RAM/PSU/board, overheating shutdowns (check cooler mounting, thermal paste,
fan header CPU_FAN connected), bent pins after a reseat. Confirm by testing the CPU in
a known-good board where possible. Under-warranty OEM PCs: replace the board/CPU via the
vendor.

## Verify
The PC POSTs repeatedly, BIOS settings match the baseline, vendor diagnostics pass,
and the faulty part and code are recorded in the ticket.
