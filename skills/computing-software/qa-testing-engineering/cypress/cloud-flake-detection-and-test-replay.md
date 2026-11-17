---
id: computing-software.qa-testing-engineering.cypress.cloud-flake-detection-and-test-replay
name: cloud-flake-detection-and-test-replay
category: computing-software
field: qa-testing-engineering
product: cypress
tags: [test-replay, cypress-cloud, flake-detection, flaky-tests, cypress-retries]
level: practitioner
status: docs-checked
description: "Use Cypress Cloud to detect and debug flaky tests: test retries config, flaky test analytics, Test Replay of DOM, network and console, and branch-level flake alerts."
sources:
  - https://docs.cypress.io/cloud/features/flaky-test-management
  - https://docs.cypress.io/cloud/features/test-replay
  - https://docs.cypress.io/app/guides/test-retries
  - https://docs.cypress.io/app/references/experiments
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud flake detection and Test Replay (Cypress)

## Enable retries (the flake signal)
```js
// cypress.config.js
module.exports = defineConfig({ retries: { runMode: 2, openMode: 0 } });
// or per test: it('x', { retries: 3 }, () => {...})
```
Experimental retry strategies (config options added in 13.4.0): `detect-flake-and-pass-on-threshold` and `detect-flake-but-always-fail`, set with `retries.experimentalStrategy` and `retries.experimentalOptions` (`maxRetries`, `passesRequired`, `stopIfAnyPassed`); `passesRequired` cannot be greater than `maxRetries`, and `openMode` and `runMode` must then be set explicitly to true or false:
```js
retries: {
  experimentalStrategy: 'detect-flake-and-pass-on-threshold',
  experimentalOptions: { maxRetries: 5, passesRequired: 2 },
  openMode: false,
  runMode: true,
}
```
By default retries stop at the first passing attempt and the final result of a flaky test is passing; Cloud flags a test that failed then passed as flaky.

## Record to Cloud
```bash
npx cypress run --record --key $CYPRESS_RECORD_KEY --parallel --ci-build-id $GITHUB_RUN_ID
```
- **Flaky test management**: scores flaky tests by severity, tracks flake rate over time, distinguishes failure rate from flake rate, and compares flake across branches with Branch Review.
- Flake alerting (an organisation-plan feature) can notify through GitHub, GitLab, Bitbucket, Slack and Microsoft Teams; check the Cloud docs for the plan that includes it.

## Test Replay
Opens a recorded run in Cypress Cloud with the DOM, network requests, console events and the application under test inspectable as in the browser, for each attempt. Compare the failed attempt with the passing retry to see what differed (e.g. request order, a slow API, an animation). Test Replay needs runs recorded in a Chromium-based browser (Chrome, Edge, or the deprecated Electron browser); WebKit and Firefox runs are listed as not supported.

## Debug workflow for a flaky test
1. Open the flaky test in Cloud; check flake rate and when it started (correlate with commits).
2. Test Replay the failed attempt: find the first divergence (network timing, element state).
3. Fix the root cause (wait on an alias, control data, remove conditional logic); keep retries as a safety net, not the fix.
4. Watch the flake rate in Cloud over following runs.

## Without Cloud
Retries still work locally; Cloud flake analytics, alerting and Test Replay need recorded runs.

## Gotchas
- High retries hide flakiness that users experience as product bugs.
- Check the Test Replay page for what is and is not captured and for network data redaction and form input masking.

## Verify
Retries are enabled in run mode, flaky tests are visible in a report with owners, and fixed tests stop appearing as flaky.

## Checked
Checked against the Cypress documentation sources (cypress-io/cypress-documentation, docs/, last commit 2026-10-24, which document Cypress 16; latest release v16.2.0). Confirmed: `retries` with `runMode`/`openMode`, per-test `{ retries: 3 }`, experimental strategies, options and constraints and the 13.4.0 introduction, default retry behaviour, Flake Detection, severity, failure versus flake rate, Branch Review, alert integrations, Test Replay contents and browser support. `--record --key --parallel --ci-build-id` usage matches the parallelization guide.

Method: documentation only; no commands were run.
