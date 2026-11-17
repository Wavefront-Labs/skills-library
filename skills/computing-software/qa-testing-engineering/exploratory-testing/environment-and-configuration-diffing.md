---
id: computing-software.qa-testing-engineering.exploratory-testing.environment-and-configuration-diffing
name: environment-and-configuration-diffing
category: computing-software
field: qa-testing-engineering
product: exploratory-testing
tags: [environment-diff, bug-investigation, configuration-drift, isolation, works-on-my-machine]
level: practitioner
status: draft
description: "Isolate why a bug appears in one environment but not another: diff versions, config, feature flags, data, infrastructure and client factors systematically."
sources:
  - https://www.satisfice.com/rapid-testing-methodology
  - https://www.istqb.org/certifications/certified-tester-foundation-level
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Isolating environment, data and configuration differences

**Goal:** turn "it works in staging but not in UAT" or "works on my machine" into the one difference that matters.

## Systematic diff checklist
1. **Build versions** of every component (version endpoints, image digests: `kubectl get pods -o jsonpath='{..image}'`). Same tag can hide different digests.
2. **Configuration:** env vars, config files, secrets references. Dump and diff (`kubectl get configmap app -o yaml` from both, `diff <(sort a.env) <(sort b.env)`).
3. **Feature flags** and remote config per environment, per user segment.
4. **Data:** the record involved (status, nulls, legacy formats, size), reference data tables, user role and permissions, locale and timezone of the account.
5. **Infrastructure:** DB engine version, OS, CPU architecture, memory limits, number of replicas (concurrency only shows with >1), caches and CDN, proxies/WAF rules.
6. **Integrations:** sandbox vs real third party, stub vs live, network policies, certificates.
7. **Client:** browser and version, extensions, device, OS, screen size, cache/cookies (try a clean profile), network (VPN, corporate proxy).
8. **Time:** cron jobs, time-dependent logic, clock skew between servers.

## Method
- Write down every known difference, then change one at a time toward the failing side (or binary search: copy half the config) until it reproduces.
- Move the failing data into the working environment (masked) to separate data from environment.
- Record each experiment and result in the bug.

## Verify
The bug report states the isolated difference with the experiment that showed it (reproduces when changed, disappears when reverted).
