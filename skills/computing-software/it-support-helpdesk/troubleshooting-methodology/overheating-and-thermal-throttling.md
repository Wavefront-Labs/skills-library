---
id: computing-software.it-support-helpdesk.troubleshooting-methodology.overheating-and-thermal-throttling
name: overheating-and-thermal-throttling
category: computing-software
field: it-support-helpdesk
product: troubleshooting-methodology
tags: [it-support-helpdesk, troubleshooting-methodology, thermal-throttling, overheating, fans, thermal-paste, hwinfo, kernel-processor-power]
level: practitioner
status: draft
description: "Prove and fix overheating: read temperatures and throttle flags, spot firmware-limited CPU speed in event logs, clean airflow, repaste, and address laptop use habits."
sources:
  - "https://www.hwinfo.com/"
  - "https://learn.microsoft.com/en-us/windows-hardware/design/device-experiences/thermal-management-in-windows"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# overheating-and-thermal-throttling

## Symptoms
Fans roaring, sudden slowdowns under load, the device hot to touch, shutdowns with no
BSOD (Kernel-Power 41), or vendor BIOS warnings about thermal events.

## Measure
- HWiNFO (sensors-only mode): CPU package temperature, per-core temperature, and the
  "Thermal Throttling" and power-limit flags. Sustained 95-100 C on most CPUs means it is
  at its limit.
- Task Manager > Performance > CPU: speed dropping well below base clock under load.
- System log: Kernel-Processor-Power event 37 ("speed of processor ... is being limited by
  system firmware") shows throttling over time.
- Vendor tools (Dell SupportAssist, HP diagnostics, Lenovo Vantage) run fan tests and read
  thermal logs.

## Fix in order
1. Usage: laptops on beds/laps block intake vents; use a hard surface. Check for a
   runaway process keeping the CPU at 100% (fix that, not the heat).
2. Airflow: compressed air through vents (hold fans still while blowing); clear dust from
   heatsink fins. Desktops: front-to-back airflow and filters cleaned.
3. Firmware: BIOS and EC updates often change fan curves; vendor thermal mode set to
   Optimized/Balanced, not Quiet, for heavy users.
4. Hardware: dried thermal paste or pads on older devices; repaste (or vendor repair under
   warranty). Failed fan = replace.

## Gotchas
- Thin laptops throttle by design under long loads; compare with the model's normal
  behaviour before calling it faulty.
- Docked laptops with lid closed run hotter; some models need the lid open.
- Swollen batteries often come with heat complaints; check (see
  laptop-battery-replacement-and-swelling).

## Verify
Under a 10-minute load test, temperatures stay below the limit, no throttle flags or
event 37 appear, and the user's workload no longer slows down.
