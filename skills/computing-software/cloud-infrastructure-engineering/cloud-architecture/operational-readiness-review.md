---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.operational-readiness-review
name: operational-readiness-review
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, operational-excellence, operational-readiness-review, production-readiness, launch-checklist, orr]
level: practitioner
status: docs-checked
description: "Run an operational readiness review: checklist built from incident lessons, self-assessment, early engagement, improvement phase and keeping the checklist current."
sources: ["https://docs.aws.amazon.com/wellarchitected/latest/operational-readiness-reviews/wa-operational-readiness-reviews.html", "https://sre.google/sre-book/evolving-sre-engagement-model/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Operational readiness review (ORR)

## What the sources say
- AWS created the ORR to distil lessons from operational incidents into curated questions with
  best-practice guidance. It follows the Correction of Errors (COE) post-incident analysis: a COE
  prevents recurrence in the workload where it happened, the ORR stops known, preventable risks
  in other workloads. It supplements Well-Architected reviews with lessons specific to your
  business, culture, tools and governance rules.
- AWS generates different checklist templates from the question set based on the workload and
  outcome wanted; teams self-assess against the right checklist across the service lifecycle, from
  inception to post-release operations.
- Google SRE's Production Readiness Review (PRR) verifies that a service meets accepted standards
  of production setup and operational readiness and improves reliability, minimising the number
  and severity of expected incidents.

## Areas to cover (from the SRE book)
SRE concerns: architecture and interservice dependencies; instrumentation, metrics and
monitoring; emergency response; capacity planning; change management; performance (availability,
latency, efficiency). Example checklist questions from the book:
- Do updates impact an unreasonably large percentage of the system at once?
- Does the service connect to the appropriate serving instance of its dependencies (end-user
  requests should not depend on a batch-processing system)?
- Does it request sufficient network quality of service for critical remote services?
- Are errors reported to central logging, and are user-visible failures instrumented, monitored
  and alerted?
Reviewers also read recent incidents, postmortems and follow-up tasks to gauge the demand for
emergency response.

## Steps
1. Engage early: the SRE book says the earlier the review, the better and cheaper the fix; early
   engagement in design lowers time to onboard. A PRR can start at any lifecycle stage.
2. Agree the process and goals (SLO or SLA, any disruptive design changes, training plans).
3. Analysis: reviewers assess against a service-specific checklist built from domain expertise,
   related systems and a production best-practice guide.
4. Improvements: prioritise by importance to reliability, negotiate with the development team,
   and work on them together.
5. Training and onboarding where the operations team takes over.
6. Continuous improvement: feed lessons from incidents and postmortems back into the guide and
   checklist.

## Gotchas
- A late review mostly finds problems that are costly to unwind.
- Not every service needs full SRE management; the book treats documentation, consultation or a
  shared platform as valid alternatives.

## Verify
- [ ] Review record with evidence for each question and tracked, owned improvements.
- [ ] Checklist updated from recent incidents.

## Checked
2026-11-08. Confirmed against the AWS "Operational Readiness Reviews" paper (origin in COE,
curated questions, checklist templates, self-assessment through the lifecycle) and chapter 32 of
the Google SRE book (PRR objectives, phases, example questions, early engagement, alternatives).
Removed: the generic checklist table (observability, cost, security items), the "2-4 weeks before
launch" timing, the "load test to peak x 2" and "30-day" style figures and the sign-off outcome
categories, none of which the pages state. The AWS operational excellence welcome page was dropped
from sources (not relied on).
Method: documentation only; no commands were run.
