---
id: computing-software.cloud-infrastructure-engineering.kubernetes.service-no-endpoints-troubleshooting
name: service-no-endpoints-troubleshooting
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, services, service-troubleshooting, no-endpoints, targetport, selector-mismatch, cka, ckad]
level: practitioner
status: docs-checked
description: "Fix Services that don't route: empty endpoints from selector/label mismatches or unready pods, and port/targetPort/named-port mistakes, checked step by step with kubectl."
sources: ["https://kubernetes.io/docs/tasks/debug/debug-application/debug-service/", "https://kubernetes.io/docs/concepts/services-networking/service/#defining-a-service"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Service with no endpoints / wrong ports

## Step 1: does it have endpoints?
```bash
kubectl get svc web -o wide                         # SELECTOR column
kubectl get endpointslices -l kubernetes.io/service-name=web -o wide
```

## Step 2: empty -> selector vs labels
```bash
kubectl get pods -l app=web -n <ns>                 # use the Service's exact selector
kubectl get pods --show-labels -n <ns>
```
| Finding | Fix |
|---|---|
| no pods match | typo, wrong key (`app` vs `app.kubernetes.io/name`), Service in another namespace than the pods |
| pods match but not Ready | readiness probe failing; fix the probe or the app |
| pods match, Ready, still empty | check the Service is not `ExternalName` or selector-less (then you manage the EndpointSlices yourself) |
| matches too many pods | selector too broad (pulls in canary or debug pods) |

## Step 3: endpoints exist but connections fail -> ports
```yaml
spec:
  ports:
  - name: http
    port: 80            # what clients use: web:80
    targetPort: http    # container port NAME or number on the pod
    protocol: TCP
```
- Is the `targetPort` correct for your Pods (some Pods use a different port than the Service)?
- If you meant a named port, do your Pods expose a port with the same name?
- Multi-port Services require a `name` on every port.
- If the application listens only on the loopback address inside the container, it cannot be
  reached through the Pod IP; it must listen on a non-loopback address.
```bash
kubectl get endpointslices -l kubernetes.io/service-name=web -o jsonpath='{.items[*].ports}'
```
To test, connect to the Pod IP and port directly, then through the Service name, from a throwaway
Pod. Pod IP works but Service does not: look at kube-proxy, the datapath or NetworkPolicy.
Neither works: look at the application.

## Verify
- [ ] The EndpointSlices list all Ready pods with the right port, and a request through the Service name succeeds.

## Checked

2026-10-23, Kubernetes documentation (kubernetes/website main, v1.36 docs) and kubernetes/kubernetes source. Confirmed against the Debug Services task page: check the targetPort, check that Pods expose a port with the same name when a named port is used, and test Pod IP vs Service. Removed unconfirmed detail: describe-output text, the claim that pods without the named port are dropped from slices, the defaulting rule for targetPort, and the busybox/ss commands.

Method: documentation only; no commands were run.
