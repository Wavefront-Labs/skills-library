---
id: engineering-technology.biomedical-engineering.biomaterials.crosslinked-uhmwpe
name: crosslinked-uhmwpe
category: engineering-technology
field: biomedical-engineering
product: biomaterials
tags: [crosslinked-uhmwpe, uhmwpe, peek, polyethylene-liner, vitamin-e-polyethylene, oxidation-index, hip-wear, iso-5834]
level: advanced
status: verified
description: "Understand crosslinked UHMWPE bearings: radiation dose, thermal stabilisation, vitamin E, oxidation control, wear versus toughness trade-off and relevant ASTM and ISO tests."
sources: ["Kurtz, The UHMWPE Handbook: Ultra-High Molecular Weight Polyethylene in Total Joint Replacement", "ISO 5834-1 (powder form) and ISO 5834-2 (moulded forms); both were revised in 2025, confirm editions", "ASTM F2102 Standard guide for evaluating the extent of oxidation in UHMWPE fabricated forms intended for surgical implants (confirm edition)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Crosslinked UHMWPE bearing materials

**Goal:** a polyethylene bearing with low wear and adequate toughness and oxidation resistance for decades in vivo.

Regulated implant material; follow ISO 5834, ASTM standards and FDA guidance (confirm editions).

## Process
1. **Resin and consolidation:** medical-grade UHMWPE powder (ISO 5834-1) is compression moulded or ram extruded into bar or sheet.
2. **Crosslinking** by gamma or electron-beam irradiation to doses of about 50-100 kGy (gated: unconfirmed, source is paywalled or blocked) forms bonds between chains and strongly reduces adhesive and abrasive wear (simulator wear reductions of 80-90% or more are commonly reported compared with conventional polyethylene (gated: unconfirmed, source is paywalled or blocked)).
3. **Free-radical stabilisation:** irradiation leaves long-lived free radicals that cause oxidation and embrittlement. Options:
   - **Remelting** (above the melting point) quenches radicals but reduces crystallinity, strength and fatigue resistance.
   - **Annealing** (below the melting point) keeps more mechanical properties but leaves some radicals.
   - **Vitamin E (alpha-tocopherol)** blended before consolidation or diffused after crosslinking acts as an antioxidant.
4. **Machining** to bearing geometry; **sterilisation** in an inert environment (gas plasma or EO, or radiation in nitrogen or vacuum) to avoid oxidation.

## Trade-offs
Higher crosslink dose and remelting lower ultimate strength, elongation, fracture toughness and fatigue crack propagation resistance; thin liners, rim impingement and locking mechanisms are critical design areas. Document minimum thickness limits and test rim loading.

## Tests
- **Crosslink density** by swell ratio (ASTM F2214), **oxidation index** by FTIR on microtomed sections (ASTM F2102), **tensile and impact** properties, **small punch test** (ASTM F2183), **fatigue crack propagation**, and **wear** in hip and knee simulators (ISO 14242 and 14243).
- Accelerated ageing (ASTM F2003, accelerated aging after gamma irradiation in air) to assess oxidation stability.

## Verify
- [ ] Oxidation index below the acceptance limit after ageing.
- [ ] Mechanical properties meet the specification with documented margin.
- [ ] Wear rate measured in a simulator with the intended articulation and ageing.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
