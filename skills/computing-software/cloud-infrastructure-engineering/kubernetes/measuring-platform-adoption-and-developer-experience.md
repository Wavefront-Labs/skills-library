---
id: computing-software.cloud-infrastructure-engineering.kubernetes.measuring-platform-adoption-and-developer-experience
name: measuring-platform-adoption-and-developer-experience
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [developer-experience, dx-metrics, platform-adoption, dora-metrics, space-framework, devex-survey, time-to-first-deploy, golden-path-adoption-rate, platform-kpis, internal-nps]
level: advanced
status: docs-checked
description: "Instrumenting golden-path adoption, time-to-first-deploy, and DX survey signals so a platform team can prove impact instead of asserting it."
sources: ["https://dora.dev/guides/dora-metrics/", "https://tag-app-delivery.cncf.io/whitepapers/platforms/", "https://queue.acm.org/detail.cfm?id=3454124", "https://github.com/backstage/backstage/blob/master/docs/plugins/analytics.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Measuring platform adoption and developer experience

**Goal:** give the platform team's product/roadmap work
(`computing-software.cloud-infrastructure-engineering.kubernetes.platform-team-operating-model-and-platform-as-a-product`)
real numbers instead of anecdotes — which golden paths are actually used,
whether using them makes teams faster, and whether developers would tell a
colleague to use them. Numbers that survive a skeptical budget review, not
vanity dashboards.

## 1. Adoption metrics — usage, not deployment
Instrumenting *usage* of the platform's own surfaces is the first and
cheapest signal:
- **Golden-path adoption rate**: % of new services created via the
  Backstage scaffolder (or equivalent) vs. hand-rolled from scratch, tracked
  from scaffolder/template invocation events (Backstage's analytics API
  emits a `create` event per Software Template run, with the template ref and
  the `backstage.io/time-saved` value if set; capture them into whatever
  analytics the org already has rather than building new pipes).
- **Template/action usage breakdown**: which templates get used repeatedly
  vs. created once and abandoned — a template with high one-time use and no
  repeat use is a signal the golden path doesn't actually fit that archetype.
- **Self-service vs. ticket ratio**: requests fulfilled via the platform API
  (a Crossplane claim, a scaffolder run) vs. requests that still went
  through a human (a Slack ask, a ticket) for the same job — rising
  self-service ratio for a given capability is the clearest "this golden
  path is working" signal there is.
- **Catalog freshness**: % of catalog entities with a recent commit/deploy
  vs. stale — a proxy for whether the catalog (and therefore the platform's
  source of truth) is still trusted and actively maintained.

## 2. Flow metrics — DORA, scoped to the platform's actual influence
DORA's current five software delivery metrics (change lead time, deployment
frequency, failed deployment recovery time, change fail rate, deployment
rework rate; the original "four keys" used MTTR) are organization-wide
outcomes, not platform-team-owned ones — a platform team claiming full credit (or blame)
for them overclaims. The honest framing: track DORA metrics **segmented by
golden-path adoption** (teams on the paved road vs. teams who aren't) to
show correlation, and track a platform-specific leading indicator the team
*does* fully own: **time-to-first-deploy** for a brand-new service (from
`scaffolder run` to first successful production deploy). This is the
cleanest "platform caused this" number because the platform is the entire
mechanism between those two events.

## 3. DX survey signal — the qualitative half
Quantitative usage numbers miss *why* adoption is low or friction persists.
The CNCF Platforms white paper suggests NPS-style satisfaction surveys and
developer-productivity metrics such as those in the SPACE framework (read the
paper for its dimensions). Run a short, recurring DX survey with questions
such as: would you recommend this golden path to a teammate; did using the
platform help you ship; how much of your last sprint was lost to
environment/infra friction (self-reported). Keep it short enough to actually
get responses (a 40-question quarterly survey gets ignored after the first
round) and publish aggregate results back to respondents — a survey that
visibly changes nothing trains people to stop answering it.

## 4. The trap: optimizing the metric instead of the outcome
Once "golden-path adoption %" is a tracked KPI, there's pressure to inflate
it by mandating usage rather than earning it — which undermines the
platform-as-a-product principle in the operating-model skill and produces
adoption numbers that look great while satisfaction numbers quietly tank.
Always pair an adoption metric with a satisfaction metric from the same
cohort; a platform "succeeding" on usage while failing on NPS is a platform
about to be worked around the moment a mandate lifts.

## 5. Practical instrumentation notes
- Backstage ships an analytics API, and analytics modules (for example
  `analytics-module-ga4`, `analytics-module-matomo` in backstage/community-plugins)
  forward its events to common analytics backends —
  wire this early; retrofitting usage tracking after a year of
  "we think adoption is good" is much harder than instrumenting from day
  one, even crudely.
- Time-to-first-deploy needs a clear start event (scaffolder invocation
  timestamp) and end event (first successful prod deploy, from CI/CD, not
  CI *trigger*) — define both precisely before reporting the number, or
  different teams will compute it differently and the metric becomes
  useless for comparison.
- Segment every metric by team/cohort size and tenure — a single aggregate
  number hides whether the platform is working well for new teams but
  poorly for long-tenured ones with legacy systems (or the reverse), which
  is usually the more actionable finding.

## Verify
- Time-to-first-deploy for a service created via the golden path today is
  measurably lower than for a hand-rolled service from before the platform
  existed, using the same start/end event definitions for both.
- The self-service vs. ticket ratio for at least one platform capability has
  a documented trend over at least two quarters, not just a single
  point-in-time snapshot.
- The most recent DX survey's results were published back to the people who
  took it, and at least one roadmap item cites a specific survey finding as
  its justification.

## Checked
2026-10-27, against the DORA metrics guide (dora.dev, fetched today), the CNCF TAG App Delivery Platforms white paper and Backstage `docs/plugins/analytics.md` (backstage/backstage master). Confirmed: DORA's five current metrics and the move from MTTR, the white paper's NPS and SPACE suggestions, and Backstage's analytics API, community analytics modules and the scaffolder `create` event. SPACE dimension names are not restated because the paper (ACM Queue) blocked automated fetching.
Method: documentation only; no commands were run.
