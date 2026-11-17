---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.incident-response-and-blameless-postmortems
name: incident-response-and-blameless-postmortems
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [site-reliability-engineering, sre, incident-response, incident-management, incident-commander, ic, communications-lead, operations-lead, scribe, severity-levels, sev1, declare-incident, mitigation-first, rollback, status-page, war-room, slack-incident-channel, pagerduty, incident-io, rootly, firehydrant, postmortem, blameless-postmortem, post-incident-review, timeline, contributing-factors, five-whys, action-items, learning-from-incidents, mttr, on-call]
level: practitioner
status: draft
description: "Run an incident with IC/comms/ops roles, mitigate before root-causing, update on a cadence; then write a blameless postmortem with timeline, contributing factors and owned actions."
sources: ["Google SRE Book - Managing Incidents and Postmortem Culture", "PagerDuty Incident Response documentation (response.pagerduty.com)", "John Allspaw - Blameless PostMortems and a Just Culture (Etsy Code as Craft)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Incident response and blameless postmortems — stop the bleeding, then learn

**Goal:** incidents are declared early, run by clear roles, mitigated fast, communicated
predictably, and turned into fixes that actually ship — without anyone being punished for
having been at the keyboard.

## 1. Severity and declaration
| Sev | Definition (example) | Response |
|---|---|---|
| 1 | critical journey down or data loss/security for many users | page IC + on-call, exec notified, status page within 15 min |
| 2 | major degradation or one key customer down | page on-call, IC assigned |
| 3 | minor, workaround exists | business hours ticket |
Rule: **declare on suspicion, downgrade later.** Declaring costs a channel; not declaring costs coordination. Anyone may declare.

## 2. Roles (Incident Command System, scaled down)
- **Incident Commander (IC):** owns decisions and coordination, does *not* debug. Assigns work, sets next update time, decides on rollback.
- **Ops/tech lead:** drives the technical investigation, the only one (or team) making production changes.
- **Comms lead:** status page, stakeholder and support updates on a fixed cadence (e.g. every 30 min for Sev1, even if "no change").
- **Scribe:** timestamps decisions and actions in the channel/doc — this becomes the postmortem timeline.
On small teams one person may hold two roles; never the IC and the hands-on debugger for long.

## 3. Mitigate first
Order of preference: roll back the last change → fail over / shift traffic → disable the feature flag → shed load / rate-limit → scale up → only then a forward fix. Root cause can wait; users can't.
Ask in the first 10 minutes: "What changed?" (deploys, config, flags, dependency status, traffic).

## 4. Hand-offs and ending
- Handover is explicit: "You are now IC" / "I am IC", stated in the channel.
- Resolve when user impact ends; keep monitoring. Open the postmortem doc before people disperse.

## 5. Blameless postmortem
Required for every Sev1/2 and for any incident consuming > ~20% of an error budget.
Structure:
1. Summary and impact (users, duration, budget consumed, money if known).
2. **Timeline** from detection to resolution, from the scribe log and system data (UTC).
3. **Contributing factors**, not "root cause": complex failures have several (a latent bug + a missing alert + a confusing runbook + a deploy at 17:55 Friday).
4. What went well, what was hard, where we got lucky.
5. **Action items:** each with owner, priority and due date; types — prevent, detect, mitigate.

Blameless means: describe actions and the context that made them reasonable at the time
("the dashboard showed green because…"), never "engineer X failed to". Ask "how did the
system make this easy to do?" Five-whys is fine as a prompt but tends to converge on a
single cause — follow multiple branches.

## 6. Make it stick
- Review meeting within 5 business days, attended by the teams owning action items.
- Track action-item completion rate; P1 items overdue appear in the weekly ops review.
- Tag postmortems (trigger type, service, contributing factor) so trends become visible across quarters.

## Gotchas
- Too many people in the incident channel: create a separate stakeholder channel for updates.
- Debugging in the incident channel by six people at once — the IC assigns threads.
- Postmortems that end with "be more careful" or "add training" have no engineering fix; push for a system change.
- Action items without owners or due dates don't happen.
- Blame leaks through wording ("should have", "obviously") — edit it out in review.

## Verify
- [ ] Severity definitions and who-can-declare are written and known by on-call.
- [ ] Every Sev1/2 in the last quarter had a named IC and a timestamped log.
- [ ] Status updates went out on the stated cadence.
- [ ] Postmortems exist for all Sev1/2, with contributing factors and owned, dated actions.
- [ ] Action-item completion rate is tracked and reviewed.

Uncertain: severity definitions and timings are examples; adapt to your organisation.
Related: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.error-budget-policy, computing-software.cloud-infrastructure-engineering.cloud-architecture.disaster-recovery-planning
