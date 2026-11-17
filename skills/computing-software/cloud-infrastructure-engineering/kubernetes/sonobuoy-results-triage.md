---
id: computing-software.cloud-infrastructure-engineering.kubernetes.sonobuoy-results-triage
name: sonobuoy-results-triage
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, conformance, sonobuoy-results, sonobuoy, e2e-focus]
level: practitioner
status: docs-checked
description: "Retrieve sonobuoy results, find failed conformance tests and their logs, separate environment problems from real failures, and rerun only failures."
sources: ["https://sonobuoy.io/docs/main/results/", "https://sonobuoy.io/docs/main/cli/sonobuoy_results/", "https://sonobuoy.io/docs/main/cli/sonobuoy_run/", "https://sonobuoy.io/docs/main/e2eplugin/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sonobuoy results triage

## Retrieve
```bash
sonobuoy status --json
outfile=$(sonobuoy retrieve)
sonobuoy results $outfile                               # summary per plugin (default report mode)
sonobuoy results $outfile --plugin e2e --mode detailed | jq -r 'select(.status=="failed") | .name'
```
The tarball can be unpacked for raw logs; `sonobuoy results $outfile --mode=dump` prints the canonical
results tree (`plugins/<name>/sonobuoy_results.yaml` inside the tarball).

## Read a failure
```bash
sonobuoy results $outfile --plugin e2e --mode detailed \
  | jq 'select(.status=="failed")' | less      # each item has name, status and a details map
```

## Classify
Group failed test names by SIG tag (for example `[sig-network]`, `[sig-storage]`) and by node to see
whether one component (DNS, CNI, storage class, one node) explains many failures. Sonobuoy's docs do
not map failure patterns to causes, so confirm each cause in the e2e test's own output.
Environment fixes are legitimate; changing the test is not.

## Rerun just the failures
```bash
sonobuoy delete --wait
sonobuoy run --rerun-failed $outfile --wait    # sets E2E_FOCUS to the failed tests in the tarball
```
Or focus manually: `sonobuoy run --e2e-focus '<regex>' --wait` (default focus is `\[Conformance\]`;
`--e2e-focus` and `--mode` should not be combined).

## Certification runs
For submissions you need a clean full `--mode certified-conformance` run with zero failures;
reruns of failures are for debugging only.

## Checked

2026-10-26, against Sonobuoy docs in vmware-tanzu/sonobuoy (site/content/docs/main, CLI reference auto-generated 1-Jul-2026; sonobuoy run default image v0.57.5; repo last pushed 2026-10-14). Confirmed: `sonobuoy results --plugin/--mode` (report, detailed, readable, dump), detailed-mode JSON objects with `status` and `details`, `--rerun-failed`, `--e2e-focus`, `status --json`, `delete --wait`. Removed the unconfirmed failure-pattern table, tarball log paths, `.details.failure` / `system-out` keys and the plugin-status jq filter.

Method: documentation only; no commands were run.
