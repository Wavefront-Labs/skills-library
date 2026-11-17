---
id: computing-software.cloud-infrastructure-engineering.linkerd.debug-sidecar-tshark
name: debug-sidecar-tshark
category: computing-software
field: cloud-infrastructure-engineering
product: linkerd
tags: [linkerd, debug-sidecar, tshark, packet-capture]
level: practitioner
status: docs-checked
description: "Add the Linkerd debug sidecar to a pod to capture traffic with tshark and inspect it via kubectl logs."
sources:
  - https://linkerd.io/2.19/tasks/using-the-debug-container/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
When you need packet-level visibility, Linkerd provides a debug sidecar. Enable it with the annotation `config.linkerd.io/enable-debug-sidecar: "true"` at pod creation time, or use the `--enable-debug-sidecar` option of `linkerd inject`. A pod's container set is immutable, so annotating an existing pod does nothing; the pod must be recreated.

The image contains `tshark`, `tcpdump`, `lsof` and `iproute2`. It starts logging all incoming and outgoing traffic with tshark automatically.

For the emojivoto voting service:

```bash
kubectl -n emojivoto get deploy/voting -o yaml \
  | linkerd inject --enable-debug-sidecar - \
  | kubectl apply -f -
```

Confirm the container is running:

```bash
kubectl get pods -n emojivoto -l app=voting-svc \
  -o jsonpath='{.items[*].spec.containers[*].name}'
```

Watch live capture output:

```bash
kubectl -n emojivoto logs deploy/voting linkerd-debug -f
```

Alternatively use `kubectl exec` into the `linkerd-debug` container and run tcpdump or tshark directly.

## Checked

2026-11-03. Confirmed against: https://linkerd.io/2.19/tasks/using-the-debug-container/.

Removed or reworded: Closing advice not on the page.

Method: documentation only; no commands were run.
