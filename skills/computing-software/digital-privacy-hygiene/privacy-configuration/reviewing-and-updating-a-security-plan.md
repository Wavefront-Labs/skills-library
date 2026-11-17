---
id: computing-software.digital-privacy-hygiene.privacy-configuration.reviewing-and-updating-a-security-plan
name: reviewing-and-updating-a-security-plan
category: computing-software
field: digital-privacy-hygiene
product: privacy-configuration
tags: [digital-privacy-hygiene, privacy-configuration, security-plan-review, threat-modeling, threat-model, risk-assessment, security-plan]
level: practitioner
status: docs-checked
description: "Revisit a personal or family security plan on a schedule and after life changes: re-answer the threat-model questions, retest controls and retire useless measures."
sources:
  - "https://ssd.eff.org/module/your-security-plan"
  - "https://www.privacyguides.org/en/basics/threat-modeling/"
  - "https://www.cisa.gov/secure-our-world"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reviewing and updating a security plan

**Goal:** threat models go stale. A plan written two years ago may defend against the wrong person with tools
you no longer use.

## Triggers for a review
- Scheduled: EFF says to revisit the plan frequently: when you write it, mark your calendar for a future date to
  check it is still relevant. Pick an interval that suits you (for example yearly, with a backup restore test).
- Life changes (EFF: the plan changes as your situation changes): new job, public role, activism or press attention,
  breakup or custody dispute, move, travel, new child, caring for an older relative's accounts.
- Incidents: breach notification, phishing that got through, lost device, a harassment campaign.

## Re-answer EFF's questions
EFF lists six; Privacy Guides uses the first five.
1. What do I want to protect? (assets: data, where it is kept, who has access, what stops others)
2. Who do I want to protect it from? (adversaries, including careless trusted people)
3. How bad are the consequences if I fail?
4. How likely is it that I will need to protect it?
5. How much trouble am I willing to go through?
6. Who are my allies? (EFF only)
Write the answers down; compare with the last version and highlight what changed.

## Retest the controls (practical checklist; not drawn from the cited pages)
- Password manager: run its security report; fix reused/weak/breached.
- MFA: still on everywhere important; recovery codes still where you think; backup key still works.
- Recovery chain: recovery phone/email still current and controlled by you.
- Devices: updates current, encryption on, unsupported devices replaced.
- Exposure: self-search, data broker opt-outs re-run (listings come back).
- Backups: restore test passed.

## Prune
Both guides say to balance convenience, cost and privacy against your risk. Drop measures that cost effort without
matching a current threat; put the effort into the new top risk.

## Keep the plan
Date it and put a "next review" date in your calendar (EFF). EFF and Privacy Guides note the list of adversaries may
be something you want to destroy once planning is done, so think before storing it anywhere permanent.

## Verify
- [ ] Plan dated; next review date set; each top threat has at least one tested control.

## Checked
Checked 2026-11-08 against the full text of EFF "Your Security Plan" and Privacy Guides "Threat Modeling", and the
CISA Secure Our World page (read through a page fetch; it lists only four core steps and has no review schedule).
Corrected EFF's question count (six, not five), removed the 6-12 month interval and the Tor example as unsupported,
and labelled the control checklist as practical advice not from the sources.
Method: documentation only; no commands were run.
