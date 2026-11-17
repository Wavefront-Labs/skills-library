---
id: computing-software.devops-ci-cd.release-engineering.dora-quick-check-and-performance-clusters
name: dora-quick-check-and-performance-clusters
category: computing-software
field: devops-ci-cd
product: release-engineering
tags: [release-engineering, dora-quick-check, performance-clusters, four-keys]
level: intro
status: draft
description: "Run the DORA Quick Check survey to baseline delivery performance, interpret the performance clusters, and decide when survey data is enough versus system instrumentation."
sources: ["https://dora.dev/quickcheck/", "https://dora.dev/research/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Survey-based measurement and performance clusters

You do not need pipelines instrumented to start. DORA's research itself is survey-based.

## DORA Quick Check
dora.dev/quickcheck asks the four key questions (deployment frequency, lead time for changes,
change failure rate, failed deployment recovery time) with banded answers, then compares you with
the latest State of DevOps report and suggests capabilities to improve.

Run it per **team/service**, not per company: averages hide the struggling systems.

## Performance clusters
Annual reports group respondents into clusters (historically elite/high/medium/low; recent reports
use varying cluster descriptions). Typical "elite" profile: on-demand deploys (multiple per day),
lead time under a day, low change failure rate, recovery in under an hour. Exact thresholds shift
per report year; quote the year.

## Survey vs instrumentation
| Survey | Instrumented |
|---|---|
| minutes to run, no tooling | needs deploy/incident events |
| perception bias, coarse bands | precise, continuous |
| good for baselining many teams quickly | good for tracking change over time |

Start with the survey, pick one capability to improve (e.g. trunk-based development, test
automation), then instrument the metrics for the teams investing.

## Pitfalls
- Comparing teams to rank them: DORA metrics are for improvement, not performance reviews.
- Treating cluster labels as targets instead of the capabilities that drive them.

## Verify
- [ ] Each team has a dated baseline and a chosen capability to work on; re-survey after a quarter.
