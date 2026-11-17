---
id: law-government.platform-and-community-governance.appeals-and-dispute-adjudication.designing-and-deciding-user-appeals
name: designing-and-deciding-user-appeals
category: law-government
field: platform-and-community-governance
product: appeals-and-dispute-adjudication
tags: [appeals-and-dispute-adjudication, platform-and-community-governance, user-appeals, content-appeals, account-reinstatement, reinstatement-decision, internal-complaint-handling, dsa-article-20, out-of-court-dispute-settlement, dsa-article-21, oversight-board, independent-review, de-novo-review, standard-of-review, due-process, procedural-fairness, natural-justice, statement-of-reasons, case-review, appeal-sla, overturn-rate, marketplace-disputes, buyer-seller-disputes, chargeback-style-disputes, precedent, case-notes, decision-letter, trust-and-safety]
level: practitioner
status: draft
description: "Design and decide platform appeals: who can appeal what, intake, independent de novo review, written reasons, reinstatement, buyer-seller disputes, oversight-body referrals and learning loops."
sources: ["EU Digital Services Act, Articles 17, 20 and 21", "Santa Clara Principles (2021) on notice and appeal", "Published decisions and charter of the Oversight Board (Meta)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Designing and deciding user appeals

**Goal:** a process where users who believe an enforcement decision (or a dispute with
another user) was wrong get a fair, timely second look by someone new, with written
reasons — and where the platform learns from what appeals reveal. Reference regime: the
EU Digital Services Act (internal complaint handling and certified out-of-court dispute
settlement bodies), plus voluntary models such as independent oversight boards. Other
markets impose fewer formal duties; check local consumer, platform and marketplace law.

## 1. Decide what is appealable
- Content removal, labelling and reach restrictions; account suspension and termination;
  monetisation decisions; marketplace listing removals.
- Also let **reporters** appeal a "no violation" decision where feasible (the DSA expects
  complaint routes for notifiers too).
- State the appeal window (the DSA sets a minimum period after the decision — at least
  six months; confirm against the current text) and the limits (e.g. one appeal per decision).

## 2. Intake
- Link from every enforcement notice directly to the appeal form, pre-filled with the
  decision ID, policy and content.
- Let the user explain context in free text and add evidence (e.g. "this was satire",
  "my account was hacked", "I own the copyright").
- Acknowledge receipt with an expected timeframe.

## 3. Review standards
- **Independence:** the appeal reviewer must not be the original decision-maker; route
  sensitive categories to specialists.
- **De novo** review on the policy in force at the time of the original decision, using all
  available context including the user's explanation.
- **Human review:** under the DSA, complaint decisions must not be taken solely by
  automated means; as a good practice anyway, automation can triage but a person decides.
- Evidence standard: "more likely than not" for most policy questions; a higher bar for
  permanent account termination.
- Decide one of: uphold; overturn and restore; modify (e.g. replace removal with a label,
  reduce suspension length). Overturns also remove the associated strike.

## 4. Write the decision
A short decision letter: what was reviewed, the policy, the outcome, the reason in one
or two plain sentences, any remaining restriction, and further options (out-of-court
dispute settlement, court, consumer bodies, oversight board where available). Never
reveal reporter identities or internal detection signals that would help abusers.

## 5. Reinstatement
Restore content and account state completely: followers, reach, monetisation,
verification; reset strike counts; notify the user. Track time-to-restore.

## 6. User-to-user disputes (marketplaces, sharing economy)
- Define evidence each side must provide (tracking, photos, messages) and deadlines.
- Decide on documented evidence with consistent rules on burden (e.g. seller proves
  delivery; buyer proves "not as described").
- Offer clear remedies: refund, partial refund, return, release of funds; explain the
  route to external redress.

## 7. Oversight and external referrals
For platforms with an independent oversight body or certified out-of-court dispute
settlement: prepare the case file (decision history, policy, rationale), respond within
the body's deadlines, implement binding outcomes, and publish responses to policy
recommendations.

## 8. Learn from appeals
Monthly analysis: overturn rate by policy, reviewer, vendor, language, and detection
source (classifier vs human). High overturn rates trigger policy clarification,
classifier retraining or reviewer coaching. Keep precedent case notes for hard cases so
future decisions are consistent.

## Gotchas
- Same reviewer, same queue, same mistake — appeals that only re-run the original process.
- Automated "appeal denied" with no reasons; users and regulators treat it as no appeal.
- Restoring content but leaving the strike or demotion in place.
- Backlogs that make suspension appeals meaningless after the suspension ends.

## Verify
- [ ] Appealable decisions, window and limits published; reporters also have a route.
- [ ] Independent, human, de novo review with a defined evidence standard.
- [ ] Decision letters give reasons and next options without exposing reporters.
- [ ] Full reinstatement checklist including strike reset.
- [ ] Monthly overturn analysis feeds policy, tooling and training.
