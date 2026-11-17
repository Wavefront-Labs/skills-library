---
id: natural-sciences.biology.molecular-biology.pcr-troubleshooting
name: pcr-troubleshooting
category: natural-sciences
field: biology
product: molecular-biology
tags: [molecular-biology, pcr, polymerase-chain-reaction, endpoint-pcr, troubleshooting, primer-design, annealing-temperature, gradient-pcr, tm, mgcl2, taq, phusion, q5, high-fidelity-polymerase, no-template-control, ntc, primer-dimer, nonspecific-bands, smear, gc-rich, dmso, betaine, touchdown-pcr, colony-pcr, agarose-gel, contamination]
level: practitioner
status: draft
description: "Diagnose a failed endpoint PCR from the gel: no band, wrong size, smear or primer-dimer, with controls, annealing gradients, Mg2+/template titration and GC-rich additives."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# PCR troubleshooting — read the gel, change one variable

**Goal:** turn a failed endpoint PCR into a clean single band of the right size by
reading what the gel and the controls tell you, then changing one variable at a time.

## 1. Before touching conditions: did the controls work?
Every run should carry:
- **No-template control (NTC)** — water instead of template. A band here means
  contamination (reagents, pipettes, aerosol of earlier amplicon), not a protocol problem.
- **Positive control** — a template/primer pair known to work with this master mix.
  If it fails too, the problem is the reagents or the cycler, not your primers.
- **Ladder** in the right size range, so "wrong size" is a measurement, not a guess.

If the NTC is positive: throw out the working aliquots of water, primers and master mix,
make fresh aliquots, and set up PCR in a different area from where you open amplified
product. Pipette tips with filters help; UV-treating the hood helps. Do not troubleshoot
anything else until the NTC is clean.

## 2. Read the gel
| What you see | Most likely causes | First thing to try |
|---|---|---|
| No band, positive control OK | Annealing too high, poor primer, bad/inhibited template, too little template | Annealing gradient; check template quality and amount |
| No band anywhere | Missing reagent, dead polymerase, wrong cycler program | Re-make master mix; check the program actually ran |
| Several bands | Annealing too low, too many cycles, too much template, primer binds elsewhere | Raise annealing 2–3 °C or gradient; cut cycles to ~30 |
| Smear | Too much template, too many cycles, degraded template, too much polymerase or extension time | Dilute template 10×; fewer cycles |
| Low band under ~100 bp | Primer-dimer | Lower primer concentration; hot-start enzyme; raise annealing |
| Band right size but faint | Low efficiency | Add 3–5 cycles; check extension time vs product length |

## 3. The variables, in the order to change them
1. **Annealing temperature.** Run a gradient spanning roughly Tm−5 °C to Tm+5 °C. Use the
   Tm calculator from your **polymerase vendor**: high-fidelity enzymes (Phusion, Q5)
   use different salt assumptions and typically want annealing near or above the
   calculated Tm, whereas Taq protocols often use about Tm−5 °C. Mixing calculators
   and enzymes is a common source of "my primers don't work".
2. **Template amount.** Typical starting points: 1–10 ng plasmid, 10–100 ng genomic DNA
   per 25–50 µL reaction (check your enzyme's sheet). Too much template is as bad as too
   little. Inhibitors (phenol, ethanol, heparin, EDTA, high salt) are diluted out by a
   1:10 template dilution — if the diluted template works better, suspect inhibition.
3. **Mg²⁺.** Usually supplied in the buffer at ~1.5–2 mM for Taq. Titrating in 0.5 mM
   steps can rescue weak reactions; excess Mg²⁺ increases non-specific products and
   lowers fidelity.
4. **Extension time.** Taq ~1 min/kb; many fast high-fidelity enzymes 15–30 s/kb. Long
   products fail quietly if this is too short.
5. **Cycle number.** 25–35. Beyond ~35 you mostly amplify junk.
6. **GC-rich or structured templates.** Add DMSO (commonly 3–5 %, it lowers the effective
   Tm, so re-run the gradient) or betaine (~1 M), or use the vendor's GC enhancer buffer.
   Raise the denaturation temperature to 98 °C if the enzyme tolerates it.
7. **Touchdown PCR** — start annealing ~5–10 °C above Tm and drop 1 °C per cycle, then
   finish at a fixed temperature — useful when a gradient does not separate the target
   from a close off-target band.
8. **Redesign the primers** if all of the above fails: 18–25 nt, 40–60 % GC, Tms within
   ~2 °C of each other, avoid 3′ runs of G/C and self-complementarity, and BLAST them
   against the template organism (see natural-sciences.biology.blast.choosing-a-blast-program-and-reading-hits).

## Gotchas
- Colony PCR: too much cell material inhibits. Touch the colony with a tip and swirl;
  you should barely see anything. Add a longer initial denaturation (~5 min) to lyse cells.
- Proofreading enzymes degrade unprotected primers if left at room temperature with the
  enzyme; assemble on ice and add polymerase last (or use hot-start).
- Gel artefacts can masquerade as PCR problems: overloaded lanes smear, and supercoiled
  plasmid template runs at the "wrong" size.
- Change **one variable per run** and write it down; otherwise you never learn which fix worked.

Uncertain/unconfirmed here: exact concentrations and times vary by enzyme — treat the numbers
above as typical starting points and defer to the polymerase datasheet.

## Verify
- [ ] NTC blank, positive control banded, ladder resolved.
- [ ] Single band within ~10 % of the expected size against the ladder.
- [ ] Result repeats on a fresh setup with the chosen conditions.
- [ ] For cloning/sequencing, product is confirmed by sequencing, not just size.
