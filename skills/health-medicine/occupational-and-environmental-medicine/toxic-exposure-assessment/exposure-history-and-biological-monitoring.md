---
id: health-medicine.occupational-and-environmental-medicine.toxic-exposure-assessment.exposure-history-and-biological-monitoring
name: exposure-history-and-biological-monitoring
category: health-medicine
field: occupational-and-environmental-medicine
product: toxic-exposure-assessment
tags: [toxic-exposure, exposure-history, biological-monitoring, biomonitoring, bei, biological-exposure-index, acgih, bmgv, lead, blood-lead, mercury, cadmium, arsenic, organophosphate, cholinesterase, carbon-monoxide, carboxyhaemoglobin, solvents, heavy-metals, chelation, chemical-incident, decontamination, poisons-centre, toxbase, occupational-toxicology, environmental-medicine]
level: advanced
status: gated
description: "Assess a hazardous exposure: structured exposure history, choosing and timing biological monitoring samples, interpreting results against BEI/BMGV values, and when to escalate to toxicology."
sources: ["https://www.poison.org/", "https://www.hse.gov.uk/pubns/books/eh40.htm"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

> General clinical/professional reference, not a substitute for independent clinical judgement, current guidelines, or verified dosing references.

# Exposure history and biological monitoring

**Goal:** turn "I think something at work is making me ill" into a quantified judgement:
what the agent is, how much got in, whether that dose explains the clinical picture, and
what to do next.

## 1. Take a structured exposure history
A useful mnemonic is **CH²OP** (community, home, hobbies, occupation, personal habits)
plus, for each candidate exposure:
- **Agent** — get the product name and the **Safety Data Sheet (SDS)**; section 2
  (hazards), 3 (composition) and 8 (exposure limits/PPE) are the useful parts.
- **Route** — inhalation, skin (solvents, organophosphates penetrate intact skin),
  ingestion (eating at the workstation, hand-to-mouth for lead).
- **Intensity and duration** — task, hours, enclosed space, heated process, spill.
- **Controls** — local exhaust ventilation, respirator type and fit-testing, gloves
  (material matters: nitrile is not universal).
- **Others affected**, and any workplace air-monitoring results (ask the employer or
  occupational hygienist).

## 2. Choose the biological test and time it
Biological monitoring measures the agent or its metabolite in blood, urine or breath.
**Sample timing is the most common failure** because half-lives differ. The rows below summarise ACGIH BEI-type guidance (gated: unconfirmed, source is paywalled or blocked):

| Agent | Typical specimen | Timing note |
|---|---|---|
| Inorganic lead | Blood lead (+ ZPP for longer-term) | Any time; reflects weeks |
| Mercury (inorganic) | Urine (creatinine-corrected) | Any time; long half-life |
| Cadmium | Urine (body burden), blood (recent) | Any time |
| Organophosphates/carbamates | RBC acetylcholinesterase vs worker's own baseline | Compare to pre-exposure baseline |
| Carbon monoxide | Carboxyhaemoglobin | **Immediately** — falls fast once off exposure/on oxygen |
| Many solvents (e.g. toluene, xylene) | Urinary metabolite | **End of shift**, sometimes end of work week |
| Arsenic | Speciated urine arsenic | Avoid seafood 48–72 h before (organic arsenic confounds) |

Check the current ACGIH BEI or national guidance value (e.g. UK HSE BMGV (gated: unconfirmed, source is paywalled or blocked)) for the exact
determinant and timing before sampling; these tables are summaries, not the reference.

## 3. Interpret
- Compare against the **occupational guidance value**, which is a population hygiene
  benchmark for exposure control, **not** a clinical toxicity threshold.
- Use **creatinine-correction** for urine where the reference specifies it; reject very
  dilute or concentrated spot samples per lab criteria.
- Correlate with symptoms and examination: a mildly elevated level with classic
  symptoms is different from the same level in a well worker.
- Trend in the same person beats a single value.

## 4. Act
- **Above action level** → workplace investigation (hygiene review, controls), repeat
  test, consider removal from exposure. Some agents have statutory removal levels (lead
  regulations in many jurisdictions set suspension thresholds; check local law).
- **Clinical toxicity** → discuss with a poisons centre (UK TOXBASE/NPIS (gated: unconfirmed, source is paywalled or blocked), US Poison
  Control 1-800-222-1222) or clinical toxicologist. **Chelation is specialist-led**; do
  not start it to treat a number alone.
- **Acute chemical incident** → decontamination before treatment (remove clothing,
  water irrigation unless agent-specific contraindication), protect staff, notify.

## Gotchas
- Lab units differ (µg/dL vs µmol/L for lead; µg/g creatinine vs µmol/mol). Convert
  before comparing.
- Pregnancy, children (take-home lead on clothing) and hobbies (shooting, stained glass,
  pottery glazes) are frequent hidden sources.
- Contaminated sample containers and skin contamination at venepuncture cause false highs.

## Verify
- [ ] SDS obtained and route, intensity and controls documented.
- [ ] Specimen and timing match the agent's kinetics and the reference method.
- [ ] Result interpreted with units converted and against the right reference type.
- [ ] Workplace follow-up triggered for any elevated result; toxicology involved for
      clinical toxicity.

## Checked

- Date checked: 2026-10-25. Jurisdiction: United States and United Kingdom; limits and removal levels are national.
- Sources read: Poison Help site; HSE EH40 page.
- Confirmed: US Poison Help number 1-800-222-1222.
- Corrected or removed: No wrong claim found.
- Gated: The biological-monitoring table (specimen and timing per agent), the BMGV reference (the HSE biological monitoring page returned 404, EH40 page does not mention BMGVs) and TOXBASE/NPIS.

Method: documentation only; no commands were run.
