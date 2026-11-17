---
id: computing-software.devops-ci-cd.release-engineering.testing-both-flag-paths-in-ci
name: testing-both-flag-paths-in-ci
category: computing-software
field: devops-ci-cd
product: release-engineering
tags: [release-engineering, flag-testing, feature-flags, test-automation]
level: practitioner
status: draft
description: "Test feature-flagged code without exploding test matrices: in-memory flag providers, testing on/off paths, release-configuration test runs and avoiding live flag services in CI."
sources: ["https://openfeature.dev/docs/reference/concepts/provider", "https://martinfowler.com/articles/feature-toggles.html#TestingFeatureToggledSoftware"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Testing both flag paths in CI

## Principles
- Unit tests set flags explicitly through an in-memory/test provider; never call the live flag
  service from CI (flaky, and someone toggling prod changes test results).
- Test both branches of each **active** flag where logic differs.
- Do not test all combinations of N flags; test the configurations you will actually ship.

## In-memory provider (OpenFeature)
```ts
import { InMemoryProvider, OpenFeature } from '@openfeature/server-sdk';
beforeEach(async () => {
  await OpenFeature.setProviderAndWait(new InMemoryProvider({
    'new-checkout': { variants: { on: true, off: false }, defaultVariant: 'off', disabled: false },
  }));
});
test.each([['on', 72], ['off', 80]])('price with new-checkout %s', async (variant, expected) => {
  // switch variant for this test
  ...
});
```
Without OpenFeature, wrap your flag client behind an interface and inject a fake.

## Pipeline configurations
- Run the acceptance suite with **current production flag values** (export from the flag service
  as a JSON snapshot at pipeline start) and again with **all release-candidate flags on** (the next state).
- Fail if a flag referenced in code does not exist in the flag service (typo, deleted flag).

## Cleanup
When a flag is removed, delete the off-path tests in the same PR; dead branches keep tests alive and
hide coverage drops.

## Verify
- [ ] CI runs with no network access to the flag service; both variants of active flags are exercised.
