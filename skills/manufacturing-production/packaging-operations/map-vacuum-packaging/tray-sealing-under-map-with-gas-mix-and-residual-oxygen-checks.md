---
id: manufacturing-production.packaging-operations.map-vacuum-packaging.tray-sealing-under-map-with-gas-mix-and-residual-oxygen-checks
name: tray-sealing-under-map-with-gas-mix-and-residual-oxygen-checks
category: manufacturing-production
field: packaging-operations
product: map-vacuum-packaging
tags: [map-vacuum-packaging, packaging-operations, map, modified-atmosphere-packaging, gas-flush, gas-mix, nitrogen, carbon-dioxide, co2, oxygen, high-oxygen-map, residual-oxygen, headspace-analyser, gas-analyser, tray-sealer, thermoformer, vacuum-packaging, vacuum-chamber, vacuum-skin-pack, vsp, lidding-film, barrier-film, evoh, seal-integrity, leak-detection, shelf-life, gas-mixer]
level: practitioner
status: draft
description: "Pack under modified atmosphere or vacuum: pick gas mixes by product, set vacuum/flush/seal on tray sealers and thermoformers, test headspace O2/CO2, and catch leaks before they cost shelf life."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Tray sealing under MAP with gas mix and residual-oxygen checks

**Goal:** every sealed pack has the specified atmosphere (or vacuum) and stays sealed,
because shelf life on the label assumes it does. A leaking MAP pack looks normal on the
line and spoils early in the store.

## 1. Gas mixes — what each gas does
- **CO₂** inhibits many bacteria and moulds; dissolves into moist/fatty product, so packs
  can collapse slightly ("pack collapse") — allow headspace.
- **N₂** inert filler, displaces oxygen, prevents collapse.
- **O₂** usually excluded (oxidation, aerobic spoilage), but kept **high** in red-meat
  packs to hold the red colour.
Typical published starting points (always follow your product specification):
red meat ~70% O₂ / 30% CO₂; poultry and many cooked meats ~30% CO₂ / 70% N₂; cheese and
bakery high CO₂ or CO₂/N₂; salads and cut produce low O₂ with breathable film.
Gas is food-grade; check cylinder/bulk supply labels at changeover — a wrong cylinder is
a wrong product.

## 2. Tray sealer and thermoformer cycle
In the sealing station: **vacuum** draws air out → **gas flush** fills with the mix →
**seal** (heated tool presses lidding film to the tray flange) → **cut**. On
thermoformers the bottom web is formed into pockets first (heat + vacuum/pressure into
the forming die), filled, then sealed the same way.
Key settings:
- **Vacuum level** (mbar) before flush — deeper vacuum = less residual O₂ but longer
  cycle; too deep with soft product draws juice into the seal.
- **Gas flush pressure/time** — enough to replace evacuated air; over-pressure
  balloons the lid.
- **Seal temperature, time, pressure** — within the lidding film's seal window and
  compatible with the tray's seal layer (e.g. PE or peelable layer on PET/APET).
- Seal tooling must match the tray format; check the seal gasket/rubber for wear.

## 3. Vacuum and skin packs
- **Vacuum chamber machines:** product in bag, chamber pumped down, bag sealed, air
  let back in. Check the pump reaches its setpoint and the oil is changed per schedule
  (oil saturated with moisture won't pull a deep vacuum).
- **Vacuum skin packaging (VSP):** heated top film drapes tightly over the product
  and seals to the whole tray surface. Watch for webbing (pleats) on tall/sharp
  product and bone-guard needs on bone-in cuts to stop punctures.

## 4. Headspace gas testing
- Use a **headspace analyser**: needle through a self-adhesive septum on the lid, it
  draws a sample and reads **O₂ and CO₂ %**.
- Test at start-up, after every gas or film change, and at the interval set (e.g. a few
  packs from each lane per hour). Test packs from **every lane / every cavity** — one
  blocked gas nozzle affects one lane only.
- Typical limit for low-O₂ MAP is residual O₂ below about 0.5–1% (check spec); high-O₂
  packs have a minimum O₂.
- Calibrate the analyser with air (20.9% O₂) and the manufacturer's check gases at the
  interval it specifies.

## 5. Leak detection
- **Water bath vacuum test:** pack submerged, vacuum applied, watch for bubbles —
  destructive, sample-based.
- **Inline/offline CO₂ leak detectors:** sense CO₂ escaping from a pack under
  vacuum — non-destructive.
- Look at seals: product, fat or liquid on the flange is the main cause; tray flange
  must be clean when it reaches the sealer.
- A leak found later in a sample: hold all product since the last good test.

## Gotchas
- Barrier film only works if it is the barrier grade (e.g. with EVOH layer): a
  non-barrier film looks identical.
- CO₂ uptake makes residual readings change over the first hours; test fresh and
  follow-up samples consistently.
- Gas mixers drift; verify the mix at the pack, not just on the mixer display.

## Verify
- [ ] Correct food-grade gas mix connected and confirmed at the pack.
- [ ] Vacuum, flush and seal settings in the recipe window.
- [ ] Residual O₂/CO₂ within spec on every lane.
- [ ] Leak test passed; flanges clean.

*Uncertain: gas mixes and residual O₂ limits are typical published values — product
specification governs.*
