---
id: agriculture-environment.livestock-farming.farm-fencing.strainer-assembly-and-electric-fence-testing
name: strainer-assembly-and-electric-fence-testing
category: agriculture-environment
field: livestock-farming
product: farm-fencing
tags: [farm-fencing, fencing, strainer-post, end-assembly, h-brace, box-brace, diagonal-stay, brace-wire, high-tensile-wire, wire-tension, ratchet-strainer, tension-spring, electric-fence, energiser, energizer, joules, earth-system, ground-rods, fence-tester, digital-voltmeter, fault-finder, insulators, offset-wire, polywire, livestock-fence, gate-hanging]
level: practitioner
status: draft
description: "Build a braced strainer assembly that holds wire tension, and set up and fault-find an electric fence with energiser sizing, earth testing and voltage checks."
sources: ["Gallagher and Speedrite electric fencing manuals (summary)", "University extension and state agriculture fencing guides (e.g. Agriculture Victoria, NRCS Conservation Practice 382 Fence)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Strainer assemblies and electric fence testing

**Goal:** fence ends that never lean or pull out (they hold *all* the wire tension), and
an electric fence that delivers a deterrent shock at the far end, with faults found fast.

## Part A — Braced strainer (end) assembly

### Why it fails
A wire fence pulls each end post with hundreds of kg per wire; eight high-tensile wires at
~100–150 kg each is over a tonne. An unbraced post leans; a badly braced one lifts out.

### The H-brace (horizontal stay) — common robust design
1. **Strainer post:** large (e.g. ~150–200 mm diameter treated timber or equivalent steel),
   set **≥ 1.0–1.2 m deep** (deeper in soft soil); tamp in layers, compacting each 10–15 cm.
2. **Brace (stay) post:** a second post of similar size set in line **~2–2.5 m away**
   — a horizontal stay length about **2–2.5 × the height above ground** works well; short
   stays are the commonest error.
3. **Horizontal stay rail** between them, near the top (about 2/3 to 3/4 of the fence
   height), notched or pinned into both posts.
4. **Diagonal tension wire:** a double loop of high-tensile wire from the **top of the
   brace post down to the bottom of the strainer post**, twisted tight with a stick until
   the assembly is rigid. Pin it in place. (The fence pulls the strainer top toward the
   brace post; the rail passes that push to the brace post, and the diagonal wire ties
   the brace post's top back to the strainer's foot.)
5. For long or heavily tensioned runs, double the bay (strainer + two brace posts).
   A diagonal-stay design (stay from strainer top to a ground block/foot) is an
   alternative; follow your local fencing guide for sizes.

### Tensioning the wire
- High-tensile wire (2.5 mm) is commonly tensioned to roughly **90–135 kg (200–300 lbf)**
  per wire; use a **tension indicator spring** or the manufacturer's gauge, not "feels tight".
- Use in-line ratchet strainers so you can retension seasonally (wire slackens in heat,
  tightens in cold).
- Tie off with a proper knot or crimp sleeves; fit end-strain insulators on electrified lines.

## Part B — Electric fence

### Energiser sizing
Rule of thumb from makers: roughly **1 joule of output (stored) energy per ~10 km of
single-wire fence** under light weed load; more for weeds, multiple wires or long runs.
Mains-powered units are stronger than battery/solar units. Follow the brand's sizing chart.

### Earth system (half the circuit — most faults are here)
- Use **galvanised earth rods ~1.5–2 m long**, at least **3 rods spaced ~3 m apart**
  (more in dry or sandy soils), connected with continuous galvanised wire and proper
  clamps; well away (≥ ~10 m) from building and utility earths.
- **Earth test:** create a deliberate short on the fence ~100 m from the energiser
  (lean steel posts against the live wire) to pull the fence voltage down to ~2 kV or less;
  then measure voltage between the earth rod and a separate probe pushed in ~1 m away.
  Reading should be **≤ ~0.2–0.3 kV**. Higher → add rods, water them, or improve
  connections.

### Voltage targets
Measure with a **digital fence voltmeter** (not a neon tester), probe in the soil away
from the earth rods:
- Commonly suggested minimum: **~3–4 kV** for cattle and horses; **~5 kV+** for sheep and
  goats (wool and hair insulate); more for predators. Check at the far end, not just at
  the energiser.

### Fault finding
1. Read voltage at the energiser terminals (disconnected from fence) — confirms the unit.
2. Reconnect; read along the fence. A **fault finder/current meter** shows amps and an
   arrow pointing toward the fault (the short draws current). Follow the current.
3. Typical faults: broken/cracked insulators, wire touching steel posts, vegetation,
   broken wire joints (use proper joint clamps; knots arc), lead-out cable cracked
   under a gate, lightning-damaged energiser. Fit **cut-out switches** to isolate sections.
4. Gates: run the live wire **underground in double-insulated cable** inside conduit.

## Gotchas
- The diagonal wire in an H-brace must run from the top of the brace post down to the
  bottom of the strainer post — the other diagonal would be in compression, which wire
  can't take, so the brace does nothing. Draw it before you build.
- Barbed wire must **never** be electrified.
- Sizes and tensions are typical guide values, **unconfirmed for your wire, soil or
  energiser** — follow your wire and energiser manufacturer.

## Verify
- [ ] Strainer posts don't move when wires are tensioned (sight down the fence).
- [ ] Wire tension measured with an indicator; strainers allow retensioning.
- [ ] Earth test ≤ ~0.3 kV with the fence shorted.
- [ ] Far-end voltage meets the target for the species.
- [ ] Cut-out switches and a fault finder available; faults logged and fixed.
