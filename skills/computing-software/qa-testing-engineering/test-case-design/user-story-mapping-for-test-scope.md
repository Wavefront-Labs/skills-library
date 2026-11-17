---
id: computing-software.qa-testing-engineering.test-case-design.user-story-mapping-for-test-scope
name: user-story-mapping-for-test-scope
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [user-story-mapping, test-scope, agile-testing, release-planning, risk-based-testing]
level: practitioner
status: gated
description: "Use user story maps to scope testing: backbone activities, walking skeleton, release slices, end-to-end journeys and gaps visible across stories."
sources:
  - https://jpattonassociates.com/story-mapping/
  - https://www.istqb.org/certifications/certified-tester-foundation-level
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# User story mapping for test scope

**Goal:** see testing scope across the whole user journey rather than story by story. Story mapping per Jeff Patton.

## Map structure (gated: unconfirmed, source is paywalled or blocked)
- **Backbone:** user activities left to right in journey order (Discover -> Choose -> Buy -> Receive -> Get help).
- **Walking skeleton:** the thinnest set of stories that delivers the journey end to end.
- **Ribs:** stories below each activity, prioritised top-down, sliced horizontally into releases.

## Using it for testing
1. **End-to-end journeys:** each release slice defines a journey through the backbone; write one E2E/acceptance scenario per slice, independent of how stories were split.
2. **Integration seams:** stories in adjacent activities often belong to different teams; mark the seams and plan integration tests there.
3. **Gaps:** empty cells under an activity in a release reveal missing behaviour (e.g. no "get help" story -> no error recovery path).
4. **Risk overlay:** colour stories by risk (money, data, compliance, novelty); depth of testing follows colour.
5. **Test status overlay:** sticky dots for tested / automated / defects open give a release-level view.
6. **Non-functional stories:** place performance, accessibility and security under the activities they affect.

## Workshop tips
Include a tester in mapping sessions; ask per activity "how would we know this works?", "what can go wrong here?", "what data do we need?". Capture answers as acceptance criteria or test charters.

## Gotchas
- Story-level acceptance tests all pass while the journey breaks at seams; the map makes journeys explicit.
- Maps go stale; update after each release planning.

## Verify
Each release slice has at least one end-to-end journey test, seams between teams have integration tests, and risk colours drive the test plan.

## Checked

2026-10-28. Confirmed: Patton story-mapping page (a landing page only). Gated: backbone, walking skeleton and ribs terminology, which is in the paywalled book. Removed: Nothing removed.

Method: documentation only; no commands were run.
