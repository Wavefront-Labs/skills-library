---
id: health-medicine.nephrology-and-rheumatology.dialysis-systems.haemodialysis-machine-alarms-and-water-treatment-checks
name: haemodialysis-machine-alarms-and-water-treatment-checks
category: health-medicine
field: nephrology-and-rheumatology
product: dialysis-systems
tags: [dialysis-systems, nephrology-and-rheumatology, nephrology, hemodialysis-machine, haemodialysis-machine, fresenius-5008, fresenius-4008, baxter-ak-98, nipro-surdial, b-braun-dialog, venous-pressure-alarm, arterial-pressure-alarm, air-detector, blood-leak-detector, conductivity-alarm, tmp, water-treatment, reverse-osmosis, chlorine-chloramine, total-chlorine-test, endotoxin, aami-iso-23500, pd-cycler]
level: practitioner
status: draft
description: "Running haemodialysis machines safely: setup checks, arterial/venous/TMP, air, blood-leak and conductivity alarms, and daily water-treatment tests (total chlorine, RO, cultures)."
sources: ["ISO 23500 series (2019): Preparation and quality management of fluids for haemodialysis", "AAMI/ANSI water quality recommended practices for dialysis", "CDC guidelines: infection control in dialysis settings", "Daugirdas JT, Handbook of Dialysis, 5th ed. — dialysis apparatus chapter", "Manufacturer operator manuals (general principles; follow your model's manual)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Haemodialysis machine alarms and water-treatment checks

> General clinical/professional reference, not a substitute for independent clinical judgement, current guidelines, or verified dosing references.

**Goal:** set up and run a haemodialysis treatment so every safety system is armed,
respond correctly to each alarm class, and verify the water feeding the machines is
safe — the checks behind the incidents that have killed dialysis patients (air embolism,
chloramine haemolysis, line disconnection bleeding).

This is model-agnostic (Fresenius 4008/5008/6008, Baxter AK series, B. Braun Dialog,
Nipro, Nikkiso). Exact menus, limits and self-tests differ — the **manufacturer's
operator manual and unit policy override this**.

## 1. Before connecting the patient
- Machine passed **automated self-test** (pressure holds, conductivity, temperature,
  air detector, blood-leak detector, UF control).
- Disinfection completed; for chemical disinfection, **residual test negative**
  (e.g. peracetic acid/formaldehyde indicator strip) before priming.
- Correct concentrate (acid composition matching prescription — K⁺, Ca²⁺) and bicarbonate;
  confirm label versus prescription. **Conductivity** within range (typically ~13.5–14.5
  mS/cm; machine-specific) and independent check if your unit requires (handheld meter).
- Dialyser and bloodlines primed per instructions, no air in the circuit; venous line
  threaded through the **air detector/venous clamp**; transducer protectors dry.
- Prescription entered: time, UF goal, Qb, Qd, temperature, Na⁺/HCO₃⁻, heparin.

## 2. Pressures to understand
| Parameter | Typical range | High/low meaning |
|---|---|---|
| **Arterial (pre-pump)** | Negative, ~−80 to −200 mmHg | More negative → access can't supply Qb (needle position, stenosis, kinked line, hypotension) |
| **Venous (return)** | ~+50 to +200 mmHg | High → clotting in venous chamber/line, kink, needle infiltration, outflow stenosis. **Sudden low → disconnection/needle dislodgement** |
| **TMP** | Machine-dependent | Rising → dialyser clotting or high UF demand |
Set alarm limits **tight around the running value** (many machines auto-set a window) —
wide venous limits can fail to detect a dislodged needle, as venous pressure may only
drop modestly.

## 3. Alarm responses (general sequence: look at patient → look at circuit → fix → restart)
- **Air detector:** blood pump stops and venous clamp closes. **Do not override.** Check
  for air in the venous line, connections, saline bag; remove air per procedure. Suspected
  air embolism (sudden dyspnoea, chest pain, neuro signs): clamp lines, place patient
  **left side down, head low**, 100% oxygen, call emergency team.
- **Venous low:** inspect needle and connections immediately — exsanguination can occur
  in minutes. Keep access and lines visible (not under blankets).
- **Venous high:** check kinks, clotting, needle position; flush with saline; consider
  heparin adequacy.
- **Arterial low (very negative):** reposition needle, check BP, reduce Qb temporarily,
  check for access stenosis.
- **Blood leak detector:** dialyser membrane rupture (blood in dialysate) — confirm with
  test strip in effluent if unclear; stop, return blood only if per policy (contamination
  risk), change dialyser.
- **Conductivity/temperature:** dialysate bypasses the dialyser automatically; check
  concentrate jugs/connections, water supply. Never defeat bypass. Wrong conductivity
  can cause severe hypo/hypernatraemia or haemolysis.
- **UF/fluid balance error:** stop UF, check weight trend; uncontrolled UF can cause
  rapid volume loss.
- Repeated alarm silencing without fixing the cause is a common incident root cause.

## 4. Water treatment — daily and periodic
- **Total chlorine** (covers chloramine) after the carbon tanks: test **before the first
  shift and every shift (e.g. ~4 h)**; limit **≤ 0.1 mg/L** (ISO 23500). Use worker
  tank → polisher tank arrangement; if the worker exceeds limit, check polisher, and stop
  treatments if it fails. Chloramine causes haemolysis and methaemoglobinaemia.
- **Reverse osmosis:** monitor product conductivity/TDS, % rejection, pressures, flows;
  alarm on falling rejection.
- Softener hardness test; sediment filter pressure differentials.
- **Microbiology:** product water and dialysate cultures and endotoxin at least monthly
  (or per programme): standard water < 100 CFU/mL and < 0.25 EU/mL; action levels at 50%
  of maximum. Ultrapure dialysate for haemodiafiltration (< 0.1 CFU/mL, < 0.03 EU/mL).
- Chemical contaminants (aluminium, fluoride etc.) tested at least annually and after
  changes.
- Log every test with result, time and initials; out-of-range → defined action plan.

## 5. Peritoneal dialysis cyclers
Check programming (fill volume, cycles, dwell, last fill) and work drain alarms (position, constipation, kinks, fibrin).

## Gotchas
- Wrong acid concentrate (e.g. 1 K⁺ instead of 3 K⁺) passes conductivity checks — verify labels.
- Venous pressure may not fall enough to alarm with needle dislodgement; visual checks
  and moisture/blood-detection sensors at the access site help.
- Carbon tanks exhaust without warning — the test schedule is the alarm.

## Verify
- [ ] Self-test passed; disinfectant residual negative; concentrate matches prescription.
- [ ] Conductivity within range and independently checked if required.
- [ ] Alarm limits tight; access and lines visible throughout.
- [ ] Each alarm handled by cause, never repeatedly silenced.
- [ ] Total chlorine ≤ 0.1 mg/L logged each shift; cultures/endotoxin within limits.
