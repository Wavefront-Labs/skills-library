---
id: natural-sciences.chemistry.chemdraw.publication-quality-structures-and-schemes
name: publication-quality-structures-and-schemes
category: natural-sciences
field: chemistry
product: chemdraw
tags: [chemdraw, chemdraw-professional, revvity, perkinelmer, chemical-drawing, structure-drawing, reaction-scheme, acs-document-1996, journal-style, bond-length, clean-up-structure, check-structure, name-to-structure, structure-to-name, stereochemistry, wedge-bonds, reaction-arrows, scheme-layout, alignment, tiff, emf, pdf-export, chemdraw-js, chemsketch, marvinsketch, chemdoodle, figure-preparation, publication-figures]
level: intro
status: draft
description: "Make ChemDraw structures and reaction schemes that pass journal checks: ACS Document 1996 style, clean-up, alignment, arrows and conditions, Check Structure, and export."
sources: ["ChemDraw User Guide (Revvity Signals)", "ACS Style Guide / journal author guidelines on chemical structures and schemes", "IUPAC, Graphical representation standards for chemical structure diagrams, Pure Appl. Chem. 80 (2008) 277"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Publication-quality structures and schemes in ChemDraw

**Goal:** figures that a journal accepts without redrawing — consistent bond
lengths and fonts, correct stereochemistry, and schemes that read left to right
— produced quickly and the same way every time.

## 1. Start with the journal's style
- **File › Apply Document Settings from › ACS Document 1996** (default for ACS
  and accepted by most journals): bond length 14.4 pt, 10 pt Arial labels, line width 0.6 pt.
  RSC, Wiley and Elsevier also accept or provide their own templates. Set it *before*
  drawing; applying it later rescales and shifts things.
- Use a template/stationery file so every figure in a paper matches.

## 2. Drawing structures well
- Use ring and chain tools; type atom labels by hovering and pressing the key
  (e.g. hover a carbon, press `o` for O, `n` for N); hotkeys speed everything up.
- **Structure › Clean Up Structure** normalises bond lengths and angles; run it after
  sketching, then fix anything it made ugly by hand.
- **Stereochemistry:** wedges start at the stereocentre (narrow end). Avoid wedges
  between two stereocentres. Turn on **Show Stereochemistry** (CIP labels) to check
  R/S matches what you mean, then hide the labels for the final figure.
- **Structure › Check Structure** flags valence errors (pentavalent carbon is the
  classic typo) — run it on every structure.
- **Name to Structure** (paste an IUPAC name or common name) and **Structure to Name**
  are great checks; a wrong name means a wrong drawing.

## 3. Reaction schemes
- Arrow from the arrow tool; conditions above (reagents) and below (solvent,
  temperature, time); yields under or after the product. Keep reagent text in the
  same font as structures.
- Align structures on a common baseline: select, **Object › Align › Vertical Centers**;
  distribute horizontally for even spacing. Group a structure with its label (Ctrl/Cmd+G).
- Compound numbers in bold under each structure; keep numbering consistent with the text.
- Avoid long single-line schemes; wrap to two rows with a continuation arrow.

## 4. Export
- For Word/LaTeX and submission: copy-paste as embedded ChemDraw objects (editable in Word on
  Windows), or save as **EMF/PDF** (vector) for submission. Use TIFF at ≥ 600 dpi (line art
  often 1200 dpi) only if raster is required.
- Keep the .cdxml source next to the figure; journals and reviewers ask for changes.
- Check the final size: if a scheme is scaled down to fit a column, fonts shrink below
  the minimum (~6–7 pt). Design at the final column width (ACS single column ≈ 3.25 in).

## Gotchas
- Mixing scaled and unscaled structures in one figure gives inconsistent bond
  lengths — Object › Scale to the document bond length.
- Copying from other software (MarvinSketch, ChemDoodle, ChemSketch) may import
  different styles; re-apply document settings.
- Colours: use them sparingly and check in greyscale; some journals charge for colour print.
- *Uncertainty note:* menu names follow recent ChemDraw versions (20–23); older versions
  place Clean Up and Check Structure under slightly different menus.

## Verify
- [ ] Document style applied before drawing; all bond lengths identical.
- [ ] Check Structure reports no valence errors.
- [ ] Stereocentres checked with CIP labels, then labels hidden.
- [ ] Structure-to-Name of each compound matches its intended name.
- [ ] Exported as vector at final size; smallest text ≥ journal minimum.
