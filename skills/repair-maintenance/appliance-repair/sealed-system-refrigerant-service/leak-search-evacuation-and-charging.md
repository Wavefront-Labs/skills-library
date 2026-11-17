---
id: repair-maintenance.appliance-repair.sealed-system-refrigerant-service.leak-search-evacuation-and-charging
name: leak-search-evacuation-and-charging
category: repair-maintenance
field: appliance-repair
product: sealed-system-refrigerant-service
tags: [appliance-repair, sealed-system-refrigerant-service, refrigerant, r600a, isobutane, r134a, r290, epa-608, f-gas, refrigerant-recovery, piercing-valve, process-tube, leak-detection, nitrogen-pressure-test, vacuum-pump, micron-gauge, triple-evacuation, filter-drier, brazing, lokring, charge-by-weight, compressor-replacement, capillary-tube]
level: advanced
status: docs-checked
description: "Domestic fridge sealed-system work: recover refrigerant, find leaks, braze or Lokring joints, change drier/compressor, evacuate to 500 microns, charge by weight. Licensed techs only (EPA 608/F-gas)."
sources: ["https://www.epa.gov/section608/section-608-technician-certification-requirements", "https://www.epa.gov/section608/stationary-refrigeration-service-practice-requirements"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Leak search, evacuation and charging

**Goal:** repair a domestic refrigerator/freezer sealed system (leak, restriction, failed
compressor) so it holds a correct, weighed charge for years. **Legal:** in the US, opening
a system requires EPA Section 608 certification (Type I covers small appliances);
elsewhere check local certification (for example F-gas in the EU/UK) and hydrocarbon
(R600a/R290) handling training. EPA Section 608 bars intentional venting (a de minimis
exception covers good-faith recovery); hydrocarbons are flammable. This is a method outline for
trained technicians.

## 1. Identify the system
Data plate: refrigerant type and **charge mass** (e.g. "R600a 55 g"). Hydrocarbon
appliances (most new European and many new US fridges) need spark-free tools,
ventilation, and no brazing until the system is purged with nitrogen.

## 2. Access and recovery
1. Fit a **piercing/saddle valve** or bullet valve on the compressor process tube (and the
   high side if needed). Many small systems have no service valves.
2. Recover HFC refrigerant (R134a etc.) with a recovery machine into a recovery
   cylinder; record the amount. For small appliances (5 lb or less), EPA sets recovery of 90% of
   the refrigerant when the compressor works and 80% when it does not, or evacuation to
   4 inches of mercury vacuum; system-dependent (passive) methods are allowed for
   Type I — check current rules.
3. Hydrocarbons: recover or, where local regulation allows, controlled venting outdoors
   through a hose, away from ignition sources; then **purge with oxygen-free nitrogen
   (OFN)** before any brazing.

## 3. Find the leak
- Pressurise with dry nitrogen (to the appliance maker's test pressure — never exceed the low-side rating).
- Bubble solution on joints; electronic leak detector (for HFC, or a trace of refrigerant
  mixed with nitrogen if permitted); listen for hiss. Common spots: process-tube welds,
  evaporator (punctured by ice picks), condenser loops in foam (often unrepairable —
  bypass with an external condenser), ice-maker water line chafe on tubing.
- Standing pressure test: hold for 15–30 min (longer for slow leaks) with a temperature
  note; no drop beyond temperature effect.

## 4. Repairs and component replacement
- **Always replace the filter drier** whenever the system is opened, with the right
  desiccant for the refrigerant; install it vertically, outlet
  (capillary) down where specified.
- Joints: braze copper–copper with a suitable phosphor-copper rod
  while flowing a trickle of nitrogen to prevent internal oxide scale; copper–steel or
  aluminium joints, or any hydrocarbon unit where brazing is unwise: **Lokring**
  mechanical connectors with their sealant.
- Compressor replacement: match refrigerant, capacity (BTU/h or W at the rated condition),
  voltage, start type; replace the start relay/overload kit supplied with it.
- Capillary restriction: cut the cap tube just before the drier and check flow; blocked
  capillaries are cleared with a cap-tube cleaner or the cap is replaced (length and bore
  must match).

## 5. Evacuate
- Vacuum pump with fresh oil, short large-bore hoses, core removal tools if valves exist.
- Pull to the vacuum level the appliance maker specifies, read on a **micron gauge** (not a compound gauge — they can't read it).
- Isolate and watch: rising and levelling = moisture still boiling
  (keep pumping/heat gently); steadily rising to atmosphere = leak.
- **Triple evacuation** (vacuum, break with nitrogen, repeat ×3) helps on wet systems.

## 6. Charge by weight
- Small systems have tiny charges: a few grams wrong changes performance. Charge **by
  weight** on a digital scale to the data plate, as liquid for blends,
  through a charging hose that has been purged.
- For hydrocarbon systems, use a cylinder and gauge set rated for HC, then crimp and
  braze/Lokring-seal the process tube (pinch-off tool, then seal).
- Run 24 h; check frost line on the evaporator (full coil frosting evenly), suction-line
  temperature near ambient at the compressor (no frost back), cabinet temperatures.

## Gotchas
- Overcharging shows as frost/sweat back down the suction line to the compressor.
- Moisture → ice at the capillary outlet → intermittent cooling weeks later.
- Brazing an uncleared HC system = fire/explosion risk.
- Uncertain: pressure limits and recovery rules vary by jurisdiction and maker; confirm current regulations.

## Verify
- [ ] Technician certified for the refrigerant/jurisdiction; recovery recorded.
- [ ] Leak located and repaired; nitrogen standing test held.
- [ ] Filter drier replaced; joints brazed under nitrogen or Lokringed.
- [ ] Vacuum to the maker's level held on decay test.
- [ ] Charge weighed to the data plate; evaporator frosts evenly, no flood-back after 24 h.

## Checked

Date checked: 2026-10-25. Jurisdiction: United States (EPA Section 608); other jurisdictions need their own certification (for example F-gas in the EU and UK).
EPA Section 608 pages: Type I certification covers servicing small appliances (5 lb or less of refrigerant); small appliance recovery is 90 percent when the compressor works and 80 percent when it does not (one EPA page ties this to the equipment date), or evacuation to 4 inches of mercury vacuum; intentional venting is prohibited with a de minimis exception for good-faith recovery. Removed unconfirmed figures: nitrogen test pressure, desiccant and brazing rod brands and silver content, vacuum target in microns and the moisture plateau range, scale resolution. The skill now defers to the appliance maker for those values.

Method: documentation only; no commands were run.
