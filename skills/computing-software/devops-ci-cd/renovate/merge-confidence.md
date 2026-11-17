---
id: computing-software.devops-ci-cd.renovate.merge-confidence
name: merge-confidence
category: computing-software
field: devops-ci-cd
product: renovate
tags: [merge-confidence, confidence-badges, breaking-releases, renovate]
level: practitioner
status: docs-checked
description: "Use Merge Confidence badges and rules to spot undeclared breaking releases, and configure its endpoint when self-hosting."
sources:
  - https://docs.renovatebot.com/merge-confidence/
  - https://docs.renovatebot.com/self-hosted-configuration/#mergeconfidenceendpoint
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Merge Confidence flags undeclared breaking releases using test and release adoption data collected from Mend Renovate App users. It adds four badges to a PR:

- Age: how old the release is.
- Adoption: the percentage of Renovate users of this package already on this release.
- Passing: the percentage of updates for this package whose tests pass.
- Confidence: the overall level for the update.

Badges are available on any supported platform or Renovate distribution. Supported languages and datasources: Go (`go`), JavaScript (`npm`), Java (`maven`), Python (`pypi`), .NET (`nuget`), PHP (`packagist`) and Ruby (`rubygems`).

Levels: Low (probably breaking, often just a `major` update), Neutral (not enough data), High (age, adoption and passing tests mean a very low chance of breaking changes) and Very High (months old with high adoption or very high passing). npm packages can only get High once at least three days old, because they can be unpublished before then. Adoption and Passing percentages are weighted towards organizations, private repositories and reliable tests, so they are not raw percentages. The algorithm is private.

The Mend Renovate App enables badges automatically. When self-hosting, add the `mergeConfidence:all-badges` preset to `extends`; `mergeConfidence:age-confidence-badges` shows only Age and Confidence. In the Mend Renovate App, disable by adding `mergeConfidence:all-badges` to `ignorePresets`.

Rules such as "only raise a PR once the update is High" or "automerge Very High" come from Merge Confidence Workflows, available to paying Mend customers and to open source projects on Mend Renovate Community Cloud.

Self-hosted global config: `mergeConfidenceEndpoint` (default `https://developer.mend.io/`) and `mergeConfidenceDatasources` (limit which datasources are queried) both apply only if you hold an access token for Mend's Merge Confidence API; the endpoint feature is documented as private beta.

## Checked

2026-11-08: read the whole Merge Confidence page (raw source of docs.renovatebot.com/merge-confidence) plus the `mergeConfidenceDatasources` and `mergeConfidenceEndpoint` sections of the self-hosted configuration page (partial read of that page). Confirmed the four badges, the seven supported datasources (added Ruby `rubygems`, which the draft omitted), the confidence levels, the three-day npm rule, the presets and the Workflows availability. Removed the `matchConfidence` automerge example and the Mend API key claim for it, which neither read page supports on the rule side.
Method: documentation only; no commands were run.
