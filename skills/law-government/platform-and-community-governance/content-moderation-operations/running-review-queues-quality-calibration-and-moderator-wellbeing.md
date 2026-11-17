---
id: law-government.platform-and-community-governance.content-moderation-operations.running-review-queues-quality-calibration-and-moderator-wellbeing
name: running-review-queues-quality-calibration-and-moderator-wellbeing
category: law-government
field: platform-and-community-governance
product: content-moderation-operations
tags: [platform-and-community-governance, content-moderation-operations, content-moderation, trust-and-safety, t-and-s, moderation-queue, review-queue, prioritisation, triage, sla, user-reports, flagging, classifier, proactive-detection, hash-matching, human-review, bpo, outsourced-moderation, quality-assurance, qa-sampling, calibration, inter-rater-agreement, accuracy, escalation-path, crisis-protocol, moderator-wellbeing, resilience, exposure-limits, grayscale, ncmec, csam-reporting]
level: practitioner
status: draft
description: "Run content moderation at scale: queue design and prioritisation by severity, SLAs, QA sampling and calibration, escalation paths, crisis surges, and protecting moderator wellbeing."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Running review queues, quality calibration and moderator wellbeing

**Goal:** the right content gets the right decision fast enough to matter, decisions are
consistent across reviewers and sites, and the people doing it aren't harmed by the job.

## 1. Intake and queue design
Sources: user reports, trusted flaggers, automated classifiers, hash-matching against
known-bad databases, legal requests, internal escalations.
- **Route by policy area and language** to trained reviewer pools; specialised queues
  for child safety, terrorism, self-harm, legal requests.
- **Prioritise by severity × reach × time-sensitivity**, not first-in-first-out:
  imminent harm (suicide threats, credible violence, live-streamed attacks, child
  exploitation) jumps every queue.
- Set **SLAs per priority tier** (e.g. minutes for imminent harm, hours for high,
  days for low) and staff to the forecast volume per language and time zone.
- Deduplicate: one decision should resolve all reports on the same item.
- Automation: auto-action only where precision is very high and measured; otherwise
  use classifiers to rank and pre-fill, with a human deciding.

## 2. Mandatory reporting
Certain content triggers legal obligations — e.g. US providers must report apparent
child sexual abuse material to NCMEC's CyberTipline, and other jurisdictions have their
own channels and preservation duties. **These vary by jurisdiction**; build them into
the tooling with legal sign-off, and never let reviewers download or forward such material.

## 3. Quality and consistency
- **QA sampling:** independent reviewers re-check a random sample per reviewer and per
  queue (plus targeted samples of high-risk decisions). Track accuracy against the
  policy owner's ruling, not the QA reviewer's opinion.
- **Calibration sessions** weekly: reviewers, QA and policy discuss disputed cases;
  outcomes become new internal examples.
- Measure **inter-rater agreement** on a common "golden set"; drops after a policy
  change signal unclear guidance.
- Feed appeal overturn data back by reviewer, queue and policy line.
- Keep a **decision log** with reasons for anything escalated.

## 4. Escalation paths
Define tiers: frontline → senior/specialist reviewer → policy team → legal/comms/
executive. Write criteria for each (public figures, newsworthy content, law
enforcement threat to life, possible regulator interest, media attention). Provide a
24/7 on-call path for imminent-harm cases, including law-enforcement emergency
disclosure procedures.

**Crisis protocol** (attacks, elections, conflicts): pre-agreed surge staffing, temporary
classifier thresholds, war-room roles, communication templates, and a stand-down review.

## 5. Moderator wellbeing (non-optional)
Reviewers of graphic and abusive content face documented risks of trauma symptoms.
- Informed consent at hiring; realistic previews of content.
- **Exposure controls:** caps on time in the most graphic queues, rotation to lower-
  severity work, mandatory breaks.
- Tooling: grayscale and blur by default, muted audio, click-to-reveal, thumbnails.
- Access to **qualified psychological support** (not just a hotline), during and after
  employment; peer support.
- Productivity targets that don't punish taking breaks.
- Apply the same standards to outsourced (BPO) vendors through contract and audit.

## Metrics dashboard
Volume by source and queue; time-to-action per tier; accuracy (QA); appeal rate and
overturn rate; prevalence estimates (sampled views of violating content); reviewer
attrition and wellbeing indicators.

## Verify
- [ ] Queues prioritised by severity and reach, with SLAs per tier.
- [ ] Mandatory-reporting flows built and legally reviewed.
- [ ] QA sampling, golden-set agreement and calibration running on schedule.
- [ ] Escalation criteria and 24/7 imminent-harm path documented.
- [ ] Wellbeing controls in tooling, scheduling and vendor contracts.
