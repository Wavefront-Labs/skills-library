---
id: computing-software.cloud-infrastructure-engineering.kubernetes.static-pod-url-manifest-source
name: static-pod-url-manifest-source
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, static-pods, staticpodurl, kubelet-configuration, kubelet]
level: practitioner
status: docs-checked
description: "Have the kubelet read static pod manifests from an HTTP URL with staticPodURL, and know the polling, header and security trade-offs versus a manifest directory."
sources: ["https://kubernetes.io/docs/tasks/configure-pod-container/static-pod/#pods-created-via-http", "https://kubernetes.io/docs/reference/config-api/kubelet-config.v1beta1/", "https://github.com/kubernetes/kubernetes/blob/master/pkg/kubelet/config/http.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# staticPodURL

```yaml
# /var/lib/kubelet/config.yaml
staticPodURL: https://config.example.internal/nodes/<node>/pods.yaml
staticPodURLHeader:
  Authorization: ["Bearer <token>"]
httpCheckFrequency: 20s        # default
```
`staticPodURLHeader` is a map of header name to a list of values. The kubelet downloads the URL
every `httpCheckFrequency` (default 20s; the `--manifest-url` flag is the older equivalent). The
body is one Pod manifest or a list of Pods (YAML or JSON, per the kubelet source). Pods appear as
mirror pods named `<pod>-<nodename>` like file-based static pods, and the kubelet applies changes
to the list of static pods when it refetches.

## When it fits
- Fleets of edge nodes managed from a central config service, without a full GitOps agent.
- Boot-time pods needed before the node can reach the API.

## Risks
- Whoever controls the URL runs root-capable pods on every node that points at it.
  Use HTTPS and authentication (`staticPodURLHeader`).
- Check the kubelet logs for fetch errors (`journalctl -u kubelet | grep -i http`).

## Verify
```bash
kubectl get pods -A --field-selector spec.nodeName=<node>
journalctl -u kubelet --since -5m | grep -i 'static pod\|http'
```

## Checked

Checked 2026-10-26 against Kubernetes documentation v1.37 (kubernetes/website commit 2026-10-25) and kubernetes/kubernetes master (kubelet source, 2026-10-24). Confirmed: `staticPodURL`, `staticPodURLHeader` (a map of string to list of strings), `httpCheckFrequency` default `20s` (kubelet config types), the periodic refetch and application of changes, the single-Pod-or-list body (source `http.go`), mirror pod naming. Removed as unconfirmed: the claim that the kubelet keeps the last known pods when the URL is unreachable, the combined `staticPodPath` note, and the "pinned CA" advice.

Method: documentation only; no commands were run.
