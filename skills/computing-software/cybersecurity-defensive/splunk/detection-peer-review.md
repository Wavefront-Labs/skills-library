---
id: computing-software.cybersecurity-defensive.splunk.detection-peer-review
name: detection-peer-review
category: computing-software
field: cybersecurity-defensive
product: splunk
tags: [detection-peer-review, detection-as-code, code-review, pull-requests, detection-engineering, codeowners]
level: practitioner
status: draft
description: "Peer review detection pull requests: review checklist for logic, performance, false positives, test evidence, metadata and deployment risk, with PR templates and CODEOWNERS."
sources: ["https://github.com/palantir/alerting-detection-strategy-framework", "https://www.splunk.com/en_us/blog/security/detection-as-code.html", "https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Peer review of detection pull requests

## Mechanics
- CODEOWNERS: `/detections/ @org/detection-reviewers`; branch protection requires one approval
  and passing CI (lint, schema, conversion, unit tests).
- PR template forces evidence:
```
## What and why (threat, ATT&CK ID, source report)
## Test evidence (positive sample hit, query output link)
## Backtest (30-day hit count, sample of hits reviewed)
## Expected volume and triage time
## Rollout (experimental -> production date)
```

## Reviewer checklist
1. **Logic**: does it catch the behaviour, not one tool's artefact? Are evasion variants
   (renamed binary, case, quoting, path variants) covered or documented as gaps?
2. **Data**: fields exist in this environment's mappings; index/sourcetype macros used; no
   dependence on fields that are often null.
3. **False positives**: backtest results reviewed; allowlists narrow (path + signer, not
   process name alone); exclusions do not create blind spots attackers can mimic.
4. **Performance**: time range and frequency sane; uses accelerated data/`tstats` where possible;
   no unbounded subsearches/joins; estimated cost acceptable.
5. **Metadata**: severity/risk justified, triage notes actionable, owner set, references.
6. **Tests**: positive and negative samples committed; unit test passes.
7. **Deployment risk**: will it flood the queue? Start as experimental/alert-to-dashboard.

## Practice
- Reviewer runs the query themselves; screenshots are not evidence.
- Comments ask questions about threat coverage, not style preferences that linting handles.
- Merge only with author present to watch first production results.

## Verify
Sample monthly: production detections have an approved PR with evidence attached; review
lead time and post-deploy false-positive rate trend down.
