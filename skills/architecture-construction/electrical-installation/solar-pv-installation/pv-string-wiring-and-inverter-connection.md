---
id: architecture-construction.electrical-installation.solar-pv-installation.pv-string-wiring-and-inverter-connection
name: pv-string-wiring-and-inverter-connection
category: architecture-construction
field: electrical-installation
product: solar-pv-installation
tags: [electrical-installation, solar-pv-installation, solar-pv, photovoltaic, pv-string, string-sizing, voc, isc, temperature-coefficient, mc4, pv-connector, pv-wire, dc-isolator, ac-isolator, inverter, microinverter, rapid-shutdown, grid-connect, anti-islanding, string-fuse, nec-690, as-nzs-5033, as-nzs-4777, g98, lockout-tagout]
level: practitioner
status: draft
description: "Wire rooftop PV strings to an inverter: cold-Voc string sizing, connector and polarity checks, DC/AC isolation and shutdown order, rapid shutdown, pre-energise tests."
sources: ["NFPA 70 National Electrical Code (NEC) Article 690", "AS/NZS 5033 Installation and safety requirements for photovoltaic arrays", "AS/NZS 4777.1 Grid connection of energy systems via inverters", "IEC 62446-1 PV systems - testing, documentation and maintenance", "BS 7671 Section 712"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# PV string wiring and inverter connection

**Goal:** connect rooftop module strings to a grid-connected inverter so that the DC
voltage never exceeds equipment ratings on the coldest morning, polarity is right
before anything is plugged in, and the system can be isolated and shut down safely.

> **Licensed, jurisdiction-specific work.** PV installation typically needs both an
> electrical licence and a PV-specific accreditation (e.g. AU SAA/CEC-style
> accreditation, UK MCS, US NABCEP is common but local licensing rules), plus network
> approval before connection. Figures are typical; confirm against your edition of the
> wiring rules, PV standard and the inverter datasheet.

## 1. Know the hazard: you can't switch the array off
Modules produce voltage whenever light falls on them; a string can be at several
hundred volts DC at dawn. DC arcs don't self-extinguish at a current zero the way AC
arcs do. Rules that follow:
- Never connect or disconnect a PV connector **under load**.
- Shutdown order: **AC isolator off first** (inverter stops drawing current), then the
  **DC isolator**. Start-up in reverse: DC on, then AC.
- Work at heights under your fall-protection plan; roof work is the bigger statistical risk.

## 2. Size the string
- **Max voltage:** Voc(cold) = Voc(STC) × [1 + |β_Voc| × (25 − T_min)], with β_Voc the
  module's temperature coefficient (e.g. −0.27 %/°C) and T_min the record low site
  temperature. String Voc(cold) × modules ≤ inverter max DC input and the module's
  system voltage rating. Typical limits: US residential 600 V, AU domestic 600 V
  (unverified — confirm against your edition of the wiring rules), commercial 1000/1500 V.
- **MPPT window:** string Vmp at hot cell temperature (often 60–70 °C) must stay above
  the inverter's minimum MPPT voltage.
- **Current:** design current commonly taken as 1.25 × Isc (US applies a further 1.25 for
  conductor sizing). Parallel strings: string fuses usually needed at three or more in
  parallel, sized per the module's maximum series fuse rating.

## 3. Wire the strings
- Use PV-rated cable (PV1-F / H1Z2Z2-K / US "PV wire") of adequate size (4–6 mm² /
  10–12 AWG common), UV-resistant, supported off the roof surface; no cable lying in
  water paths or across sharp edges.
- Connectors: **mate only identical make and type** (genuine MC4 to genuine MC4) and
  crimp with the maker's tool; mismatched "compatible" connectors overheat.
- Keep positive and negative of each string close together to limit loop area (lightning
  induced surges).
- Bond module frames and rails to earth as the rules and racking instructions require.
- US: fit **rapid shutdown** devices so conductors inside the array boundary fall to ≤80 V
  within 30 s of initiation (NEC 690.12).

## 4. Test before connecting to the inverter (per IEC 62446-1)
With DC isolator **open** and the string unplugged at the inverter end:
1. **Polarity** of each string with a DC-rated meter (CAT III 1000 V DC or higher).
2. **Voc** of each string — within a few percent of the expected value for irradiance
   and temperature; a low reading means a missing/reversed module.
3. **Isc** with a PV tester (not a multimeter's amps range).
4. **Insulation resistance** positive and negative to earth at 500 V or 1000 V DC per
   system voltage, with surge devices disconnected.
Record all results per string.

## 5. AC connection
1. Isolate the board way (or main) for the inverter circuit: **lock off, tag, prove the
   tester, test dead, re-prove**.
2. Install the dedicated circuit, AC isolator near the inverter if required, and the
   inverter's protection settings for the local grid code (AU AS/NZS 4777.2 region setting,
   UK G98/G99, US IEEE 1547 / UL 1741).
3. Fit all mandatory labels: dual-supply warning at the board and meter, DC isolator
   labels, shutdown procedure.

## 6. Commission
DC isolator on → AC isolator on → confirm inverter syncs, check each MPPT voltage and
current, test the anti-islanding/shutdown function (open AC, inverter must stop).

## Gotchas
- Cold-weather Voc over the inverter limit destroys inputs on the first frosty sunrise.
- Reversed string in parallel back-feeds other strings.
- Opening a DC isolator rated only for AC, or one not rated for the string voltage, arcs.
- Water ingress in rooftop isolators is a known fire cause — mount and gland to the maker's orientation.

## Verify
- [ ] Voc(cold) per string below inverter and module limits; Vmp(hot) above MPPT minimum.
- [ ] Connectors genuine, same type, factory-crimped.
- [ ] Polarity, Voc, Isc and IR recorded per string before connection.
- [ ] AC side isolated, locked off and proved dead before termination.
- [ ] Shutdown sequence (AC then DC) labelled; rapid shutdown works where required.
- [ ] Grid-protection settings match the network's requirements.
