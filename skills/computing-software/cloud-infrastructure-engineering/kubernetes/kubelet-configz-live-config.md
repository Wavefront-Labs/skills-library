---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kubelet-configz-live-config
name: kubelet-configz-live-config
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, kubelet-config, kubelet-configz, kubeletconfiguration, kubelet]
level: practitioner
status: docs-checked
description: "Read the kubelet's effective running configuration through the /configz endpoint to confirm flags, config file and drop-ins merged as intended."
sources: ["https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/", "https://kubernetes.io/docs/reference/access-authn-authz/kubelet-authn-authz/", "https://kubernetes.io/docs/reference/node/kubelet-config-directory-merging/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Inspecting live kubelet config with /configz

The kubelet merges defaults, the `--config` file, the drop-in directory (`--config-dir`, which must be
set explicitly) and command-line flags (flags win). `/configz` returns the result actually in use.

## Through the API server
```bash
kubectl get --raw "/api/v1/nodes/<node>/proxy/configz" | jq .kubeletconfig
kubectl get --raw "/api/v1/nodes/<node>/proxy/configz" | jq '.kubeletconfig | {cgroupDriver, maxPods, evictionHard, systemReserved, kubeReserved, serverTLSBootstrap, rotateCertificates}'
```
Needs RBAC on `nodes/proxy`, which is powerful (full kubelet API). With feature gate
`KubeletFineGrainedAuthz` (stable and on by default from 1.36) the kubelet checks the `nodes/configz`
subresource first, so you can grant `configz` alone.

## Via kubectl proxy
```bash
kubectl proxy --port=8001 &
curl -X GET http://127.0.0.1:8001/api/v1/nodes/<node>/proxy/configz | jq .
```

## Compare across nodes
```bash
for n in $(kubectl get nodes -o name | cut -d/ -f2); do
  echo "$n $(kubectl get --raw /api/v1/nodes/$n/proxy/configz | jq -c '.kubeletconfig | {maxPods, cgroupDriver, imageGCHighThresholdPercent}')"
done
```
Drift between nodes usually comes from hand-edited `/var/lib/kubelet/config.yaml` or flags in
`/etc/default/kubelet`.

## Gotchas
- Fields set by flags show the flag value; if a config-file change "did nothing", look for a
  conflicting flag in `kubeadm-flags.env` or `KUBELET_EXTRA_ARGS`.
- Fields not supported by the running version are absent. If the kubelet will not start after a
  config edit, read `journalctl -u kubelet`.

## Checked

2026-10-26: kubernetes.io docs for v1.37 (kubernetes/website main, 2026-10-25). Confirmed: configz via the API server proxy path, merge order, fine-grained kubelet authorization table (nodes/configz, then proxy) and the KubeletFineGrainedAuthz gate stages (alpha 1.32, beta 1.33, stable 1.36). Replaced the client-certificate curl on the node with the documented kubectl proxy example; removed unconfirmed format and failure remarks.

Method: documentation only; no commands were run.
