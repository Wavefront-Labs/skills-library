---
id: transportation-logistics.logistics-supply-chain.cold-chain-logistics.reefer-setup-and-excursion-response
name: reefer-setup-and-excursion-response
category: transportation-logistics
field: logistics-supply-chain
product: cold-chain-logistics
tags: [cold-chain-logistics, cold-chain, logistics-supply-chain, reefer, reefer-container, refrigerated-trailer, setpoint, pre-trip-inspection, pti, pre-cooling, airflow, temperature-logger, data-logger, temperature-excursion, chilled, frozen, gdp, good-distribution-practice, pharma-cold-chain, 2-8c, haccp, continuous-mode, cycle-sentry, cold-store, dock-handoff]
level: practitioner
status: draft
description: "Set up and run a reefer move: PTI, setpoint and mode by product, pre-cool the box not the cargo, airflow-safe stowage, loggers, cold-store handoffs and a temperature-excursion response."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reefer setup and excursion response — keep product in range, prove it

**Goal:** move temperature-sensitive goods (food, pharma, chemicals) so they stay inside
their specified range, with records that show it, and know exactly what to do when
they don't.

## 1. Get the specification in writing
- Setpoint and allowed range (e.g. frozen −18 °C or colder; chilled 0–4 °C;
  pharma 2–8 °C or 15–25 °C "controlled room temperature").
- Allowed excursion budget, if any (pharma stability data may allow e.g. a few hours
  outside range — only the product owner/QA can say).
- Ventilation (fresh-air exchange m³/h for respiring produce), humidity, ethylene-sensitive?
- Mode: **continuous** fan operation for chilled/fresh and pharma; cycle (start-stop)
  only for frozen goods when the shipper allows it.

## 2. Equipment before loading
1. **Pre-trip inspection (PTI)** done and recorded on the unit (reefer containers
   show PTI date; trailers have their own check). Check fuel level for gensets/trailers.
2. Set setpoint, mode, vents, and check display units (°C vs °F) — a common error.
3. **Pre-cool the empty box** to setpoint with doors closed (fresh: before loading,
   ideally loading via a sealed cold dock). Do **not** run the unit with doors open at
   a warm dock — it ices the evaporator and pulls in warm air.
4. **Product must already be at temperature.** A reefer maintains temperature; it is
   not designed to pull down warm cargo. Probe pulp/product temperature at loading
   and record it on the bill of lading/CMR.

## 3. Stowage for airflow
- Bottom-air delivery (containers): keep load on the T-floor, no plastic sheeting over
  the floor, don't block the floor at the door end; respect the **red load line** at
  the top (leave ~10+ cm for return air).
- Frozen: tight block stow is fine (air goes around). Chilled/fresh: vented cartons,
  aligned vent holes, pallets centred to avoid short-circuiting air paths.
- Fill gaps at the door end so air doesn't bypass the load.

## 4. Monitoring
- Place an independent **data logger** in the load (pharma: often one front and one
  rear, at the top/door end — the warmest zones), calibrated, set to e.g. 5–15 min intervals.
- Use telematics remote monitoring where available; alarm on setpoint deviation, unit
  shutdown, door open, power loss.
- Keep the unit download (supply/return air) as evidence alongside loggers.

## 5. Cold-store handoffs
Doors open is where excursions happen. Dock-to-dock time target (e.g. < 20–30 min for
chilled), seals intact, temperatures probed and signed at handover by both parties.

## 6. Excursion response
1. **Contain:** fix the cause (power, setpoint, doors), don't release product.
2. **Quarantine** affected stock in the system and physically label it.
3. **Collect evidence:** logger file, unit download, timeline, product temperatures.
4. **Assess** with the product owner/QA against stability data or food safety rules —
   never let logistics staff decide disposition for pharma.
5. Record CAPA (root cause and prevention); notify carrier in writing for claims.

## Gotchas
- °F/°C mix-ups on manual setpoint entry.
- Mixed loads with different setpoints in one compartment — they can't both be right.
- Reefer gensets running out of fuel over weekends at the port.
- Logger left in "sleep" or not started: no data means no proof.

## Verify
- [ ] Setpoint, mode, vents and PTI recorded at loading.
- [ ] Product temperature probed and documented before loading.
- [ ] Logger running and retrieved at destination; data reviewed before acceptance.
- [ ] Excursions quarantined and dispositioned by QA with evidence.

*Uncertainty:* stowage and ventilation details depend on unit type (container vs trailer, bottom vs top air); follow the unit manufacturer and shipper instructions.
