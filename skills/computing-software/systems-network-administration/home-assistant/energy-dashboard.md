---
id: computing-software.systems-network-administration.home-assistant.energy-dashboard
name: energy-dashboard
category: computing-software
field: systems-network-administration
product: home-assistant
tags: [energy, riemann-sum, kwh]
level: practitioner
status: docs-checked
description: "Set up the Home Assistant Energy dashboard: add grid, solar, battery, gas, water and individual devices, convert power to energy, and hide cards."
sources:
  - https://www.home-assistant.io/docs/energy/
  - https://www.home-assistant.io/docs/energy/individual-devices/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: get energy data into the dashboard from whatever hardware you have.

The Energy dashboard covers electricity, gas and water. For each, usage is grouped into what you consume, produce and store. You can start with a single source.

Add sources by type:

- Electricity grid
- Solar panels
- Home batteries
- Gas consumption
- Water consumption
- Individual devices

Each has its own page in the energy docs.

Sensor requirements:

- Energy inputs expect sensors reporting energy (kWh).
- If you only have an instantaneous power sensor (W or kW), add a sensor that returns energy using the Riemann sum integral integration.
- Power inputs can also be configured alongside, accepting sensors with `state_class: measurement` and units such as `W` or `kW`.

Hardware for individual devices, per the individual devices page: smart plugs (Zigbee, Z-Wave or Wi-Fi) that measure energy through the outlet, and smart relays behind existing switches.

Customise: show or hide individual cards without changing sources. Add at least one source or device first, or the customise option is unavailable.

## Checked

2026-11-04. Confirmed against the Energy page and the Energy individual devices page. Removed the CT clamp, Tesla Powerwall and Forecast.Solar lines, which are not on these pages.

Method: documentation only; no commands were run.
