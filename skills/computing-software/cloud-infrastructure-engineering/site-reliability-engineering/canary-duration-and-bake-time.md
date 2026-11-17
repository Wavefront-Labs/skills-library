---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.canary-duration-and-bake-time
name: canary-duration-and-bake-time
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [sre, release-canarying, canary-bake-time, canary-duration, statistical-power]
level: advanced
status: docs-checked
description: "Choose canary duration and bake time from release velocity, traffic volume, time of day, the metrics evaluated and their intervals, not a fixed habit."
sources: ["https://sre.google/workbook/canarying-releases/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Canary duration and bake time

**Goal:** canaries long enough to catch real problems and short enough to keep releases flowing.

## What drives duration (SRE Workbook, "Canarying Releases")
1. **Release velocity**: if you release daily you cannot let a canary last a week with one canary at a
   time; weekly releases allow fairly long canaries; continuous deployment (the book's example is 20 times a
   day) needs a significantly shorter duration.
2. **Size and duration are representative**: ending a canary after a handful of queries gives no useful
   signal for diverse queries. The higher the processing rate, the less time you need to get a representative
   sample that is attributable to the change and not a random artifact.
3. **Traffic volume**: enough traffic that the system handled a representative sample and had a chance to
   react negatively. The more homogeneous the requests, the less volume you need.
4. **Time of day**: performance defects typically manifest only under heavy load, so deploying off-peak
   likely will not trigger them.
5. **Metrics evaluated**: trivial metrics such as query success can be evaluated quickly; others, such as
   queue depth, may need more time or a larger canary population.
6. **Metric intervals**: make the interval of your metrics the same as or shorter than the canary duration.
   The book's example is a 30-minute canary evaluated with an hourly metric, which gives a muddied signal.

## Rules of thumb
- Run only one canary at a time (the book strongly advises it); overlapping canaries add mental effort and
  signal contamination.
- Include a traffic peak for changes to hot paths (follows from the time-of-day point).
- The requirements can conflict. Once you have metrics from past canaries, choose parameters from typical
  canary evaluation failure rates rather than hypothetical worst cases.
- Set bake time in requests or events as well as minutes; pick the numbers from your own service's history,
  since the book gives no universal figure.
- Don't let canary duration grow unboundedly: if you need hours, improve detection (better SLIs) or use smaller blast radius steps.

## Verify
- [ ] Release pipeline config documents per-stage bake time and minimum request counts; past incidents' detection times fall inside the bake windows.

## Checked
2026-11-01. Confirmed against the SRE Workbook "Canarying Releases" chapter (release velocity, representativeness,
traffic volume, time of day, metric choice, metric interval versus duration, one canary at a time, using past canary
rates). Removed: the stage/bake-time table, the 10,000 requests and 0.1% versus 0.2% figures, the failure-mode
latency list, and the AWS multi-region claim (the AWS article and the Release Engineering chapter were not
cited because their relevant text was not confirmed).
Method: documentation only; no commands were run.
