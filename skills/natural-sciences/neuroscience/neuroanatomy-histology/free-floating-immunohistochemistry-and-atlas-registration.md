---
id: natural-sciences.neuroscience.neuroanatomy-histology.free-floating-immunohistochemistry-and-atlas-registration
name: free-floating-immunohistochemistry-and-atlas-registration
category: natural-sciences
field: neuroscience
product: neuroanatomy-histology
tags: [neuroanatomy-histology, neuroscience, histology, immunohistochemistry, ihc, immunofluorescence, free-floating-sections, perfusion, pfa-fixation, cryoprotection, vibratome, cryostat, freezing-microtome, antigen-retrieval, blocking, primary-antibody, secondary-antibody, antibody-validation, controls, nissl, dapi, confocal, slide-scanner, atlas-registration, allen-ccf, quicknii, brainreg, qupath, stereology, cell-counting]
level: advanced
status: draft
description: "Process rodent brain for free-floating immunofluorescence: perfusion and sectioning, staining with proper antibody controls, imaging, and registering sections to an atlas for regional counts."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Free-floating immunohistochemistry and atlas registration

**Goal:** stained brain sections whose signal is specific, comparable across animals,
and assigned to the correct anatomical region.

## 1. Fixation and tissue preparation
- **Transcardial perfusion:** saline/PBS flush until liver clears, then 4%
  paraformaldehyde (PFA). Poor perfusion leaves blood (autofluorescent red cells) and
  uneven fixation. Under approved protocols and deep terminal anaesthesia only.
- **Post-fix** (commonly overnight at 4 °C); over-fixation masks some epitopes.
- **Cryoprotect** in 30% sucrose until the brain sinks (1–3 days) if cutting frozen.
- **Sectioning:** 30–50 µm sections on a vibratome (no freezing needed), freezing
  microtome or cryostat. Collect **serial series** (e.g. every 6th section into well 1)
  so each well samples the whole brain systematically.
- Store in cryoprotectant (glycerol/ethylene glycol based) at −20 °C long-term.

## 2. Staining protocol (free-floating, immunofluorescence)
1. Wash 3× in PBS. Optional **antigen retrieval** (e.g. warm citrate buffer) for
   antibodies that need it.
2. **Block and permeabilise:** PBS + 0.3% Triton X-100 + 5–10% normal serum (from
   the secondary's host species), 1–2 h at room temperature.
3. **Primary antibody** in blocking buffer, often overnight to 48 h at 4 °C with
   gentle agitation. Titrate dilution on pilot sections.
4. Wash 3× ≥10 min.
5. **Secondary antibody** (fluorophore-conjugated, cross-adsorbed), 1–2 h at room
   temperature, protected from light.
6. Wash; counterstain (DAPI or fluorescent Nissl); mount on slides, air-dry briefly,
   coverslip with anti-fade medium.
Run all groups **in the same batch** with the same reagent lots; mixed-batch staining
creates group differences in intensity.

## 3. Antibody validation and controls
- Use antibodies validated for IHC in your species, ideally with **knockout tissue**
  showing absent staining.
- **No-primary control** (secondary only) for nonspecific secondary binding.
- Peptide-block controls are weaker evidence than knockouts.
- Check expected pattern against atlas expression data (e.g. in situ hybridisation
  resources).
- Multiple labelling: primaries from different host species, or directly conjugated
  antibodies; check for bleed-through between channels with single-stained controls.

## 4. Imaging
- Widefield slide scanner for whole-section overviews; confocal for colocalisation and
  fine structure.
- **Fix acquisition settings** (exposure/laser power, gain, offset, pinhole, z-step) for
  all samples to be compared; avoid saturated pixels (use the histogram/LUT).
- Image a reference section under the same settings across sessions if imaging is split.

## 5. Atlas registration
- Identify each section's anteroposterior level and match to a reference atlas
  (e.g. Allen Mouse Brain Common Coordinate Framework, Paxinos & Franklin, Waxholm rat).
- Tools: **QuickNII** + **VisuAlign** (QUINT workflow) for 2D sections with
  non-linear refinement; **brainreg**/**brainglobe** for whole-brain volumes (e.g.
  light-sheet); **ABBA** in Fiji/QuPath. Sectioning angle often deviates from atlas
  planes — use tools that estimate the cutting angle.
- Count cells with **QuPath** or similar (threshold + detection settings fixed across
  animals), then assign to regions via registration.
- For unbiased absolute numbers, use **design-based stereology** (optical fractionator)
  rather than profile counts.

## Gotchas
- Tissue shrinkage (especially in z after mounting) affects densities; report it.
- Edge artefacts and folded sections give false signal — exclude by pre-set criteria.
- Autofluorescence (lipofuscin in older animals) — consider quenching (e.g. Sudan Black/TrueBlack).

## Verify
- [ ] Well-perfused tissue; serial sampling scheme documented.
- [ ] All groups stained in one batch with the same lots.
- [ ] Antibody validation plus no-primary and single-stain controls.
- [ ] Acquisition settings fixed; no saturation.
- [ ] Sections registered to a named atlas version; counting settings fixed and blinded.

*Draft note:* concentrations and times are common starting points; every antibody
needs its own titration and protocol optimisation.
