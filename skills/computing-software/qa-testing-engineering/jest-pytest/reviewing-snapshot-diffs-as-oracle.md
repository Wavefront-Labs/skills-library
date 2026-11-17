---
id: computing-software.qa-testing-engineering.jest-pytest.reviewing-snapshot-diffs-as-oracle
name: reviewing-snapshot-diffs-as-oracle
category: computing-software
field: qa-testing-engineering
product: jest-pytest
tags: [snapshot-review, snapshot-testing, test-oracles, jest-snapshots, syrupy]
level: practitioner
status: verified
description: "Treat snapshot tests as a reviewed oracle: keep snapshots small and stable, review diffs in PRs, and update deliberately with Jest, syrupy and Playwright."
sources:
  - https://jestjs.io/docs/snapshot-testing
  - https://github.com/syrupy-project/syrupy
  - https://playwright.dev/docs/test-snapshots
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reviewing snapshot diffs as an oracle

**Goal:** a snapshot is an expected result recorded from the system; it is only an oracle once a human has reviewed it.

## Tools
- Jest: `expect(tree).toMatchSnapshot()`, `toMatchInlineSnapshot()` (stored in the test file, easier to review). Update with `jest -u`. In CI use `--ci`, which fails instead of writing new snapshots (`New snapshot was not written`; run).
- pytest: syrupy, `assert result == snapshot`; update with `pytest --snapshot-update` (new snapshots also need this flag: without it a missing snapshot fails); unused snapshots fail the run (`1 snapshot unused`) until `--snapshot-update` deletes them, or use `--snapshot-warn-unused`. Do not install `pytest-snapshot` alongside syrupy: both define `--snapshot-update` and pytest crashes at startup.
- Playwright: `expect(page).toHaveScreenshot()` and ARIA snapshots `toMatchAriaSnapshot()`; update with `npx playwright test --update-snapshots`.

## Keep snapshots reviewable
- Small and focused: snapshot a serialised API response body or a component's key output, not a whole page's DOM.
- Deterministic: scrub or freeze timestamps, IDs, random values (Jest property matchers `expect.any(String)`, syrupy matchers/exclude).
- Stable ordering: sort collections before snapshotting.
- Named: one assertion per snapshot with a descriptive name.

## Review discipline
1. Snapshot changes appear in the PR diff; reviewers read them like code.
2. Ask for each diff: is this change intended by this PR? If unrelated snapshots change, investigate.
3. Never run `-u` on the whole suite to "fix CI"; update only the tests the change explains (`jest -u -t "invoice header"`). Note that `-u` also removes obsolete snapshots in the files it runs, even with `-t` (observed), so review that diff too.
4. Commit message notes why snapshots changed.

## Gotchas
- Huge snapshots get rubber-stamped; break them up or replace with explicit assertions on the fields that matter.
- Obsolete snapshot files accumulate; Jest prints an obsolete-snapshot summary after each run (`1 snapshot obsolete`); remove them deliberately (`jest -u` on a clean tree) and review that diff too.
- Screenshots differ by OS/fonts; generate them in the same container as CI.

## Verify
CI runs in `--ci` mode, snapshot diffs are visible in PRs, and sampled updates carry a justification.
