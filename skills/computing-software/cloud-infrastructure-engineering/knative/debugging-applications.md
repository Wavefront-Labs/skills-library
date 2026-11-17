---
id: computing-software.cloud-infrastructure-engineering.knative.debugging-applications
name: debugging-applications
category: computing-software
field: cloud-infrastructure-engineering
product: knative
tags: [debugging, route-status, revision-status, pod-status, troubleshooting, kingress-debug]
level: practitioner
status: docs-checked
description: "Walk the object chain from deploy output to Route, Revision, Pod and ingress to find why a Service fails."
sources:
  - https://knative.dev/docs/serving/troubleshooting/debugging-application-issues/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: locate where a deployed Knative application breaks.

Work down the chain:

1. Terminal output. A failed apply usually means a bad manifest or command. Example: an admission webhook message that the route must have traffic percent summing to 100.

2. Route status:

```bash
kubectl get route <route-name> --output yaml
```

The `conditions` in `status` give the reason for a failure; the Knative Error Conditions and Reporting page explains them.

3. Ingress and Istio routing: list `ingresses.networking.internal.knative.dev` with custom columns for name and labels, then get the Ingress YAML. With Istio, query the VirtualService by label `networking.internal.knative.dev/ingress=<INGRESS_NAME>` in the ingress namespace.

4. Ingress status: check the gateway Service, for example `kubectl get svc -n istio-system istio-ingressgateway`.

5. Revision status. Find the Revision from a Configuration:

```bash
kubectl get configuration <configuration-name> --output jsonpath="{.status.latestCreatedRevisionName}"
kubectl get revision <revision-name> --output yaml
```

A ready Revision has `reason: ServiceReady`, `status: "True"`, `type: Ready`.

6. Pod status: `kubectl get pods`, then `kubectl get pod <pod-name> --output yaml` and read `conditions` and `containerStatuses`. A pod showing `1/2 CrashLoopBackOff` means one of its two containers is failing.

## Checked

2026-11-04. Confirmed against the Debugging application issues page (page text of knative.dev): terminal-output example about route traffic percent summing to 100, `kubectl get route` conditions, the Ingress listing with custom columns and the VirtualService label query, the `istio-ingressgateway` Service check, the Configuration `latestCreatedRevisionName` jsonpath, the ready Revision condition (`ServiceReady`, `"True"`, `Ready`) and the pod `conditions` and `containerStatuses` fields. Corrected the name of the page that explains error conditions to Knative Error Conditions and Reporting.

Method: documentation only; no commands were run.
