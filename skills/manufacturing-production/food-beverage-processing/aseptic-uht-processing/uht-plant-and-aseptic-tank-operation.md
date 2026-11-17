---
id: manufacturing-production.food-beverage-processing.aseptic-uht-processing.uht-plant-and-aseptic-tank-operation
name: uht-plant-and-aseptic-tank-operation
category: manufacturing-production
field: food-beverage-processing
product: aseptic-uht-processing
tags: [aseptic-uht-processing, uht, ultra-high-temperature, aseptic-processing, aseptic-filling, aseptic-tank, alsafe, direct-uht, indirect-uht, steam-injection, steam-infusion, tubular-heat-exchanger, plate-heat-exchanger, holding-tube, flow-diversion, plant-sterilisation, sterile-water-circulation, sterile-barrier, steam-barrier, tetra-pak, sig, h2o2, hydrogen-peroxide, packaging-sterilisation, sterility-break, incubation-testing, commercial-sterility, fouling, intermediate-cleaning, aic, dairy, plant-based-milk, food-processing]
level: practitioner
status: draft
description: "Run a UHT line and aseptic tank: plant pre-sterilisation, product changeover, holding-tube temperature control, sterile barriers, aseptic filler links, fouling and recognising a sterility break."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# UHT plant and aseptic tank operation

**Goal:** keep everything downstream of the holding tube commercially sterile for the
whole run — from plant sterilisation through product, any aseptic tank buffer, to the
filler — and recognise when sterility has been lost.

## 1. Sequence of a run
1. **Plant pre-sterilisation**: circulate hot water (pressurised) through the sterile
   side at sterilisation temperature (commonly ~130–140 °C for ~30 min — plant-specific)
   to sterilise everything after the holding tube, including the aseptic tank and filler
   connections where on-line.
2. **Cool to production temperature on sterile water**; plant runs on water ("sterile water circulation").
3. **Product changeover**: product displaces water; mix-phase is diverted to drain/
   a mix tank until product concentration is stable (Brix or density sensor/time).
4. **Production**: product heated (direct steam injection/infusion or indirect via
   tubular/plate exchangers) to e.g. 137–145 °C, held for a few seconds in the **holding
   tube**, cooled and sent to the filler or aseptic tank.
5. **End of run**: product chased out with water, then CIP; or an **intermediate
   cleaning (AIC)** that removes fouling without losing sterility, to extend run time.

## 2. Holding tube and flow diversion
- Sterilisation temperature is measured at the **end of the holding tube**; if it drops
  below the set point the plant must **divert** (send product back/away, not forward)
  and in most designs lose sterile status — requiring re-sterilisation.
- Holding time depends on flow rate: never run above the validated maximum flow.
- Positive pressure on the sterile side relative to the non-sterile side in regenerative
  sections, so a pinhole leak goes the right way.

## 3. Sterile barriers
Valves, pump seals and the aseptic tank's inlets/outlets are protected by **steam or
sterile-water barriers**. A barrier temperature alarm means the barrier may have been breached:
- Treat it as a potential sterility break until assessed; follow the plant's alarm
  matrix (some alarms require stopping production and re-sterilising).
- Check steam traps on barriers during walk-rounds — a failed trap is a cold barrier.

## 4. Aseptic tank
- Buffers product between UHT and filler (allows filler stoppages, two fillers, or
  running products in parallel).
- Sterilised with steam and kept under **sterile air overpressure** (through sterile filters).
- Track **hold time** of product in the tank against the limit; check tank pressure,
  level and sterile-air filter status. Filter integrity tests per schedule.

## 5. Aseptic filling interface
- Fillers (Tetra Pak, SIG, Elopak and bottle-based ABF) sterilise packaging (typically
  hydrogen peroxide bath or spray + hot air) and keep a sterile zone under overpressure.
- H2O2 concentration and temperature, sterile zone pressure, and residual H2O2 in packs are checked as specified.
- **Incubation**: samples from start, end and around every stop/splice incubated (e.g.
  30 °C for ~5–7 days, plant-specific) and checked by pH/visual or rapid methods before release.

## 6. Fouling and running time
- Watch heater **temperature difference/pressure drop** rising — milk proteins and
  minerals foul indirect heaters. When the medium temperature needed to hold product
  temperature exceeds a limit, plan an AIC or stop for CIP.
- High-protein and plant-based products foul faster.

## Gotchas
- Restarting after a divert without re-sterilising "because it was only a few seconds".
- Mix-phase sent forward, giving diluted packs.
- Holding tube temperature probe drifting — compare against the reference probe as scheduled.
- Ignoring a hissing steam barrier because product still looks fine.
- Incubation samples not taken around a filler stop.

## Verify
- [ ] Plant sterilisation chart shows required temperature and time on the sterile side.
- [ ] Holding tube temperature stayed above set point; every divert recorded and handled.
- [ ] Barrier alarms none, or each assessed per alarm matrix.
- [ ] Aseptic tank hold time, overpressure and sterile filter status within limits.
- [ ] Incubation samples taken at start, end and every stop; results released before shipment.
