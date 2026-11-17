---
id: natural-sciences.biology.genomics-sequencing.ngs-library-qc-before-sequencing
name: ngs-library-qc-before-sequencing
category: natural-sciences
field: biology
product: genomics-sequencing
tags: [genomics-sequencing, ngs, next-generation-sequencing, illumina, library-prep, library-qc, qubit, bioanalyzer, tapestation, fragment-analyzer, qpcr-library-quantification, kapa, adapter-dimer, insert-size, molarity, nm-conversion, pooling, multiplexing, index-hopping, unique-dual-indexes, phix, low-diversity, rin, din, input-qc, rna-seq, whole-genome-sequencing]
level: practitioner
status: gated
description: "QC an Illumina-style NGS library before loading: input integrity, Qubit vs qPCR quantification, fragment-size traces, adapter dimers, ng/uL-to-nM conversion, pooling and PhiX."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NGS library QC before sequencing

**Goal:** catch a bad library at the bench, where it costs an hour, instead of on the
sequencer, where it costs a flow cell and a week. Applies to short-read
(Illumina-style) libraries; long-read platforms have different QC.

## 1. QC the input, not just the library
- **DNA:** fluorometric concentration (Qubit/PicoGreen), integrity on a gel or
  TapeStation (DIN). Purity by NanoDrop ratios (A260/280 ~1.8, A260/230 ~2.0–2.2);
  low 260/230 suggests salt, phenol or guanidine carryover that inhibits enzymes.
- **RNA:** RIN/RQN. Many poly-A RNA-seq protocols want RIN ≳ 7–8; degraded samples
  (FFPE) need rRNA-depletion protocols and DV200 rather than RIN.
- NanoDrop **overestimates** concentration when RNA/free nucleotides are present; use a
  dye-based assay for the number you put into the prep.

## 2. Library QC — two numbers and one picture
1. **Concentration (ng/µL)** by Qubit dsDNA HS — measures all dsDNA, including molecules
   without adapters.
2. **Size distribution** on Bioanalyzer/TapeStation/Fragment Analyzer — gives the average
   fragment size (insert + adapters, roughly +120–140 bp for standard Illumina adapters) (gated: unconfirmed, source is paywalled or blocked)
   and shows contaminants.
3. **qPCR library quantification** (e.g. KAPA-type kits) — measures only molecules with
   both adapters, i.e. what will actually cluster. This is the most accurate number for
   loading; many cores insist on it.

## 3. Reading the trace
| Feature | Meaning | Action |
|---|---|---|
| Sharp peak ~120–150 bp | Adapter dimer | Extra bead clean-up (e.g. 0.8–0.9× SPRI); dimers cluster preferentially and waste reads |
| Peak ~70–90 bp | Leftover primers | Bead clean-up |
| Broad hump at high MW / "bubble" product | Over-amplification (heteroduplexes migrate slowly) | Fewer PCR cycles next time; quantify by qPCR, not trace |
| Distribution centred where expected | Good | Proceed |

Many cores want adapter dimer below a few % of molarity — check their requirement.

## 4. Convert to molarity
Molarity (nM) = concentration (ng/µL) ÷ (660 g/mol × average size bp) × 10⁶

Example: 4 ng/µL, average 450 bp → 4 ÷ (660 × 450) × 10⁶ = 13.47 ≈ **13.5 nM** (computed; the units work out because 1 ng/µL = 1 mg/L = 10⁻³ g/L).

Use the average size from the trace over the library region only (set the region to
exclude dimers), otherwise the molarity is off.

## 5. Pooling
- Bring every library to the same nM, then combine equal volumes — or weight by the
  read depth each sample needs.
- Use **unique dual indexes (UDIs)** on patterned flow cells to make index hopping
  detectable and filterable.
- Check index **colour balance** for the instrument chemistry (2-colour systems read
  G as dark; an all-G index cycle can fail). The vendor's index-pooling guide lists
  compatible sets.
- Low-diversity libraries (amplicons, single-cell barcodes) need **PhiX spike-in**
  (often ~1–5 % for normal libraries, 10–50 % for very low diversity) or custom
  primers. Exact percentages are platform-specific.

## Gotchas
- Qubit-based nM is often higher than qPCR nM; loading from Qubit alone tends to
  under-cluster if the library has unligated fragments, or over-cluster if the size
  estimate is wrong.
- Pipetting a fraction of a microlitre to pool introduces most of the variance in read
  depth. Dilute first so each volume is ≥ 2 µL.
- Re-quantify after freezing a diluted pool at low concentration; DNA sticks to tubes
  at pM levels. Use low-bind tubes and add Tween/EB per the loading guide.

Checked 2026-10-19: the molarity formula and example computed. The vendor-specific figures (adapter offset, dimer and primer peak sizes, PhiX percentages, 2-colour index rule, NanoDrop ratio ranges) come from kit and platform documents that were not re-read (gated: unconfirmed, source is paywalled or blocked); confirm in your kit and sequencer guides.

Uncertain here: dimer thresholds and PhiX percentages vary by sequencing core and
instrument model; follow the core's submission guidelines where they exist.

## Verify
- [ ] Input passed integrity and purity checks; quantified by fluorometry.
- [ ] Trace shows expected size, no dominant dimer peak.
- [ ] Library molarity by qPCR (or justified alternative) and calculation recorded.
- [ ] UDIs used; index set colour-balanced; PhiX level set for library diversity.
- [ ] After the run, demultiplexed read counts per sample within ~2× of each other.
