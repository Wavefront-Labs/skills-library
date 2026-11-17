---
id: computing-software.systems-network-administration.network-design.rack-power-and-airflow
name: rack-power-and-airflow
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, rack-airflow, hot-aisle, cold-aisle, rack-power, pdu, data-centre]
level: practitioner
status: draft
description: "Lay out network racks for power and cooling: hot/cold aisle, port-side vs PSU-side intake, blanking panels, PDU A/B feeds and power budget per rack."
sources:
  - https://www.apc.com/us/en/download/document/SPD_VAVR-5UDTU5_EN/
  - https://www.ashrae.org/technical-resources/bookstore/datacom-series
  - https://www.cisco.com/c/en/us/td/docs/switches/datacenter/nexus9000/hw/n93180ycfx_hig/guide/b_c93180ycfx_nxos_mode_hardware_install_guide/b_c93180ycfx_nxos_mode_hardware_install_guide_chapter_01.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Rack power and airflow

## Airflow
- Hot aisle / cold aisle: rack fronts face the cold aisle, exhausts face the hot aisle; contain one
  of them for efficiency.
- Switches come in **port-side intake** or **port-side exhaust** (Cisco calls these "front-to-back"
  and "back-to-front"; check by fan/PSU colour, often blue vs red/burgundy). A ToR switch mounted
  with its ports at the rack rear (next to server NICs) needs port-side **exhaust**; one with ports
  facing the cold aisle needs port-side **intake**. Mixed directions recirculate hot air.
- Blanking panels in every empty U; brush strips for cable openings.
- Side-to-side airflow devices (some chassis) need baffles in standard racks.
- ASHRAE recommended inlet 18-27 C. Measure at the inlet (front, mid-height), not the room.

## Power
- Two PDUs per rack on separate feeds (A/B), each device's PSUs split across them.
- Load each feed to <= 40 % of breaker rating in a 2N design, so one feed can carry everything
  at <= 80 % after the other fails.
- Budget from measured or vendor "typical" power, not PSU nameplate (which overstates), but check
  PoE switches at full PoE.
- Use metered/switched PDUs for remote reboot and per-outlet monitoring; alert at thresholds.

## Cabling for airflow
Do not block exhausts with cable bundles; route on the sides; use the correct length patch leads.

## Verify
- [ ] Inlet temperatures logged per rack; A/B feed load table shows survivable single-feed failure; every device's fan direction matches its mounting.
