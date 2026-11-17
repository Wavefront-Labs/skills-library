---
id: computing-software.it-support-helpdesk.troubleshooting-methodology.root-cause-analysis-and-post-incident-review
name: root-cause-analysis-and-post-incident-review
category: computing-software
field: it-support-helpdesk
product: troubleshooting-methodology
tags: [it-support-helpdesk, troubleshooting-methodology, root-cause-analysis, rca, post-incident-review, pir, five-whys, fishbone-diagram, timeline-reconstruction, blameless-postmortem, preventive-action, major-incident, contributing-factors]
level: practitioner
status: draft
description: "Write a formal RCA and run a post-incident review for a major incident: timeline reconstruction, 5 Whys taken to real depth, contributing-factor analysis, action tracking."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# root-cause-analysis-and-post-incident-review

Goal: produce an RCA that identifies something fixable, not just a
narrative that sounds thorough — this is the formal write-up that follows
the in-the-moment technique in `systematic-problem-isolation`, specifically
for major incidents that need documentation and follow-through.

## Timeline first, analysis second
- Before any "why" analysis, build a factual timeline: detection time,
  each action taken and by whom, each state change in the system, and
  resolution time — pulled from actual logs/ticket timestamps/chat
  records, not from memory days later. A timeline built from memory
  after the fact reliably compresses and reorders events, especially
  under multiple people acting concurrently.
- Separate **what happened** (facts, timestamped) from **what we think
  it means** (analysis) as distinct sections — mixing interpretation into
  the timeline makes it impossible for someone else to check your
  reasoning later.

## Taking 5 Whys to actual depth
- The failure mode of 5 Whys isn't asking "why" too few times, it's
  stopping at the first answer that *feels* satisfying rather than the
  one that's *actionable*. "The server ran out of disk space" →
  "because logs filled it" → "because log rotation wasn't configured" is
  three whys that sound complete but stop at a symptom (missing
  config) rather than a process cause (why wasn't it configured, why did
  no monitoring catch it approaching full, why did provisioning not
  include it by default).
- A good stopping point is a cause that, if fixed, would have prevented
  *this specific incident* and plausibly prevents a *class* of similar
  ones — "we added a monitoring alert for disk >80%" prevents a class;
  "we manually freed disk space" only prevents repeating this exact
  symptom.
- Multiple independent chains, not one: most real incidents have more
  than one contributing factor (the bug plus the missing alert plus the
  unclear escalation path that delayed response) — run the Whys down
  each contributing thread separately rather than forcing one single
  root cause when there were genuinely several.

## Fishbone / contributing-factor categories
- When a single Whys chain feels too linear for what was clearly a
  multi-factor incident, a fishbone (Ishikawa) sweep across categories —
  people, process, technology, environment — surfaces factors a purely
  linear "why" chain misses, e.g. "the on-call engineer was new and
  hadn't seen this alert type before" (people/process) alongside "the
  alert threshold was mistuned" (technology).
- Not every incident needs a full fishbone — reserve it for incidents
  complex or severe enough to justify a formal post-incident review, not
  routine tickets; using it on everything produces generic, low-signal
  output on simple cases.

## Blameless framing (and why it's not just etiquette)
- Name actions and system states, not people, as causal — "the deploy
  script lacked a rollback step" gets fixed; "Dana pushed a bad deploy"
  gets defensive, incomplete testimony in the next review, and nothing
  structural fixed. This isn't about being nice, it's that blame-framed
  RCAs measurably produce worse information because people stop being
  candid once they expect to be blamed.
- If a genuine process violation occurred (skipped a required approval,
  ignored a known runbook step), name the *gap in the process/guardrail*
  that allowed the violation, not just the individual action — a missing
  guardrail recurs with the next person even if this person is
  "corrected."

## Preventive actions: specific, owned, tracked to closure
- Each action item needs an owner, a due date, and a concrete
  deliverable — "improve monitoring" is not an action item; "add a disk-
  usage alert at 80% threshold on the logging volume, owned by X, due
  <date>" is.
- Track actions in the same system tickets/incidents are tracked in (a
  linked problem record or change request), not just in the RCA document
  itself — an action item that lives only in a document nobody revisits
  has a very high rate of quietly never happening; this is the most
  common way RCAs become a paperwork exercise instead of a prevention
  mechanism.
- Distinguish **immediate fix** (what stopped the active incident) from
  **preventive action** (what stops recurrence) explicitly — closing the
  incident ticket on the immediate fix alone, with no linked preventive
  action, is how the same incident recurs in 3 months.

## Gotchas
- "Human error" as a stated root cause is almost always incomplete — ask
  what in the system allowed that error to cause this much impact (lack
  of validation, no staging environment, no peer review) rather than
  stopping at the human action itself.
- A post-incident review held too long after the incident loses
  participants' specific recall of decisions made under pressure — aim
  to hold it within a few business days while memory and logs are both
  still fresh, not weeks later once it's been deprioritized.

## Verify
- The RCA's timeline is independently checkable against raw logs/
  tickets (not just narrated), each contributing-factor chain reaches an
  actionable cause (not a symptom), and every listed preventive action
  has an owner and a due date tracked in a system that gets reviewed —
  confirm closure of previous RCA action items as part of running the
  next one, not just producing new ones.
