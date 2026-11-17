---
id: computing-software.qa-testing-engineering.jmeter-k6.grafana-cloud-k6-distributed-runs
name: grafana-cloud-k6-distributed-runs
category: computing-software
field: qa-testing-engineering
product: jmeter-k6
tags: [k6, k6-cloud, grafana-cloud-k6, distributed-load-testing, load-zones, k6-operator, k6-outputs]
level: practitioner
status: gated
description: "Run k6 at scale: Grafana Cloud k6 (k6 cloud run, load zones, cloud options) or the self-hosted k6-operator on Kubernetes with parallelism and segments."
sources:
  - https://grafana.com/docs/k6/latest/reference/cloud-commands/
  - https://grafana.com/docs/k6/latest/get-started/migrating-to-v2/
  - https://grafana.com/docs/k6/latest/testing-guides/running-distributed-tests/
  - https://grafana.com/docs/k6/latest/using-k6/k6-options/reference/
  - https://grafana.com/docs/k6/latest/set-up/set-up-distributed-k6/usage/k6-operator-to-gck6/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Distributed k6: Grafana Cloud k6 and k6-operator

**Goal:** generate more load than one machine can, from multiple regions if needed.

## Grafana Cloud k6
```bash
k6 cloud login --token $K6_CLOUD_TOKEN --stack <stack-url-or-slug>
k6 cloud run script.js                       # executes on Grafana Cloud infrastructure
k6 cloud run --local-execution script.js     # runs locally, streams results to the cloud
```
In k6 v2 a stack is required for every `k6 cloud` command (token and stack can also come from `K6_CLOUD_TOKEN` and `K6_CLOUD_STACK_ID`), `k6 cloud script.js` and `k6 login cloud` were removed, and `options.ext.loadimpact` was replaced by `options.cloud`:
```js
export const options = {
  cloud: { name: 'checkout peak' },
}
```
Choosing load zones and their traffic split in `options.cloud` (for example a `distribution` block with `loadZone` and `percent`) (gated: unconfirmed, source is paywalled or blocked). The Grafana Cloud k6 reference pages are not in a public repository; list available zones with `k6 cloud load-zone list` and check the Grafana Cloud k6 documentation. Private load zones also exist (the k6 Operator docs link to them).

## k6-operator (self-hosted Kubernetes)
```yaml
apiVersion: k6.io/v1alpha1
kind: TestRun
metadata: { name: checkout-peak }
spec:
  parallelism: 8                      # runner pods, each gets an equal execution segment
  script: { configMap: { name: checkout-script, file: script.js } }
  arguments: --tag testid=checkout-peak --out experimental-prometheus-rw
  runner: { resources: { limits: { cpu: "2", memory: 4Gi } } }
```
`kubectl create configmap checkout-script --from-file=script.js && kubectl apply -f testrun.yaml`.

## Manual segments
Run the same script on each machine with its own segment and the shared sequence, for example machine 1 `k6 run --execution-segment "0:1/4" --execution-segment-sequence "0,1/4,1/2,3/4,1" script.js`, machine 2 `--execution-segment "1/4:1/2"` and so on; send results to a shared output.

## Gotchas
- Open-source segment-based distribution has no built-in metric aggregation (listed as a missing part in k6's distributed-execution design doc), so thresholds and the end-of-test summary come from each instance; compute final pass/fail from the aggregated output.
- Cloud runs consume VU hours (the k6 docs say `--local-execution` streaming also consumes VUH or test runs); validate with a small smoke run first.
- `SharedArray` memory is shared between the VUs of one k6 process, not between machines; partition unique data by segment or instance.
- In k6 v2, aborted cloud runs not caused by thresholds exit with 97 (threshold aborts exit with 99).

## Verify
Aggregated RPS equals the target, and per-pod/zone metrics are evenly distributed.

## Checked
Checked against the Grafana k6 docs sources (grafana/k6-docs, docs/sources/k6/next, last commit 2026-10-13, which document k6 v2) and the k6 Operator repository (grafana/k6-operator, last commit 2026-10-21). Confirmed: `k6 cloud login --token/--stack`, `k6 cloud run` and `--local-execution`, stack requirement and removed commands in k6 v2, `options.cloud`, `k6 cloud load-zone list`, TestRun `parallelism`/`arguments`/runner fields, execution segment options and sequence example, VUH consumption, exit codes 97 and 99. Gated: the cloud `distribution`/`loadZone` option block, whose reference lives in the non-public Grafana Cloud docs.

Method: documentation only; no commands were run.
