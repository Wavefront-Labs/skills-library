---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.production-readiness-review-and-launch-coordination
name: production-readiness-review-and-launch-coordination
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [site-reliability-engineering, sre, production-readiness-review, prr, launch-checklist, launch-coordination, lce, gradual-rollout, dark-launch]
level: advanced
status: docs-checked
description: "Run launches and Production Readiness Reviews the SRE Book way: curated launch checklist, staged rollouts, feature flags, client-behaviour and overload checks."
sources: ["https://sre.google/sre-book/reliable-product-launches/", "https://sre.google/sre-book/evolving-sre-engagement-model/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Production readiness review and launch coordination

**Goal:** launches and service hand-overs go through a lightweight, repeatable review so the first days in production
are uneventful.

## 1. The Production Readiness Review (SRE Book, Evolving SRE Engagement Model)
- A PRR identifies the reliability needs of a service from its specifics and is a prerequisite for an SRE team to
  take on production responsibility. Its objectives: verify the service meets accepted standards of production setup
  and operational readiness, and improve its reliability to minimise the number and severity of expected incidents.
- Production aspects SRE looks at: system architecture and interservice dependencies; instrumentation, metrics and
  monitoring; emergency response; capacity planning; change management; performance (availability, latency,
  efficiency).
- Simple PRR phases: Engagement (agree SLO/SLA, disruptive design changes, training schedule), Analysis (a
  service-specific checklist built from domain expertise and the Production Guide; also review recent incidents,
  postmortems and follow-ups), Improvements and Refactoring (prioritise by reliability importance, negotiate a plan
  with the development team), Training, Onboarding (progressive transfer of operations, change management and
  access; developers stay available to back SRE up), Continuous Improvement.
- Example analysis questions from the chapter: do updates impact an unreasonably large percentage of the system at
  once; does the service use the right serving instance of each dependency (user requests should not depend on a
  batch-oriented system); are all user-visible request failures instrumented and monitored with suitable alerting;
  does it report exceptional conditions to central logging.
- Early engagement: involving SRE at design time is cheaper than fixing later, and SRE can help with launch patterns
  such as a dark launch (copy part of live traffic to the new service and discard its responses). Where SRE
  cannot give full support, documentation and consultation are the alternatives; launch consultation is typically a
  few hours of one or two SREs studying the design, then advising the development team.

## 2. The launch checklist (SRE Book, Reliable Product Launches at Scale)
- Checklists reduce failure and give consistency. Each entry is a question with an action item and a pointer to more
  information (for example: persistent data stored, so implement backups; could a user abuse the service, so
  implement rate limiting and quotas).
- Curate it: every question's importance must be substantiated, ideally by a previous launch disaster; every
  instruction must be concrete, practical and reasonable for developers. Update it continuously and review the whole
  list once or twice a year for obsolete items.
- Prefer replacing long requirement sections with a pointer to shared infrastructure ("implement rate limiting
  using system X"); that drives convergence on common infrastructure.
- Launch process criteria in the chapter: lightweight, robust, thorough, scalable, adaptable. Tactics: simplicity, a
  high-touch approach customised by experienced engineers, and fast common paths for recurring launch classes
  (low-risk launches get a near-trivial checklist; the chapter's example is no new server executables and under 10
  percent traffic increase). Burdensome processes get sidestepped.
- Checklist themes the chapter develops, with example questions and actions:
  - Architecture and dependencies: request flow from user to frontend to backend; separate user-facing from
    non-user-facing requests; validate request-volume assumptions (one page view can become many requests).
  - Integration: DNS name, load balancer, monitoring setup for the new service.
  - Capacity planning: is the launch tied to a press release or promotion; expected traffic and growth; compute
    obtained. Launch spikes can differ in traffic mix from steady state, and some products saw spikes up to 15
    times the estimate; launching one region or country at a time builds confidence. Capacity interacts with
    redundancy (three deployments needed at peak means maintaining four or five).
  - Failure modes: single points of failure; mitigating dependency unavailability at startup and at runtime; request
    deadlines; load shedding.
  - Client behaviour: auto-save, auto-complete, heartbeat or periodic sync; exponential backoff on failure; jitter
    on automatic requests.
  - Processes and automation: document every manual process so any team member can run it in an emergency;
    automate building and releasing.
  - Development process: all code and configuration in version control; release branches.
  - External dependencies: third-party code, data, services; whether partners need notice; what happens if the
    vendor misses a hard deadline.
  - Rollout planning: a launch plan with an owner per item, risk per step and contingency measures.

## 3. Techniques for reliable launches
- Gradual and staged rollout: install on a few machines in one datacenter, observe for a defined period, then the
  whole datacenter, then globally. First stages are canaries. Tooling observes new servers and rolls back
  automatically if they fail validation. Mobile app staged percentages and rate-limited or invite-based signup are
  the same idea.
- Feature flag frameworks: roll out many changes in parallel, each to a few servers, users, entities or datacenters;
  ramp to a limited group (usually 1 to 10 percent); route by user, session, object or location; handle failure of
  new code paths without affecting users; revert each change independently; measure the user-experience effect.
- Abusive client behaviour: a client syncing every 60 seconds instead of every 600 causes 10 times the load; retries
  need exponentially increasing delay with random jitter and only for retryable errors (a network error usually,
  a 4xx usually not); choose random times for periodic jobs rather than 2 a.m. for everyone. Server-controlled client
  configuration and dormant client-side functionality make a launch easy to abort by switching the feature off.
- Overload and load tests: service behaviour near overload is hard to predict from first principles (the chapter
  gives debug logging that cost more than handling the response, and GC thrashing on the JVM). Load testing is
  required for most launches.

## Verify
- [ ] The service has a completed PRR or launch checklist with an owner on every action item.
- [ ] Each checklist question traces to a past incident or a stated reason; stale items are pruned on a schedule.
- [ ] The rollout plan names stages, observation periods, contingency and who is responsible for each step.
- [ ] Clients back off with jitter and a server-side switch can disable the new feature.

## Checked

Checked 2026-11-09. Confirmed against the SRE Book chapters Reliable Product Launches at Scale and The Evolving SRE
Engagement Model. Removed: the Workbook engaging-with-SRE source (404) and the Release Engineering source (not used),
the ten-section PRR template with 0 to 3 scoring, the dated checklist example with T-minus deadlines, the 2x load test
rule, the 48 hour freeze, roles on launch day, hyper-care period, the readiness bot idea and the abort-threshold example,
none of which appear on the pages read.

Method: docs-checked 2026-11-09 against the pages above, read from downloaded copies; no commands were run.
