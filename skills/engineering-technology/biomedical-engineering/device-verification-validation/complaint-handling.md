---
id: engineering-technology.biomedical-engineering.device-verification-validation.complaint-handling
name: complaint-handling
category: engineering-technology
field: biomedical-engineering
product: device-verification-validation
tags: [complaint-handling, post-market-surveillance, capa, medical-device-reporting, mdr-reporting, vigilance, complaint-investigation, trending]
level: practitioner
status: gated
description: "Run a device complaint process: intake, triage, investigation, reportability decisions, trending and links to CAPA, ISO 13485 and FDA and EU adverse event reporting."
sources: ["ISO 13485 Medical devices - Quality management systems (feedback and complaint handling; confirm edition)", "21 CFR 820.35 and ISO 13485 clause 8.2.2 (complaint records, https://www.ecfr.gov/current/title-21/part-820/section-820.35)", "21 CFR Part 803 Medical Device Reporting https://www.ecfr.gov/current/title-21/part-803", "Regulation (EU) 2017/745 Articles 87 to 92 https://eur-lex.europa.eu/eli/reg/2017/745/oj"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Complaint handling

**Goal:** capture every complaint, decide quickly whether it is reportable, investigate the cause and feed trends into design and CAPA.

Regulatory process. Checked on 2026-10-19: 21 CFR 803.50 (30 calendar days) and 803.53 (5 work days) on eCFR; MDR Article 87(3), (4), (5) (15, 2 and 10 days) on EUR-Lex; 21 CFR 820.35(a) now adds complaint-record requirements on top of ISO 13485 clause 8.2.2 (the ISO text (gated: unconfirmed, source is paywalled or blocked)). Reporting deadlines and criteria below are summarised and must be confirmed against the current regulations of each market.

## Process
1. **Intake:** a single channel and log (sales, service, customer care, social, literature); record date received, product, lot or serial, event description, patient involvement and reporter contact. Do not ask patients for clinical advice; direct them to clinicians.
2. **Triage within a day:** does it involve death or serious injury or a malfunction that could cause it? Does it suggest a safety trend?
3. **Reportability assessment** (documented for each complaint):
   - US: manufacturer reporting under 21 CFR 803, generally within 30 calendar days of becoming aware of a reportable death, serious injury or malfunction, and within 5 work days for events needing remedial action to prevent unreasonable risk of substantial harm.
   - EU MDR: serious incident reports generally within 15 days, shorter for a serious public-health threat (2 days) and for death or unanticipated serious deterioration (10 days) per Article 87.
   - Other jurisdictions have their own rules (UK, Canada, Japan, Australia).
4. **Investigation:** retrieve the device (or data and images), reproduce, review production records and risk file; decide root cause or "cause not determined" with rationale; record whether a design, process, labelling or use error is involved.
5. **Closure and response** to the complainant per policy; keep records for the required retention period.
6. **Trending:** rate by product and failure mode against sales or use; pre-set thresholds trigger CAPA (see capa-process) and risk-file review.
7. **Feedback:** update the ISO 14971 risk file, post-market surveillance report and clinical evaluation.

## Gotchas
- Complaints received by distributors or service staff that never reach quality.
- Closing "no fault found" without trying to reproduce.
- Not linking complaints to the same lot or supplier.

## Verify
- [ ] Every complaint has a reportability decision and date stamps.
- [ ] Reports submitted within deadlines (audit sample).
- [ ] Trending report reviewed in management review.
