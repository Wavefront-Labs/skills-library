---
id: computing-software.it-support-helpdesk.troubleshooting-methodology.power-supply-testing
name: power-supply-testing
category: computing-software
field: it-support-helpdesk
product: troubleshooting-methodology
tags: [it-support-helpdesk, troubleshooting-methodology, psu-testing, power-supply, multimeter, atx, laptop-charger, usb-c-power-delivery, random-shutdowns]
level: practitioner
status: draft
description: "Test desktop PSUs and laptop chargers safely: symptoms, swap tests, PSU tester and multimeter voltage tolerances, USB-C PD wattage problems, and when to stop."
sources:
  - "https://www.usb.org/usb-charger-pd"
  - "https://www.comptia.org/en/certifications/a/core-1-v15/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# power-supply-testing

## Symptoms that point to power
- Dead: no lights, no fans. Click-then-nothing: PSU protection tripping (could be a short
  elsewhere).
- Random restarts under load (gaming, renders) without a BSOD; Kernel-Power 41.
- Laptop: "plugged in, not charging", "slow charger" warning, battery draining while
  plugged in, charger LED off or blinking.

## Desktop PSU
1. Check the obvious: wall socket, power strip, rear switch, 115/230 V selector on older
   units, cable.
2. Swap with a known-good PSU of sufficient wattage; this is the fastest real test.
3. PSU tester or multimeter on the 24-pin connector (powered via the PSU's own switch
   with the tester attached). ATX tolerances are about plus or minus 5%:

| Rail | Acceptable |
|---|---|
| +12 V | 11.40 - 12.60 V |
| +5 V | 4.75 - 5.25 V |
| +3.3 V | 3.14 - 3.47 V |
| +5 VSB | 4.75 - 5.25 V |

   Readings at idle do not prove the PSU holds up under load; a swap test does.

## Laptop chargers
- Match wattage to the model; a lower-watt USB-C charger may charge only when off.
- USB-C PD: use the cable and charger rated for the wattage; e-marked cables are needed
  above 60 W. Try another USB-C port (not all ports take power).
- Vendor BIOS often shows adapter wattage detected; "unknown" means bad charger or cable.
- Barrel chargers: inspect the tip and cable strain points for damage.

## Safety
Never open a PSU or charger; capacitors hold dangerous charge after unplugging. Replace,
do not repair. Burning smell or scorch marks: unplug and retire immediately.

## Verify
With the replacement, the device runs a load test without restarts, voltages are in
tolerance, and the laptop reports the expected adapter wattage and charges.
