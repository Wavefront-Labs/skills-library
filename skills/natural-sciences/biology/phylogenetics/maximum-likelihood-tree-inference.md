---
id: natural-sciences.biology.phylogenetics.maximum-likelihood-tree-inference
name: maximum-likelihood-tree-inference
category: natural-sciences
field: biology
product: phylogenetics
tags: [phylogenetics, phylogeny, maximum-likelihood, ml-tree, iq-tree, iqtree2, raxml-ng, mafft, muscle, multiple-sequence-alignment, trimal, alignment-trimming, model-selection, modelfinder, gtr, bic, ultrafast-bootstrap, ufboot, sh-alrt, bootstrap-support, outgroup, rooting, long-branch-attraction, figtree, itol, newick]
level: practitioner
status: gated
description: "Infer a maximum-likelihood phylogeny end to end: align with MAFFT, trim, pick a model with ModelFinder, run IQ-TREE with UFBoot/SH-aLRT, root and read support honestly."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Maximum-likelihood tree inference

**Goal:** a phylogeny from a set of homologous sequences whose topology and support
values you can defend, using a standard ML workflow (MAFFT → trimming → IQ-TREE).

## 1. Assemble the right sequences
- Sequences must be **homologous** (same gene/region), ideally orthologs. Paralogs
  produce gene-duplication trees, not species trees.
- Include an **outgroup**: one or more taxa known to sit outside your group of interest,
  but not so distant that their sequences are saturated.
- Remove exact duplicates (IQ-TREE also collapses identical sequences and warns).
- Use clean, informative headers — no spaces or special characters (`Genus_species_ACC`),
  because many tools truncate names at whitespace.

## 2. Align
```
mafft --auto input.fasta > aln.fasta          # small/medium sets
mafft --localpair --maxiterate 1000 in.fa > aln.fa   # L-INS-i: <~200 seqs, accurate
```
For protein-coding DNA, align as amino acids and back-translate (codon-aware tools such as
MACSE or PAL2NAL) so gaps fall in frame. **Look at the alignment** (AliView, Jalview):
misaligned or reverse-complemented sequences are obvious by eye.

## 3. Trim (optionally)
Remove gap-rich, poorly aligned columns: `trimal -in aln.fa -out aln.trim.fa -automated1`
or ClipKIT (gated: unconfirmed, source is paywalled or blocked; trimAl and ClipKIT were not run here). Over-trimming discards signal; studies disagree on how much trimming helps,
so compare trees with and without if a result hinges on it.

## 4. Choose a model and infer the tree
IQ-TREE 2 does both in one run:
```
iqtree2 -s aln.trim.fa -m MFP -B 1000 -alrt 1000 -T AUTO -o Outgroup_taxon
```
- `-m MFP` runs **ModelFinder** and picks the best model by BIC (look in the `.iqtree`
  report for the chosen model, e.g. `GTR+F+I+G4` or `LG+G4`).
- `-B 1000` = ultrafast bootstrap (UFBoot); `-alrt 1000` = SH-aLRT test.
- For multi-gene data, use a partition file (`-p partitions.nex`) so each gene gets its
  own model.
RAxML-NG is the main alternative (`raxml-ng --all --msa aln.fa --model GTR+G --bs-trees 200`);
it uses standard non-parametric bootstraps (gated: unconfirmed, source is paywalled or blocked; RAxML-NG was not run here).

## 5. Read support honestly
- **UFBoot and standard bootstrap are not on the same scale.** IQ-TREE's FAQ
  suggests trusting a clade when **UFBoot ≥ 95** and **SH-aLRT ≥ 80**, but says this applies to single-gene trees only: in a concatenated phylogenomic analysis supports tend to 100%, so compute concordance factors instead. With `-B` and `-alrt` the treefile labels read SH-aLRT/UFBoot (e.g. `99.6/100`); for standard
  bootstrap, ≥ 70 is a common (soft) threshold.
- Low support is a result, not a failure: collapse poorly supported nodes in figures or
  say they are unresolved.
- Support measures repeatability given the data and model, **not** truth. A strongly
  supported wrong tree is possible with systematic error.

## 6. Root and draw
ML trees are unrooted. Root on the outgroup (FigTree, iTOL, ETE, `ape::root()` in R).
Midpoint rooting assumes a clock-like rate and is a last resort. Display support values
on branches and include a scale bar (substitutions per site).

## Gotchas
- **Long-branch attraction:** fast-evolving taxa cluster together regardless of true
  relationships. Remedies: add taxa that break up long branches, better models
  (site-heterogeneous for proteins, e.g. C20/C60 in IQ-TREE), remove saturated third codon
  positions.
- Gene trees ≠ species trees (incomplete lineage sorting, introgression, HGT). For
  species trees from many genes, use coalescent methods (e.g. ASTRAL) on gene trees.
- Recombining sequences (many viruses, some bacteria) violate the single-tree assumption;
  screen for recombination first.
- Always report alignment length, number of parsimony-informative sites, model and
  software versions.

Checked 2026-10-19 on a simulated 7-taxon, 600 bp alignment: `mafft --auto` and `mafft --localpair --maxiterate 1000` (MAFFT 7.526 Windows) and `iqtree2 -s aln -m MFP -B 1000 -alrt 1000 -T AUTO -o <outgroup>` (IQ-TREE 2.4.0) ran; ModelFinder reported its best model by BIC (JC on this simulated data) and the two clades received 99.6/100 and 99.7/100.

Uncertain here: flag names given are for IQ-TREE 2.x; IQ-TREE 3 and RAxML-NG versions may
change defaults — check `--help`.

## Verify
- [ ] Alignment inspected by eye; no reversed or frame-shifted sequences.
- [ ] Model chosen by ModelFinder (or justified) and reported.
- [ ] Support thresholds stated for the method used (UFBoot vs bootstrap).
- [ ] Tree rooted on a stated outgroup; scale bar present.
- [ ] Key clade robust to trimming/model choice, or sensitivity is reported.
