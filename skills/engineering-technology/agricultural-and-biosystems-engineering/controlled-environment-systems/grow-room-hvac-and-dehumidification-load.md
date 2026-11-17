---
id: engineering-technology.agricultural-and-biosystems-engineering.controlled-environment-systems.grow-room-hvac-and-dehumidification-load
name: grow-room-hvac-and-dehumidification-load
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: controlled-environment-systems
tags: [agricultural-and-biosystems-engineering, controlled-environment-systems, grow-room-hvac, dehumidification-load, vertical-farm-cooling, latent-load, sensible-load, led-heat-load, transpiration-load, vertical-farming]
level: advanced
status: draft
description: "Size HVAC for indoor grow rooms and vertical farms: lighting heat, transpiration latent load, envelope loads, dehumidifier or coil capacity, load swings and redundancy."
sources:
  - "ASHRAE Handbook (Fundamentals and Refrigeration volumes) (https://www.ashrae.org)"
  - "ASABE Standards, Engineering Practices and Data (https://www.asabe.org)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Indoor grow room HVAC and dehumidification load

**Goal:** cooling and dehumidification capacity that holds temperature and humidity through the lights-on and lights-off cycles.

## Loads
- Lighting: essentially all electrical power into the lights ends up as heat in the room (light absorbed by the crop and surfaces becomes heat, apart from the small chemical energy stored in biomass). So sensible load from lights is about the total input power; with water-cooled or ducted luminaires, part is removed before the room air.
- Plant transpiration: the crop evaporates water that must be removed again as latent load. Latent heat of vaporisation is about 0.68 kWh per kg (2.45 MJ/kg) near 20-25 C, so each kg of water transpired per hour is about 0.68 kW of latent load, and the dehumidification capacity (kg/h) must equal the transpiration (and any other moisture sources). Estimate crop ET from the light level and VPD (using the Penman-Monteith approach in `et0-penman-monteith-inputs-and-checks` adapted to the controlled environment, or measured data of similar rooms).
- Equipment: fans, pumps, power supplies and other motors inside the envelope.
- Envelope and infiltration through doors, plus fresh air for CO2 and people. Rooms with good insulation have little envelope load.
- People, and moisture from floors and nutrient solution evaporation.

## Calculation
Total cooling = sensible (lights + equipment + people + envelope) + latent (transpiration + other). Compute separately for lights-on (peak) and lights-off (lower sensible load, still some transpiration). The sensible heat ratio is typically low because of the high latent fraction at high light intensity; specify coils and dehumidifiers for the actual sensible-to-latent ratio, not just total tons.

## Equipment
- Chilled water or DX coils with sufficient depth for dehumidification; reheat to avoid overcooling; heat-pump dehumidifiers that return the heat to the room; or desiccant systems for very low dew points.
- Controls for temperature and VPD (`humidity-control-and-vapour-pressure-deficit`), staging for light dimming and the night cycle. Redundancy: a failure in a sealed room causes crop loss within hours.
- Heat rejection to outdoors, and heat recovery where useful.

## Verify
- [ ] Load calculation separated into sensible and latent, lights-on and lights-off.
- [ ] Dehumidifier condensate volume measured against predicted transpiration.
- Unconfirmed: crop ET values; use measured data.
