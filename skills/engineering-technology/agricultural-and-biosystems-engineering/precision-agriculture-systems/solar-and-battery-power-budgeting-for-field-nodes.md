---
id: engineering-technology.agricultural-and-biosystems-engineering.precision-agriculture-systems.solar-and-battery-power-budgeting-for-field-nodes
name: solar-and-battery-power-budgeting-for-field-nodes
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: precision-agriculture-systems
tags: [agricultural-and-biosystems-engineering, precision-agriculture-systems, field-node-power, solar-power-budget, battery-sizing, duty-cycle, sleep-current, lifepo4, charge-controller, farm-iot]
level: practitioner
status: draft
description: "Budget power for field sensor nodes: average current from duty cycle, daily energy, solar panel and battery sizing for the worst month, chemistry and temperature limits."
sources:
  - "ISO standards catalogue (https://www.iso.org)"
  - "ASHRAE Handbook (Fundamentals and Refrigeration volumes) (https://www.ashrae.org)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Solar and battery power budgeting for field nodes

**Goal:** a node that keeps reporting through the worst weather of the season without a site visit.

## Energy budget
1. List each state: sleep (microamps), sensor warm-up and measurement (milliamps for a short time), radio transmit (tens of milliamps for the airtime) and receive. For each, multiply current by time per day to get ampere-hours (or watt-hours with the supply voltage).
2. Sum per day and add margin (25-50 percent) for ageing, temperature and unknowns; check the sleep current by measurement with a precise meter, not only the datasheet, since it dominates the average.
3. Modems with always-on cellular connections use far more energy; a gateway needs a larger panel than a sleeping sensor.

## Solar sizing
- Use the peak sun hours for the worst month at the site (from a solar atlas); daily panel energy = panel rated power x peak sun hours x system efficiency (about 0.6-0.8 including controller, wiring and soiling). Size the panel so the worst month still gives at least the daily need.
- Tilt toward the equator at about the latitude angle (or steeper for winter bias) and keep clear of crop shade and dust.
- Charge controller: use an MPPT for larger systems and a good PWM controller for small ones matched to the battery chemistry.

## Battery
- Autonomy: store several days (three to five days is common) of the daily need without sun; do not discharge lead-acid below about 50 percent for long life; lithium iron phosphate (LiFePO4) tolerates deeper cycling but must not be charged below 0 C unless the battery has a low-temperature protection; lithium-ion cells likewise.
- Keep the battery in a shaded, ventilated box; temperature affects capacity.
- Protect with a fuse and use wire sized for the current.

## Enclosure
IP65 or higher for outdoor enclosures, with a breather or desiccant and cable glands; mount to avoid the water ingress and animal damage.

## Verify
- [ ] Measured average current over a day versus the budget.
- [ ] Battery voltage log through a week of poor weather.
- Unconfirmed: battery charge limits; read the cell specification.
