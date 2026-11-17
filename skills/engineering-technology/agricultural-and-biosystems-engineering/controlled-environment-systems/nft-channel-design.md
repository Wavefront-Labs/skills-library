---
id: engineering-technology.agricultural-and-biosystems-engineering.controlled-environment-systems.nft-channel-design
name: nft-channel-design
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: controlled-environment-systems
tags: [agricultural-and-biosystems-engineering, controlled-environment-systems, nft-design, nutrient-film-technique, hydroponic-channel, channel-slope, flow-rate-per-channel, lettuce-hydroponics, recirculating-hydroponics, hydroponics]
level: practitioner
status: draft
description: "Design NFT hydroponic channels: slope, flow per channel, channel length limits, film depth, pump and return sizing, and failure protection against pump stops."
sources:
  - "ASABE Standards, Engineering Practices and Data (https://www.asabe.org)"
  - "ASHRAE Handbook (Fundamentals and Refrigeration volumes) (https://www.ashrae.org)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# NFT channel design

**Goal:** a shallow stream of nutrient solution that wets the root mat evenly along every channel while keeping the roots oxygenated.

## Principle
In the nutrient film technique the roots sit in a thin flowing film in a sloped channel, so the upper roots are in humid air and the lower ones in the film, which gives good oxygen supply. It suits small, fast crops: lettuce, herbs, strawberries.

## Design values (typical, adjust by pilot)
- Flow per channel: commonly about 1-2 L/min per channel; too low gives dry spots and nutrient depletion along the channel, too high floods roots and wastes pumping energy.
- Slope: about 1 in 30 to 1 in 100 (roughly 1-3 percent) along the channel; the lower slope needs very accurate installation, and any sag creates a pond.
- Length: channels of around 10-15 m are common limits for lettuce; longer channels deplete oxygen and nutrients and give a growth gradient from inlet to outlet. Measure the EC, pH and temperature at the end.
- Film depth a few mm; roots mats should not dam the stream (thin out mats and use ridged or corrugated bottoms).
- Channel shape: width for the pot spacing; covers or lids for light exclusion and algae control.

## Hydraulics
- Distribution manifold with equal-length feeds or flow restrictors (orifice or micro-tube) at each channel inlet to equalise flow; check that the flow variation is within about 10 percent among channels.
- Return gutter sized for the total flow without backing up; sump and pump sized for the total plus a margin; filtration before the manifold.
- Solution temperature (target about 18-24 C for lettuce, lower oxygen solubility when warm) and shading of tanks and pipes.

## Protection
NFT roots dry out very fast if the pump stops (within an hour in hot conditions). Use an alarm and back-up power or a second pump, and design the sump to keep the system fed.

## Verify
- [ ] Measure flow per channel by catching at the outlet for a timed interval.
- [ ] Check EC, pH and temperature at inlet and outlet.
- Unconfirmed: crop-specific limits; trial before scaling.
