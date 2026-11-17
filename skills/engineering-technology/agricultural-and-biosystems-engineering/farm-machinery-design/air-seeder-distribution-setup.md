---
id: engineering-technology.agricultural-and-biosystems-engineering.farm-machinery-design.air-seeder-distribution-setup
name: air-seeder-distribution-setup
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: farm-machinery-design
tags: [agricultural-and-biosystems-engineering, farm-machinery-design, air-seeder, pneumatic-distribution, seeding, planter-design, distribution-head, fan-speed, blockage-sensor]
level: practitioner
status: draft
description: "Set up and troubleshoot an air seeder: meter calibration, fan speed, primary and secondary distribution, blockage monitoring and sectioned control."
sources:
  - "Srivastava, Goering, Rohrbach & Buckmaster, Engineering Principles of Agricultural Machines (ASABE)"
  - "ASABE Standards, Engineering Practices and Data (https://www.asabe.org)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Air seeder distribution setup

**Goal:** even rate across all openers at the intended seed and fertiliser rate.

## Layout
Tank and meter roller (per product) feed an air stream from a fan; the primary line leads to a distribution head (or tower), which splits flow to secondary hoses and openers. Some machines use individual row metering.

## Setup and calibration
1. Calibrate each product (seed, fertiliser): run the meter for a set number of revolutions and weigh; the monitor computes rate per revolution and ground speed.
2. Fan speed: set per the manufacturer's chart for the product and rate; too low causes plugging, too high bounces seed and damages kernels.
3. Check hose lengths and layout: equal runs help equal distribution; kinks and tight bends restrict flow.
4. Monitor blockages with sensors; clean distribution heads for wet fertiliser or treated seed.
5. Test distribution: collect from each opener over fixed time; calculate the coefficient of variation between openers; target a small CV, typically under about 10 percent (check the manufacturer).

## Gotchas
- Mixed products with different densities can segregate in the air stream; use separate bins/lines when the rates differ widely.
- Seed damage at high air speed on large or fragile seeds (pulses).
- Moisture and static cause bridging in tank outlets.

## Verify
- [ ] Rate within 5 percent of target on a catch test.
- [ ] Opener-to-opener CV acceptable and no blocked lines after field work.
