---
id: repair-maintenance.marine-vessel-repair.marine-diesel-repair.fuel-system-bleeding-and-filter-service
name: fuel-system-bleeding-and-filter-service
category: repair-maintenance
field: marine-vessel-repair
product: marine-diesel-repair
tags: [marine-diesel-repair, marine-diesel, diesel-bleeding, air-in-fuel, fuel-filter, racor, primary-filter, secondary-filter, water-separator, lift-pump, injection-pump, bleed-screw, yanmar, volvo-penta, beta-marine, perkins, westerbeke, nanni, diesel-bug, fuel-polishing, vacuum-gauge, hard-starting, engine-dies]
level: practitioner
status: draft
description: "Change marine diesel fuel filters and bleed air out: primary/secondary sequence, bleed screws in order, lift-pump priming, vacuum-gauge diagnosis of blocked filters, and diesel bug control."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Fuel system bleeding and filter service — marine diesel

**Goal:** clean fuel and no air between tank and injectors. Most marine diesel
"failures" at sea are fuel: blocked filters after rough weather stirs the tank, water,
diesel bug, or air drawn in after a filter change.

## Fuel path (typical small marine diesel)
Tank → fuel pickup → shut-off valve → **primary filter/water separator** (e.g. Racor
spin-on or bowl type, usually 10–30 µm) → **lift pump** (mechanical, with hand-priming
lever, or electric) → **secondary/engine filter** (finer, ~2–10 µm) → **injection pump**
→ high-pressure lines → injectors → return line to tank.

## 1. Filter change
1. Engine off and cool; close the fuel shut-off. Absorbent pads and a container under
   the filters; diesel in the bilge goes overboard with the bilge pump — don't let it.
2. **Primary**: drain water from the bowl first (look for water, black slime/sludge =
   diesel bug). Replace element/spin-on; lube the seal with clean diesel; hand-tight
   per the filter's instructions. **Pre-fill** a spin-on with clean fuel if the design
   allows (only from the dirty/outer side).
3. **Secondary (engine) filter**: same approach; on many engines pre-filling isn't
   possible — you'll bleed it.
4. Open the fuel valve. Check for leaks at seals.

## 2. Bleeding sequence (work downstream, one point at a time)
General order — details and bolt positions are in the engine manual:
1. **Primary filter**: some have a bleed screw or T-handle; open slightly, pump the
   lift pump (or the filter's primer), close when bubble-free fuel flows.
2. **Secondary filter bleed screw**: open 1–2 turns, operate the lift pump hand lever
   (if the lever has no stroke, turn the engine over a little to move the cam lobe off the
   lever) until fuel flows **free of bubbles**, then close while still pumping.
3. **Injection pump bleed screw(s)** — same procedure.
4. Many modern small diesels (Yanmar GM/YM, Beta, Volvo D1/D2) are **self-bleeding from
   the injection pump** after the filter is bled; crank for 10–15 s bursts, rest
   between to protect the starter.
5. Still won't start: crack an **injector line nut** at the injectors (one or two flats),
   throttle full, decompress if fitted, crank until fuel spits, tighten. Wrap with rag —
   **high-pressure fuel can penetrate skin; never put hands near a cracked injector line
   while cranking.**
Electric lift pumps: switch ignition to "on" (or run the pump) for 30–60 s and bleed
the same points.

## 3. Diagnosing restriction with a vacuum gauge
Fit a vacuum gauge on the outlet of the primary filter (some Racor housings have a
port). At cruise:
- ~0–2 inHg: clean.
- Rising past roughly **5–7 inHg** (check the filter maker's figure): filter loading —
  plan a change.
- Climbing high quickly after rough weather: tank debris; change and expect to repeat.
A vacuum reading near zero with fuel starvation symptoms points at **air leaks**
(loose fittings, cracked filter bowl, worn shaft seal on the valve) — look for bubbles
in a clear section of line.

## 4. Water and diesel bug
- Drain the separator every few engine hours of operation, and before departure.
- Black/brown slime or a sour smell = microbial growth at the fuel–water interface.
  Treat with a **biocide** at the shock dose, then change filters (it'll block them),
  and consider **fuel polishing** (circulating tank fuel through filters) or tank
  cleaning.
- Prevention: keep tanks full over winter (less condensation), buy fuel from busy
  outlets, check deck-fill O-rings and tank vents for water ingress.

## Gotchas
- Air leaks on the **suction** side don't drip — they suck. A filter that leaks only
  when the engine's off is still a candidate.
- Over-tightening a spin-on filter crushes the seal; under-tightening lets air in.
- Starter motors overheat on long cranking: 15 s on, 30–60 s off.
- Carry two of every filter and a way to bleed (the right spanner) on board.

## Verify
- [ ] Filters changed, seals lubricated, no leaks with the fuel valve open.
- [ ] Each bleed point closed only after bubble-free fuel; started within a few cranks.
- [ ] Engine runs at full load for 20+ min without hunting or dying.
- [ ] Vacuum gauge baseline recorded for this new filter.
- [ ] Separator bowl clear of water and sludge after the run.

*Draft: bleed point locations and self-bleeding behaviour vary by engine — use the manual.*
