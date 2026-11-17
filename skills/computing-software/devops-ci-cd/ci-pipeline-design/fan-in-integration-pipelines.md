---
id: computing-software.devops-ci-cd.ci-pipeline-design.fan-in-integration-pipelines
name: fan-in-integration-pipelines
category: computing-software
field: devops-ci-cd
product: ci-pipeline-design
tags: [ci-pipeline-design, fan-in-pipeline, component-pipelines, integration-pipeline]
level: advanced
status: draft
description: "Design fan-in integration pipelines that combine independently built component versions into one tested candidate: triggers, version selection, and avoiding thundering rebuilds."
sources: ["https://www.oreilly.com/library/view/continuous-delivery-reliable/9780321670250/", "https://docs.gitlab.com/ci/pipelines/downstream_pipelines/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Fan-in integration pipelines

Continuous Delivery ch13: each component has its own pipeline producing a versioned artifact; an
**integration pipeline** assembles a set of component versions and runs system/acceptance tests on
the combination.

## Shape
```
svc-a pipeline --> artifact a@1.4.2 --\
svc-b pipeline --> artifact b@2.0.1 ----> integration pipeline: compose manifest -> deploy to test env -> e2e -> publish "release candidate set"
svc-c pipeline --> artifact c@0.9.7 --/
```

## Triggering
- Each component's successful main build triggers integration with its new version and the
  **last known good** versions of the others (from the previous green manifest).
- Debounce: batch triggers within a window (e.g. 10 min) or use a queue with "newest wins", so five
  components finishing together cause one integration run, not five.
  GitHub: `concurrency: integration` with cancel-in-progress; GitLab: `resource_group` + `interruptible`.

## Version selection
```yaml
# manifest.yaml written by the integration pipeline
components:
  svc-a: 1.4.2     # just built
  svc-b: 2.0.1     # last green
  svc-c: 0.9.7
```
Green run => commit manifest as the new candidate (tag `rc-2026.10.18.3`). Red run => identifies the
newly introduced version as suspect; others stay on last green.

## Gotchas
- Integration runs must use the exact artifacts (digests), not rebuild from source.
- Keep component contract tests in component pipelines; fan-in finds what contracts miss, not everything.

## Verify
- [ ] Manifest history shows each green set; a failing component version never enters a candidate.
