---
id: computing-software.devops-ci-cd.ci-pipeline-design.snapshot-and-golden-file-tests
name: snapshot-and-golden-file-tests
category: computing-software
field: devops-ci-cd
product: ci-pipeline-design
tags: [ci-pipeline-design, snapshot-testing, golden-files, test-automation]
level: practitioner
status: docs-checked
description: "Use Jest snapshot and Go golden-file tests in CI without them rotting: deterministic output, explicit update flags and reviewed snapshot diffs."
sources: ["https://jestjs.io/docs/snapshot-testing", "https://jestjs.io/docs/cli", "https://pkg.go.dev/gotest.tools/v3/golden"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Snapshot and golden-file tests

Compare output (rendered UI, CLI output, logs, API responses, error messages) to a committed expected file.

## Jest
- `expect(value).toMatchSnapshot()` writes a `.snap` file on first run and compares on later runs; `toMatchInlineSnapshot()` writes the value into the test source instead (Jest delegates the writing to prettier if the project uses it). Snapshots can capture any serializable value, not only React components.
- Update intentionally changed snapshots with `jest --updateSnapshot` (alias `-u`); add `--testNamePattern` to limit which are re-recorded. Fix real bugs first, or you record the buggy behaviour.
- Generated fields (ids, dates) fail every run. Use property matchers: `expect(user).toMatchSnapshot({ createdAt: expect.any(Date), id: expect.any(Number) })`; the snapshot stores `Any<Date>`. For strings, replace the random part yourself, or use a serializer or mock the generator.
- Freeze time: `Date.now = jest.fn(() => 1_482_363_367_071)`.

## Go golden files
`gotest.tools/v3/golden`: golden files live in the package's `./testdata/` directory. `golden.Assert(t, actual, "name.golden")` (strings) and `golden.AssertBytes` compare to the file; `go test pkgname -update` rewrites the files, so compare the old and new diff to confirm the update is right. `golden.String` and `golden.Bytes` return comparisons for use with `assert.Assert`. `golden.FlagUpdate()` reports whether `-update` is set.
`\r\n` in actual strings is normalised to `\n` (set `GOTESTTOOLS_GOLDEN_NormalizeCRLFToLF=false` to turn off, needed with `core.autocrlf=true` on Windows). The golden files themselves can still contain CRLF on Windows checkouts; `* text=auto eol=lf` in `.gitattributes` avoids that.

## CI rules
- CI never records new snapshots: with `jest --ci` a new snapshot fails the test and requires `--updateSnapshot`. Jest also does not write snapshots on a CI system unless `--updateSnapshot` is passed. Do not pass `-u` in the CI pipeline.
- Determinism: the snapshot must not contain platform-specific or other non-deterministic data; same test, unchanged code, same result every run.

## Review discipline
- Commit snapshots and review them in code review as you would any test. Keep them focused and short (`eslint-plugin-jest` `no-large-snapshots`, `snapshot-diff` can help) and give tests descriptive names so reviewers can tell the expected content.
- Do not regenerate snapshots just to turn the suite green; examine the cause of the failure.
- Merge conflicts in snapshot files: resolve manually or rerun Jest to regenerate and inspect.
- Snapshot testing (serialised text diff) is not visual regression testing (pixel comparison of screenshots) and does not replace unit tests.

## Verify
- [ ] Changing output without updating snapshots fails CI with a readable diff.
- [ ] The CI command contains no `-u` / `--updateSnapshot` / `-update`.

## Checked
Method: docs-checked 2026-11-09 against the Jest snapshot testing page (full), the Jest CLI page (`--ci`, `--updateSnapshot`) and the gotest.tools golden package page (full).
Removed as unconfirmed: the syrupy, pytest-snapshot, insta, Verify and Vitest rows and their update commands (`INSTA_UPDATE=no`, `cargo insta`, `--unreferenced=reject`, `.received` files), the hand-rolled Go `-update` flag snippet, the claim that `jest --ci --detectOpenHandles` reports obsolete snapshots (the pages do not say it), obsolete-snapshot failure flags generally, and the `*.snap text eol=lf` gitattributes line (the golden docs show `* text=auto eol=lf`). Sorting maps and seeding randomness were dropped as not in the sources.
