---
id: natural-sciences.biology.protein-biochemistry.western-blot-troubleshooting
name: western-blot-troubleshooting
category: natural-sciences
field: biology
product: protein-biochemistry
tags: [protein-biochemistry, western-blot, immunoblot, sds-page, transfer, pvdf, nitrocellulose, ponceau-s, blocking, bsa, milk, primary-antibody, secondary-antibody, hrp, ecl, chemiluminescence, fluorescent-western, high-background, no-signal, nonspecific-bands, loading-control, total-protein-normalisation, phospho-protein, densitometry, troubleshooting]
level: practitioner
status: draft
description: "Fix a western blot with no signal, high background or extra bands: check transfer with Ponceau, choose blocker, titrate antibodies, and normalise to total protein for quantitation."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Western blot troubleshooting

**Goal:** get a specific band at the expected molecular weight on a clean membrane,
and quantify it defensibly — by checking each stage (gel, transfer, blocking,
antibodies, detection) in order rather than re-running the whole thing blindly.

## 1. Check the stage that failed
Work forward; each check is cheap.
1. **Gel:** was the ladder resolved? Did the dye front run off? Use a gel percentage
   suited to your target (higher % for small proteins, gradient gels for a wide range).
2. **Transfer:** stain the membrane with **Ponceau S** right after transfer (reversible,
   washes off in TBST/water). You should see evenly loaded lanes. Blank patches = air
   bubbles; faint high-MW region = transfer too short; small proteins missing = blown
   through the membrane (use 0.2 µm pore, shorter time, or a second membrane behind to
   catch them). This one photo also serves as a total-protein loading record.
3. **Blocking, antibodies, detection:** only now troubleshoot the immunostaining.

## 2. Symptom table
| Symptom | Likely cause | Try |
|---|---|---|
| No signal, Ponceau fine | Primary too dilute, wrong species secondary, epitope destroyed, protein not expressed | Positive-control lysate; check secondary matches host species; increase primary or incubate overnight at 4 °C |
| No signal, Ponceau blank | Transfer failed | Check sandwich orientation (proteins move toward the + anode), methanol in buffer, PVDF wetted in methanol first |
| Uniform high background | Insufficient blocking or washing, antibody too concentrated, membrane dried out | Longer block; more/longer TBST washes; dilute secondary |
| Speckled background | Particulates in blocker, dirty trays | Filter blocker; clean trays |
| Extra bands | Antibody cross-reactivity, degradation, PTMs, dimers | Protease inhibitors; fresh samples; knock-down/knock-out control; compare to vendor's validation blot |
| Band at the wrong size | Glycosylation, phosphorylation, splicing, incomplete denaturation | Check predicted vs reported apparent MW in the literature; boil properly in reducing buffer |
| White (hollow) bands with ECL | Too much HRP/protein — substrate exhausted locally | Dilute secondary; load less |
| Saturated signal | Over-exposure | Shorter exposures; imager saturation warnings |

## 3. Blocking choice matters
- **Non-fat milk (~5 %)** is cheap and blocks well, but contains phosphoproteins (casein)
  and biotin. For phospho-specific antibodies and streptavidin systems use **BSA** instead.
- Use the blocker the antibody datasheet recommends; some primaries only work in one.
- Use TBS-based buffers for phospho-detection with alkaline-phosphatase systems; PBS
  phosphate can interfere (commonly cited — check your kit).

## 4. Quantitation that survives review
- Stay in the **linear range**: run a dilution series of one lysate once to find where
  signal is proportional to load. Saturated bands cannot be compared.
- Prefer **total-protein normalisation** (Ponceau or stain-free total lane signal) over a
  single housekeeping protein. GAPDH/actin/tubulin are often saturated at typical loads
  and can change with treatment.
- For phospho-proteins, normalise to the total protein of the same target (strip and
  re-probe, or multiplex fluorescent secondaries from different species).
- Fluorescent secondaries give a wider linear range than ECL film; digital imagers beat
  film for quantitation.
- Keep the uncropped full-membrane images; many journals require them.

## Gotchas
- PVDF must be pre-wetted in methanol; nitrocellulose must not be. A dried-out membrane
  gives patchy background that no washing fixes.
- Sodium azide (antibody preservative) inhibits HRP — don't add it to HRP secondaries
  or ECL steps.
- Re-using diluted primaries works for some antibodies and not others; record usage
  count if you do.
- Stripping removes some antigen too; don't quantitatively compare before/after strip
  signals.

Uncertain here: exact dilutions, transfer times and voltages depend on the apparatus
(wet tank vs semi-dry vs rapid systems) — start from the manufacturer's protocol.

## Verify
- [ ] Ponceau (or stain-free) image shows even transfer across all lanes.
- [ ] Band at the expected apparent MW, absent or reduced in a negative/knock-down control.
- [ ] Signals for quantitation are below saturation and inside the tested linear range.
- [ ] Normalised to total protein (or justified loading control); full blots saved.
