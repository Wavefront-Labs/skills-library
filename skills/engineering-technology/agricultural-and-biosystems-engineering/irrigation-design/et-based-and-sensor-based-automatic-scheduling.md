---
id: engineering-technology.agricultural-and-biosystems-engineering.irrigation-design.et-based-and-sensor-based-automatic-scheduling
name: et-based-and-sensor-based-automatic-scheduling
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: irrigation-design
tags: [agricultural-and-biosystems-engineering, irrigation-design, et-based-scheduling, sensor-based-scheduling, smart-controller, soil-moisture-threshold, weather-station-et, automatic-irrigation]
level: practitioner
status: gated
description: "Automate irrigation scheduling from ET or soil moisture sensors: trigger logic, depletion model, rain handling, limits and sensor validation."
sources:
  - "Allen, Pereira, Raes & Smith, FAO Irrigation and Drainage Paper 56: Crop Evapotranspiration (https://www.fao.org/4/x0490e/x0490e00.htm)"
  - "ASABE Standards, Engineering Practices and Data (https://www.asabe.org)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# ET-based and sensor-based automatic scheduling

**Goal:** a controller that irrigates when the crop needs it, with guardrails.

## ET-based
- Daily reference ET from a nearby station (`et0-penman-monteith-inputs-and-checks`), multiplied by the crop coefficient (`single-and-dual-crop-coefficient-method`) gives crop ET; subtract effective rain (`effective-rainfall-estimation`); keep a running soil water balance (`checkbook-water-balance-scheduling`).
- Trigger when depletion reaches the management allowed depletion (`taw-raw-and-management-allowed-depletion`); apply the net depth divided by the application efficiency.
- Limits: minimum and maximum run time, interval, and a skip rule after forecast rain (with caution on forecast reliability).

## Sensor-based
- Soil moisture sensors at representative depths trigger irrigation at set thresholds (`soil-moisture-sensor-selection-and-installation`); use at least two depths and replicate locations to avoid a single bad sensor.
- Determine thresholds from field capacity and refill points observed on the sensor record, not from factory defaults.

## Combined
Use ET for the planned depth and sensors to correct drift: a good practice is to use ET for routine decisions and sensor trends as a check.

## Verify
- [ ] Sensor readings versus soil sampling check once per season.
- [ ] Controller log shows irrigation events following the set logic.
- Commercial controller methods differ; read the vendor's documentation. No numeric thresholds are given here.
