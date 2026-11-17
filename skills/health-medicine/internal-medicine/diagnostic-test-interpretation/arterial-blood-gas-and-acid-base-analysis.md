---
id: health-medicine.internal-medicine.diagnostic-test-interpretation.arterial-blood-gas-and-acid-base-analysis
name: arterial-blood-gas-and-acid-base-analysis
category: health-medicine
field: internal-medicine
product: diagnostic-test-interpretation
tags: [diagnostic-test-interpretation, internal-medicine, abg, arterial-blood-gas, vbg, acid-base, anion-gap, delta-ratio, winters-formula, metabolic-acidosis, metabolic-alkalosis, respiratory-acidosis, respiratory-alkalosis, osmolar-gap, a-a-gradient, mudpiles, gold-mark, hagma, nagma]
level: practitioner
status: draft
description: "Six-step blood-gas reading: primary disorder, expected compensation (Winter's etc.), albumin-corrected anion gap, delta ratio, osmolar gap and A-a gradient, with worked numbers."
sources: ["Berend K, de Vries AP, Gans RO, Physiological approach to assessment of acid-base disturbances, NEJM 2014", "Kraut JA, Madias NE, Serum anion gap, Clin J Am Soc Nephrol 2007", "Harrison's Principles of Internal Medicine, acid-base chapter"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Arterial blood gas and acid–base analysis

> General clinical/professional reference, not a substitute for independent clinical judgement, current guidelines, or verified dosing references.

**Goal:** read any gas in under two minutes, identify every coexisting disorder, and
name the next test — using the same steps every time so mixed disorders don't slip by.

Units below: pH, PaCO₂ in mmHg (× 0.133 for kPa), HCO₃⁻ and electrolytes in mmol/L.

## Step 0 — Is the sample what you think?
Arterial vs venous (VBG pH runs ~0.03–0.04 lower, HCO₃⁻ similar, PCO₂ unreliable for
ventilation — though a normal venous PCO₂ makes arterial hypercapnia unlikely). Check
the HCO₃⁻ on the gas roughly matches serum bicarbonate from the chemistry panel.

## Step 1 — Acidaemia or alkalaemia?
pH < 7.35 acidaemia, > 7.45 alkalaemia. A normal pH does **not** exclude disorders —
it can mean two opposing ones.

## Step 2 — Primary process
- pH low + HCO₃⁻ low → metabolic acidosis; pH low + PaCO₂ high → respiratory acidosis.
- pH high + HCO₃⁻ high → metabolic alkalosis; pH high + PaCO₂ low → respiratory alkalosis.

## Step 3 — Is compensation appropriate?
| Primary | Expected compensation |
|---|---|
| Metabolic acidosis | PaCO₂ = 1.5 × HCO₃⁻ + 8 ± 2 (**Winter's**) |
| Metabolic alkalosis | PaCO₂ ≈ 0.7 × HCO₃⁻ + 21 ± 2 (rises ~0.7 per 1 HCO₃⁻) |
| Respiratory acidosis | HCO₃⁻ rises 1 per 10 PaCO₂ (acute), 3.5–4 per 10 (chronic) |
| Respiratory alkalosis | HCO₃⁻ falls 2 per 10 PaCO₂ (acute), 4–5 per 10 (chronic) |
Outside the range → a second primary disorder. (Exact coefficients vary slightly by
textbook.)

## Step 4 — Anion gap (always, even without acidosis)
AG = Na⁺ − (Cl⁻ + HCO₃⁻); normal ~8–12 (lab-dependent; ~4–12 with modern
analysers). **Correct for albumin:** add ~2.5 per 1 g/dL albumin below 4 g/dL
(≈ 0.25 per g/L below 40). High-AG causes: **GOLDMARK** — glycols (ethylene,
propylene), oxoproline (paracetamol, chronic), L-lactate, D-lactate, methanol,
aspirin, renal failure, ketoacidosis.

## Step 5 — Delta ratio (if AG is high)
Δ ratio = (AG − 12) / (24 − HCO₃⁻).
- < 1 → coexisting normal-AG (hyperchloraemic) acidosis.
- 1–2 → pure high-AG acidosis.
- > 2 → coexisting metabolic alkalosis (or chronic respiratory acidosis compensation).

Normal-AG acidosis: urine anion gap (Na⁺ + K⁺ − Cl⁻) negative suggests GI bicarbonate
loss; positive suggests renal tubular acidosis. Remember saline infusion.

## Step 6 — Extra gaps
- **Osmolar gap** = measured osm − (2Na⁺ + glucose/18 + BUN/2.8) [mg/dL units; with
  mmol/L: 2Na⁺ + glucose + urea]. > ~10 with high AG → think toxic alcohols. A normal
  gap does not exclude late presentation.
- **A–a gradient** (oxygenation): PAO₂ = FiO₂ × (Patm − 47) − PaCO₂/0.8; at sea level on
  air PAO₂ ≈ 150 − 1.25 × PaCO₂. Normal gradient ≈ (age/4) + 4. Raised gradient → V/Q
  mismatch, shunt or diffusion problem; normal gradient with hypoxaemia → hypoventilation.

## Worked example
pH 7.25, PaCO₂ 24, HCO₃⁻ 10, Na⁺ 138, Cl⁻ 100, albumin 2.0 g/dL.
- Metabolic acidosis. Winter's: 1.5×10 + 8 = 23 ± 2 → 24 is appropriate.
- AG = 138 − 110 = 28; corrected for albumin = 28 + 5 = 33 → high-AG.
- Δ ratio = (33 − 12)/(24 − 10) = 1.5 → pure high-AG acidosis.
- Next: lactate, ketones, creatinine, osmolar gap, salicylate level.

## Gotchas
- Skipping albumin correction hides a high-AG acidosis in sick, hypoalbuminaemic patients.
- Respiratory alkalosis plus metabolic acidosis = classic salicylate toxicity.
- Lactate on many analysers is L-lactate only; D-lactate (short bowel) needs a
  separate assay.
- Delay or air bubbles in the syringe alter PO₂/PCO₂; ice and analyse promptly.

## Verify
- [ ] Sample type confirmed and gas HCO₃⁻ consistent with chemistry.
- [ ] Primary disorder named; compensation calculated, not eyeballed.
- [ ] Albumin-corrected AG calculated; delta ratio if raised.
- [ ] Osmolar gap and A–a gradient considered where relevant.
- [ ] Every disorder listed with a differential and the next test.
