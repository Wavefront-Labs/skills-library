---
id: engineering-technology.industrial-design.cmf-design.cmf-specification
name: cmf-specification
category: engineering-technology
field: industrial-design
product: cmf-design
tags: [industrial-design, cmf-design, cmf, colour-material-finish, color-material-finish, colour-matching, color-matching, cielab, delta-e, gloss, gloss-units, vdi-3400, spi-finish, mold-tech, texture, anodising, anodizing, pvd, soft-touch-paint, in-mould-decoration, imd, pad-printing, laser-etching, ral, pantone, ncs, metamerism, cmf-board, finish-specification, colour-master, light-booth]
level: practitioner
status: draft
description: "Specifying colour, material and finish: material expression, texture (VDI/MT) and finish processes, colour standards, tolerances and a CMF spec sheet."
sources: ["Becerra, CMF Design: The Fundamental Principles of Colour, Material and Finish Design", "Ashby & Johnson, Materials and Design", "Thompson, Manufacturing Processes for Design Professionals", "VDI 3400 texture reference", "SPI mould finish guide", "ISO 2813 / ASTM D523 gloss measurement", "CIE colour-difference formulae (CIELAB, CIEDE2000)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# CMF specification — from mood board to a finish the factory can hit

**Goal:** choose colour, material and finish that express the product and survive
use, then document them so tooling, suppliers and quality control produce the same
result every time.

## 1. Start from intent and use
- Write the **material story** in a sentence ("tool-like and durable", "warm, soft,
  domestic"). Every CMF choice should serve it.
- Map **zones**: primary body, secondary/accent, touch points, interface (buttons,
  lenses), branding. Typically 1 primary + 1-2 accents.
- List the **use conditions**: abrasion, hand oils and sunscreen, UV, cleaning
  chemicals, drops, temperature. These knock out finishes before aesthetics do.

## 2. Material and process expression

| Look/feel | Typical process route |
|---|---|
| Fine matte plastic | moulded texture (VDI / Mold-Tech) on the tool |
| High gloss plastic | polished tool (SPI A-grade) or IMD/IML film |
| Soft, warm touch | 2K overmould TPE, or soft-touch PU paint |
| Premium metal | aluminium, bead-blast + anodise (Type II for colour) |
| Hard-wearing metal | hard anodise (Type III), PVD, powder coat |
| Graphics, icons | pad print, screen print, laser etch, IMD |
| Wood/textile | real material, laminate or printed IMD |

Moulded-in colour is cheaper and scratch-tolerant; paint opens colours and effects
but adds cost and a wear risk.

## 3. Texture and gloss
- Mould textures by reference: **VDI 3400** (grade = 20·log10(Ra / 0.1 µm), so VDI 12 ~ Ra 0.4 µm,
  VDI 30 ~ Ra 3.2 µm, VDI 45 ~ Ra 18 µm) and supplier
  pattern codes (e.g. Mold-Tech MT-xxxx).
- **SPI** finishes: A-1 to A-3 polished (diamond buff), B paper, C stone, D blasted.
- Deeper texture needs more **draft**: roughly 1-1.5° extra per 0.025 mm depth; confirm on
  the texture supplier's chart (see enclosure-design).
- Specify **gloss** in gloss units with geometry: 60° for most; 20° for high gloss
  (>70 GU at 60°); 85° for very matte (<10 GU at 60°), per ISO 2813 / ASTM D523.

## 4. Colour
- Reference a system for communication (Pantone, RAL, NCS), then make a **physical
  master** (plaque) in the **production resin and texture**: the same code looks different
  in ABS, PC and paint, and on gloss vs matte.
- Measure with a spectrophotometer in **CIELAB**; tolerance with **ΔE*ab or ΔE2000**.
  Typical targets: ΔE <= ~1.0 for parts that sit side by side, <= ~2.0 for separated parts;
  agree the formula and values with suppliers.
- Approve in a **light booth** under D65 plus a second illuminant (e.g. store lighting
  such as TL84, or incandescent A) to catch **metamerism**.

## 5. The CMF spec sheet (one row per part)
Part name/number · material grade (and colourant) · colour reference + master ID ·
ΔE tolerance · finish/texture code + depth · gloss (GU @ angle) · decoration process
and artwork file · durability tests (abrasion, adhesion cross-hatch, chemical, UV) ·
image of the zone. Version it like a drawing; changes need sign-off.

## Gotchas
- Texture makes colour look lighter and less saturated; approve colour on the textured
  plaque.
- Metallic/effect resins show flow and knit lines; gate location matters, check with the
  moulder.
- Anodised colour varies with alloy; cast high-silicon alloys go dull grey.
- Soft-touch paints can turn sticky with age and chemicals; test before committing.
- Dark gloss shows every scratch and fingerprint; most handheld products avoid it on
  touch zones.
- Screen and render colours aren't a standard; only measured physical masters are.

## Verify
- [ ] Every zone has a material, colour master, texture code and gloss value.
- [ ] Colour approved on production resin and texture under two illuminants.
- [ ] ΔE formula and tolerances agreed with each supplier.
- [ ] Texture depth reconciled with part draft.
- [ ] Durability tests listed and passed for the use conditions.
