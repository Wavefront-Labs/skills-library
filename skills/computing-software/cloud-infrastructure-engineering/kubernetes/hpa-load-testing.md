---
id: computing-software.cloud-infrastructure-engineering.kubernetes.hpa-load-testing
name: hpa-load-testing
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, hpa, hpa-load-test, autoscaling, k6, load-testing]
level: practitioner
status: docs-checked
description: "Load-test a workload to verify HPA reaction time, scale limits and scale-down behaviour, and catch requests, metrics or node capacity problems before production traffic does."
sources: ["https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale-walkthrough/", "https://kubernetes.io/docs/concepts/workloads/autoscaling/horizontal-pod-autoscale/#configurable-scaling-behavior", "https://grafana.com/docs/k6/latest/using-k6/k6-options/reference/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Load-testing HPA behaviour

## Quick generator (adapted from the docs walkthrough)
```bash
kubectl run load-generator --image=busybox:1.28 --restart=Never -- /bin/sh -c \
  "while sleep 0.01; do wget -q -O- http://web.default.svc; done"
```

## Realistic ramp with k6
```javascript
// ramp.js
import http from 'k6/http';
export const options = { stages: [
  { duration: '2m', target: 50 }, { duration: '10m', target: 300 }, { duration: '5m', target: 0 } ] };
export default function () { http.get('http://web.default.svc/api'); }
```
```bash
kubectl create configmap k6 --from-file=ramp.js
kubectl run k6 --image=grafana/k6 --restart=Never --overrides='{"spec":{"containers":[{"name":"k6","image":"grafana/k6","args":["run","/s/ramp.js"],"volumeMounts":[{"name":"s","mountPath":"/s"}]}],"volumes":[{"name":"s","configMap":{"name":"k6"}}]}}'
```
Run the generator from a separate node pool so it does not steal CPU from the target.

## Watch
```bash
kubectl get hpa web -w
kubectl describe hpa web | sed -n '/Conditions/,$p'
kubectl get events --field-selector involvedObject.kind=HorizontalPodAutoscaler -w
```

## What to record
- Time from load increase to new pods Ready (HPA sync period, 15 s by default, plus metrics
  pipeline lag, image pull and readiness).
- Whether `maxReplicas` or node capacity is hit (`ScalingLimited`, pending pods).
- Latency and errors during scale-up; if they spike, lower the target utilization or add
  `behavior.scaleUp` policies allowing bigger steps.
- Scale-down after load stops (default 300 s stabilization) without flapping.

## Common findings
Missing CPU requests (`<unknown>` targets), readiness probes that pass before warm-up,
cluster autoscaler adding nodes too slowly (add overprovisioning).

## Checked

Checked 2026-10-24 against Kubernetes v1.37 documentation (kubernetes/website main, the latest published release on 2026-10-24), the HPA walkthrough and the k6 docs.
- Load-generator loop and image taken from the walkthrough (busybox:1.28, `while sleep 0.01; do wget -q -O- ...`).
- Sync period 15 s and scale-down stabilization window 300 s confirmed in the HPA page (default `behavior` block).
- k6 `stages` option (list of duration and target) confirmed in the k6 options reference; `grafana/k6` image is the one the k6 install docs pull and run with `run`.

Method: documentation only; no commands were run.
