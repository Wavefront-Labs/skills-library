---
id: manufacturing-production.assembly-line-hand-work.wire-harness-assembly.crimping-routing-and-testing-a-harness-to-ipc-whma-a-620
name: crimping-routing-and-testing-a-harness-to-ipc-whma-a-620
category: manufacturing-production
field: assembly-line-hand-work
product: wire-harness-assembly
tags: [wire-harness-assembly, assembly-line-hand-work, wire-harness, cable-assembly, ipc-whma-a-620, crimping, crimp-terminal, crimp-height, pull-test, pull-force, bellmouth, conductor-brush, insulation-crimp, wire-stripping, strip-length, formboard, harness-board, routing, breakout, taping, convoluted-tube, cable-ties, connector-population, terminal-retention, tpa, cpa, continuity-test, harness-tester, hipot]
level: practitioner
status: draft
description: "Build wire harnesses on a formboard: strip and crimp terminals to spec (crimp height, pull test, visual), route and dress breakouts, populate connectors with retention checks, and electrically test."
sources: ["IPC/WHMA-A-620 Requirements and Acceptance for Cable and Wire Harness Assemblies"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Crimping, routing and testing a harness to IPC/WHMA-A-620

**Goal:** a harness where every wire is the right one, in the right cavity, with a
crimp that is electrically and mechanically sound, routed so it fits the product and
survives vibration. IPC/WHMA-A-620 is the acceptance standard (paid; this paraphrases
practice). The **terminal manufacturer's application spec** sets the actual numbers.

## 1. Cutting and stripping
- Cut to the length on the drawing/cut list; mark or label wires as specified.
- **Strip length** from the terminal spec — too short and the conductor doesn't reach
  through the crimp; too long and bare wire shows past the insulation crimp or causes
  shorts.
- Inspect the strip: **no nicked or cut strands** (the standard limits damaged
  strands), insulation cut clean, no strands splayed. Twist stranded wire gently only
  if the spec allows.
- Check stripper blade setting per wire gauge; a dull blade or wrong die nicks strands.

## 2. Crimping
Use the **specified tool or applicator** for that terminal and wire gauge (a ratchet
hand tool that won't release until fully closed, or a bench press with an applicator).
A good open-barrel crimp shows, in order from the front:
- **Conductor brush** — strands just visible beyond the conductor crimp.
- **Conductor crimp** — wings rolled in evenly, no strands outside.
- **Bellmouth** — small flare at the rear edge of the conductor crimp (no sharp edge to
  cut strands).
- **Inspection window** — conductor *and* insulation both visible between the two
  crimps.
- **Insulation crimp** — grips the insulation without piercing it (for insulation
  support types).
**Crimp height** is the key measurable: measure across the conductor crimp with a crimp
micrometer (pointed anvil) and compare to the terminal spec, at setup, after
applicator/reel changes and at the interval set (sampling). **Pull test** to the
specified minimum force for the gauge on setup samples; it is destructive.
Crimp-force monitors on presses flag bad crimps automatically — never override a
reject.

## 3. Routing on the formboard
- The formboard is a 1:1 layout of the harness with pegs/forks, breakout points and
  connector holders. Lay wires in the sequence on the board instructions, usually
  longest/main trunk first.
- Keep wires parallel in the bundle without crossing where the drawing says so; route
  round pegs with the specified bend radius (often a multiple of bundle diameter —
  check the drawing).
- **Dress:** tape (spot or spiral as specified), cable ties at the specified spacing and
  tension with a tension-controlled tie gun (over-tight ties deform insulation),
  convoluted tube or sleeving where called up. Breakout positions within the drawing
  tolerance.

## 4. Populating connectors
- Insert each terminal into the cavity on the drawing (watch the cavity numbering on
  the connector face — it can be mirrored between mating and wire sides).
- Push until it **clicks**, then **push-back/pull test** each terminal gently to confirm
  the retention lance engaged.
- Close the **TPA** (terminal position assurance) and later the **CPA** (connector
  position assurance) where fitted; a TPA that won't close means a terminal is not
  fully seated.
- Unused cavities: seal plugs where sealed connectors require them.

## 5. Electrical test
- A **harness tester** (continuity/short, sometimes hipot and insulation resistance)
  checks every circuit against the netlist. Many testers also detect seated
  terminals and TPA. Pass = label and log the serial; fail = locate, repair per the
  approved method (some customers forbid repairs) and retest the whole harness.
- Hand probing with a meter misses intermittent and wrong-but-continuous faults.

## Gotchas
- Mixing a terminal with a near-identical one from another supplier: different
  crimp heights.
- Re-crimping a bad crimp is not allowed — cut and redo.
- Soldering a crimp "to be sure" makes the wire brittle at the joint; not allowed
  unless specified.

## Verify
- [ ] Strip length right, no damaged strands.
- [ ] Crimp height within spec; setup pull test passed; visual features all present.
- [ ] Routing, breakouts and tie spacing match the drawing.
- [ ] Every terminal push-back tested; TPA/CPA closed.
- [ ] 100% electrical test passed and logged.
