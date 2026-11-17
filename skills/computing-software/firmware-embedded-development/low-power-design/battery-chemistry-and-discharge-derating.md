---
id: computing-software.firmware-embedded-development.low-power-design.battery-chemistry-and-discharge-derating
name: battery-chemistry-and-discharge-derating
category: computing-software
field: firmware-embedded-development
product: low-power-design
tags: [battery, cr2032, aa-lithium, li-ion, li-socl2, nimh, internal-resistance, voltage-sag, pulse-current-derating, peukert, self-discharge, cold-temperature-derating, cutoff-voltage, brownout-threshold, state-of-charge, firmware-embedded-development]
level: advanced
status: draft
description: "Pick a battery chemistry that survives the real current profile: internal-resistance sag under pulse loads, cold-temperature derating, self-discharge, cutoff voltage vs regulator dropout."
sources:
  - https://data.energizer.com/pdfs/cr2032.pdf
  - https://www.ti.com/lit/an/slva196/slva196.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Battery chemistry and discharge derating

**Goal:** choose a battery that actually survives the product's real current
profile over its claimed life, not just one whose mAh rating divides nicely
into the average-current number from
`computing-software.firmware-embedded-development.low-power-design.current-profiling-and-duty-cycle-budget`
— capacity-on-paper and deliverable-capacity-under-this-load are different
numbers.

## Internal resistance and pulse-current voltage sag
A coin cell (CR2032) has internal resistance in the tens of ohms, rising as it
discharges and drops further in cold temperature. A transmit pulse drawing
even 30-60mA (common for a radio TX burst) across that resistance sags the
terminal voltage significantly below open-circuit voltage for the pulse
duration — if that sag crosses the regulator's/MCU's brownout threshold, the
device resets mid-transmission, intermittently, in a way that looks like a
firmware bug and only reproduces as the battery ages or in cold weather.
**Match chemistry to current profile, not just to average capacity**: CR2032
and similar lithium coin cells are poor at sustained high pulse current;
AA-sized lithium (higher capacity, much lower internal resistance) or a
small supercapacitor/bulk capacitor in parallel with the cell (absorbs the
pulse, cell only supplies the time-averaged current) are the standard fixes
when pulse current is unavoidable.

## Peukert-like capacity derating under real loads
A cell's rated mAh is typically measured at a specific, often very low,
discharge rate. Pulling meaningfully more current than that test condition
delivers less *usable* capacity than the rating implies (loosely analogous to
the Peukert effect well-documented for lead-acid, less commonly quantified
for small lithium cells but the direction is the same: higher current, less
effective mAh) — treat a datasheet mAh rating at a mismatched discharge
profile as optimistic, and derate it using the chemistry-specific discharge
curve at a current closer to the product's actual peak, not nominal.

## Cold-temperature derating
Capacity and sustainable current both drop in cold temperature, and the drop
varies sharply by chemistry — Li-SOCl₂ (lithium thionyl chloride) is a common
choice specifically for better cold-temperature/long-shelf-life behavior
versus alkaline or standard lithium coin cells for outdoor/industrial sensor
products. If the product's deployment environment includes cold temperature,
validate against the datasheet's temperature-derated discharge curves, not
the room-temperature headline spec.

## Self-discharge and shelf life
A product that sits in a warehouse/retail channel for months before first
power-on loses capacity to self-discharge before the user ever sees it —
chemistries vary widely here (some lithium primary cells retain >90% after
years; NiMH self-discharges materially faster, unsuitable for long-shelf-life
unpowered storage). Factor expected time-to-first-use into the capacity
budget, not just time-in-service after that.

## Cutoff voltage vs regulator dropout
The product's actual usable battery life ends when terminal voltage drops
below whatever the regulator/MCU needs to keep operating, not at some
chemistry-nominal "empty" voltage — a buck-boost or low-dropout regulator
rated to operate down near the cell's end-of-discharge voltage extracts
meaningfully more usable capacity from the same cell than a regulator with a
higher minimum input voltage. Check this against the actual discharge curve,
not the nominal voltage alone.

## Verify
- [ ] Battery chemistry's internal-resistance/pulse-current behavior was checked against the product's actual peak current draw, not just average current.
- [ ] Capacity budget uses a discharge curve at a current and temperature representative of real deployment, not the datasheet's low-rate room-temperature test condition.
- [ ] Brownout/regulator cutoff voltage was checked against sagged (not open-circuit) voltage during the product's highest current pulse, on the actual hardware.
- [ ] Expected warehouse/shelf time before first use is included in the capacity budget for the chosen chemistry's self-discharge rate.
