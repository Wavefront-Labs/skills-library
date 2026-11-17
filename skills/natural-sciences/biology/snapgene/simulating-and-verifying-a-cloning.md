---
id: natural-sciences.biology.snapgene.simulating-and-verifying-a-cloning
name: simulating-and-verifying-a-cloning
category: natural-sciences
field: biology
product: snapgene
tags: [snapgene, snapgene-viewer, plasmid-map, in-silico-cloning, cloning-simulation, restriction-cloning, gibson-assembly, nebuilder, hifi-assembly, golden-gate, gateway, ta-cloning, primer-design, overlap-primers, agarose-gel-simulation, diagnostic-digest, sanger-sequencing, align-to-reference, chromatogram, sequence-verification, benchling, geneious, ape, plasmid-editor, open-reading-frame]
level: practitioner
status: draft
description: "Plan a cloning in SnapGene before touching the bench: simulate restriction or Gibson assembly, design primers, predict a diagnostic digest gel, then verify Sanger reads against the map."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Simulating and verifying a cloning in SnapGene

**Goal:** have a correct, annotated map of the plasmid you intend to build before you
order primers, and a fast way to confirm the colonies you pick actually match it.
Applies to SnapGene (paid); the free **SnapGene Viewer** opens and displays files but
does not simulate cloning. Similar workflows exist in Benchling, Geneious and ApE.

## 1. Start from trustworthy files
- Get vector sequences from the supplier or Addgene as `.dna` or GenBank (`.gb`) — not
  retyped. Addgene's "full sequence from depositor" vs "Addgene assembled" can differ;
  prefer full sequencing when available.
- Check features are annotated (**Features › Detect Common Features** adds standard
  promoters, resistance genes, origins). Mis-annotated maps are a common source of
  frame errors.
- Set the correct topology (circular vs linear) — it changes fragment sizes.

## 2. Simulate the cloning (Actions menu)
SnapGene offers dedicated dialogs for each method; the main ones:
- **Restriction cloning** (Actions › Restriction and Insertion Cloning): choose
  vector sites and insert fragment. The dialog warns about incompatible ends and shows
  whether the insert is in frame with a fusion partner. Check that your chosen enzymes
  don't cut **inside** the insert — use **Enzymes › Choose Enzymes › Unique 6+ Cutters**
  on the final product to see.
- **Gibson / NEBuilder HiFi** (Actions › Gibson Assembly or "Assembly"): pick the
  linearised vector and fragments; SnapGene designs primers with overlaps (typically
  ~20–30 bp) and shows them on the product. Keep overlap Tm roughly in the 48–65 °C
  range for Gibson (check the kit's guidance).
- **Golden Gate**, **Gateway** (BP/LR), **TA/TOPO**, **In-Fusion**, and **mutagenesis** each
  have their own dialogs.
The output is a new file with history: **File › History** (or the history view)
records every step, which documents the construct's lineage.

## 3. Check the product file
- Translate the ORF across the junctions (select the region, view translation) — no
  stop codons, correct frame into tags.
- Kozak/RBS spacing and start codon preserved.
- Unique sites you will need later still unique.
- Save with a meaningful name and version; keep the parent files.

## 4. Predict a diagnostic digest
Use **Tools › Simulate Agarose Gel** with the product and parent plasmids side by side,
picking enzymes that give clearly different band patterns (ideally bands well separated
on a 0.8–1 % gel, e.g. 0.5–5 kb). This screens colonies before sequencing. Include the
empty vector lane to show what a failed clone looks like.

## 5. Verify by sequencing
1. Design sequencing primers ~50–100 bp upstream of each junction (Sanger reads lose
   quality in the first ~30–50 bases).
2. Import the `.ab1` trace files: **Actions › Align to Reference DNA Sequence** (or
   drag the traces onto the map) against the expected product.
3. Inspect every mismatch on the **chromatogram**, not just the base call: mixed peaks
   indicate a mixed colony; a clean peak that disagrees is a real mutation.
4. Sequence the full insert and both junctions; for PCR-amplified inserts, mutations
   can be anywhere in the amplified region.

## Gotchas
- **Dam/Dcm methylation:** some sites (e.g. XbaI, ClaI overlapping GATC) are blocked
  when DNA comes from dam+ *E. coli*. SnapGene can show methylation-sensitive sites; use
  dam−/dcm− strains if needed.
- Simulated Gibson primers sometimes have strong secondary structure or a high Tm
  mismatch between the annealing and overlap parts; check them in the primer view.
- SnapGene trusts your input sequence. A vector map from a catalogue can lack a
  manufacturer-unlisted mutation; sequence-verify parental plasmids in critical work.
- Menu names drift across versions; the functions above existed in recent versions but
  exact menu paths may differ — search the help for the method name.

Uncertain here: menu paths quoted from memory of SnapGene 6/7-era releases; not checked
against the current version.

## Verify
- [ ] Final map built by simulation from source files, with history intact.
- [ ] ORF translates through all junctions with no unexpected stops.
- [ ] Predicted gel distinguishes correct clone from empty vector.
- [ ] Sanger traces aligned; every discrepancy inspected on the chromatogram.
