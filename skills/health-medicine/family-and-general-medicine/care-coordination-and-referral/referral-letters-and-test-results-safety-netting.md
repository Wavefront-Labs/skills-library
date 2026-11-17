---
id: health-medicine.family-and-general-medicine.care-coordination-and-referral.referral-letters-and-test-results-safety-netting
name: referral-letters-and-test-results-safety-netting
category: health-medicine
field: family-and-general-medicine
product: care-coordination-and-referral
tags: [family-and-general-medicine, care-coordination-and-referral, referral, referral-letter, specialist-referral, consultant-letter, two-week-wait, 2ww, urgent-suspected-cancer, nice-ng12, referral-thresholds, advice-and-guidance, e-consult, safety-netting, results-management, test-results, abnormal-results, results-follow-up, closing-the-loop, tracking-referrals, lost-to-follow-up, care-transitions, discharge-summary, handover, sbar, patient-safety, diagnostic-error, primary-care]
level: practitioner
status: draft
description: "Decide when and how urgently to refer, write a specialist letter that gets triaged correctly, and run a closed-loop system so referrals and abnormal results are never lost."
sources: ["NICE NG12 Suspected cancer: recognition and referral (2015, updated)", "RCGP/Cancer Research UK safety-netting guidance", "Royal College of Physicians / PRSB standards for outpatient letters and referrals", "AHRQ, Improving Your Office Testing Process toolkit"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

*General clinical/professional reference on primary-care systems and correspondence, not patient-specific advice. Local referral pathways and criteria take precedence.*

# Referral letters and test-results safety-netting

**Goal:** the right patient reaches the right service at the right speed, the specialist
can triage from your letter alone, and nothing you ordered or referred silently falls
through the gaps. Missed follow-up of results and referrals is one of the commonest causes
of diagnostic harm and litigation in primary care.

## 1. Decide: refer, ask, or keep
- **Keep** if you can manage it with time, a trial of treatment, or local guidance.
- **Ask** (advice-and-guidance / e-consult) when you need a specialist opinion but not a
  clinic slot — often faster and avoids a wasted appointment.
- **Refer** when the patient needs a test, procedure or expertise you can't provide.
- **Urgency:** emergency (same day), urgent suspected cancer (UK 2-week-wait / NG12 criteria;
  other systems have equivalents), urgent (weeks), routine. Use the pathway's criteria
  literally — triage teams downgrade letters that don't state which criterion is met.
- Check the patient *wants* referral and can attend; explain what happens next.

## 2. Write the letter (the specialist triages from it)
Structure (SBAR-like):
1. **The question** — first line: "Please assess for ? inflammatory arthritis; I'd value
   your opinion on DMARD initiation." One clear question.
2. **Urgency and criterion** — "Urgent suspected cancer: age 62, unexplained iron-deficiency
   anaemia (NG12)."
3. **Key history** — onset, course, red flags present *and* absent.
4. **Examination** — relevant positives/negatives.
5. **Investigations so far** — with dates and values, not "bloods normal".
6. **What's been tried** — drugs, doses, duration, response.
7. **Background** — PMH, current meds, allergies, anticoagulation.
8. **Patient factors** — interpreter, mobility, capacity, carer, preferences, what they've
   been told.

Keep it to one screen. Attach (don't paste) long results.

## 3. Close the loop on referrals
- Log every urgent referral in a tracker (EHR task or register) with an expected date.
- Check receipt and appointment booked within the pathway timeframe (e.g. within 1–2 weeks
  for suspected cancer); chase if not.
- Tell the patient to contact you if they haven't heard by a specific date.
- When the clinic letter arrives, action it: med changes, tests requested of you, follow-up.

## 4. Results management
- **Whoever orders the test owns the result.** Make that explicit in team policy, including
  for locums and trainees.
- Every test ordered → appears in a tracked "pending" list until resulted and filed.
- File each result with an action: normal-no-action, normal-inform, abnormal-routine,
  abnormal-urgent. "Seen" without an action is not filed.
- Tell patients how they'll get results; never use "no news is good news".
- Critical values: a phone pathway out of hours, with a named responder.
- Audit periodically: pick 20 abnormal results and check each was acted on.

## 5. Safety-netting the patient (every consultation with uncertainty)
State: what you think it is, what would make you worry (specific symptoms), what to do and
how fast (who to call, A&E/999/911), and when to come back if not better. Document the
advice given, not just "safety-netted".

## Gotchas
- Results return to the ordering clinician's inbox after they've left or are on leave —
  configure cover/redirection.
- Rejected or downgraded referrals often come back by letter weeks later; the tracker
  should flag "rejected" as an action, not a filing.
- Patients who DNA a cancer appointment are high risk: contact them, don't just re-refer.
- Copying the patient into letters (plain language) reduces errors and improves trust.
- Uncertainty: exact criteria and timeframes differ by country and change; always check
  the current local pathway before relying on any threshold here.

## Verify
- [ ] Letter opens with a single explicit question and stated urgency/criterion.
- [ ] Investigations listed with dates and values.
- [ ] Urgent referral logged in a tracker with a chase date.
- [ ] Patient told what happens next and when to chase.
- [ ] Results pending list empty of unfiled items older than its agreed turnaround.
- [ ] Safety-net advice documented specifically.
