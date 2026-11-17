---
id: computing-software.qa-testing-engineering.jmeter-k6.k6-operator-kubernetes
name: k6-operator-kubernetes
category: computing-software
field: qa-testing-engineering
product: jmeter-k6
tags: [k6-operator-testrun, k6-operator, distributed-load-kubernetes, testrun-crd]
level: practitioner
status: docs-checked
description: "Run distributed k6 tests on Kubernetes with the k6 Operator: TestRun CRD, parallelism, script ConfigMaps, separate runners, env and secrets, and result aggregation."
sources:
  - https://grafana.com/docs/k6/latest/set-up/set-up-distributed-k6/
  - https://grafana.com/docs/k6/latest/set-up/set-up-distributed-k6/install-k6-operator/
  - https://grafana.com/docs/k6/latest/set-up/set-up-distributed-k6/usage/executing-k6-scripts-with-testrun-crd/
  - https://grafana.com/docs/k6/latest/set-up/set-up-distributed-k6/usage/configure-testrun-crd/
  - https://github.com/grafana/k6-operator/blob/main/docs/crd-generated.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# k6 Operator on Kubernetes

## Install
```bash
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
helm install k6-operator grafana/k6-operator
```

## Script and TestRun
```bash
kubectl create configmap checkout-test --from-file=test.js -n load
# a ConfigMap is limited to 1048576 bytes; use volumeClaim or localFile for larger scripts
```
```yaml
apiVersion: k6.io/v1alpha1
kind: TestRun
metadata: { name: checkout, namespace: load }
spec:
  parallelism: 8                       # runner pods; each gets an equal execution segment
  separate: true                       # spread the jobs across different nodes
  cleanup: post                        # remove the TestRun and its resources when the run ends
  script:
    configMap: { name: checkout-test, file: test.js }
  arguments: --out experimental-prometheus-rw --tag testid=checkout-run1
  runner:
    image: <custom runner image>      # default: ghcr.io/grafana/k6-operator:latest-runner
    env:
      - { name: K6_PROMETHEUS_RW_SERVER_URL, value: http://prometheus:9090/api/v1/write }
      - { name: BASE_URL, value: http://checkout.svc.cluster.local }
    envFrom: [{ secretRef: { name: load-secrets } }]
    resources: { requests: { cpu: "2", memory: 2Gi }, limits: { cpu: "2", memory: 2Gi } }
```
`kubectl apply -f testrun.yaml`; watch `kubectl get testrun -n load` and runner pod logs.

## How load splits
Each runner is assigned an equal execution segment, so 200 VUs with `parallelism: 4` become four runners with 50 VUs (an arrival rate divides the same way). Open-source distribution has no built-in metric aggregation, so thresholds and summaries are per runner; send results to a central store (for example Prometheus remote write) or use Grafana Cloud k6 with a token as described in the "k6 Operator with Grafana Cloud k6" guide.

## Multi-file scripts
Create a ConfigMap with several entries (`--from-file` per file or a folder), or archive the script with `k6 archive` and set `file: archive.tar`; or use `script.volumeClaim` (files under `/test/`) or `script.localFile` with a custom image. k6 extensions need your own xk6-built image set as the runner `image`.

## Gotchas
- Set CPU and memory requests and limits on runner pods so generator saturation does not look like system latency.
- Delete finished TestRuns (`kubectl delete -f`) or set `cleanup: post`.
- The initializer job defaults to the runner options; override them with `.spec.initializer` if needed.

## Verify
All runner pods complete; central dashboard shows the total rate equals the script's configured rate.

## Checked
Checked against the Grafana k6 docs sources (grafana/k6-docs, docs/sources/k6/next, last commit 2026-10-13, which document k6 v2) and the k6 Operator repository (grafana/k6-operator, last commit 2026-10-21). Confirmed: Helm repo and install commands, ConfigMap/volumeClaim/localFile script options and the ConfigMap size limit, multi-file and archive usage, `parallelism`, `separate`, `cleanup`, `arguments`, runner `image`/`env`/`envFrom`/`resources` fields in the generated CRD reference, default runner image, equal-segment splitting, Prometheus remote-write output name and `K6_PROMETHEUS_RW_SERVER_URL`. Removed the pinned k6 image tag, unconfirmed namespace flags and NAT claim.

Method: documentation only; no commands were run.
