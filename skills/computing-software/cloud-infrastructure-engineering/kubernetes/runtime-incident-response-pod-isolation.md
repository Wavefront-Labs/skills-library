---
id: computing-software.cloud-infrastructure-engineering.kubernetes.runtime-incident-response-pod-isolation
name: runtime-incident-response-pod-isolation
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, runtime-security, runtime-incident-response, pod-isolation, forensics, checkpoint]
level: practitioner
status: docs-checked
description: "Respond to a runtime security alert in a pod by isolating it from traffic, capturing evidence (logs, filesystem, checkpoint) and then removing and rebuilding safely."
sources: ["https://kubernetes.io/docs/reference/node/kubelet-checkpoint-api/", "https://kubernetes.io/docs/concepts/services-networking/network-policies/", "https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/#isolating-pods-from-a-replicaset", "https://kubernetes.io/docs/tasks/debug/debug-application/debug-running-pod/", "https://kubernetes.io/docs/concepts/security/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Responding to a runtime alert

Do not delete the pod first: that destroys the evidence and the controller simply recreates
the compromised image.

## 1. Isolate
```bash
NS=shop; POD=web-7c9-abc12
kubectl label pod $POD -n $NS quarantine=true --overwrite
kubectl label pod $POD -n $NS app-     # drop the Service label: traffic stops, ReplicaSet makes a replacement
```
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: {name: quarantine, namespace: shop}
spec:
  podSelector: {matchLabels: {quarantine: "true"}}
  policyTypes: [Ingress, Egress]          # no rules: deny all (needs a CNI that enforces NetworkPolicy)
```
Cordon the node so nothing new lands there: `kubectl cordon <node>`.
Removing the controller's selector label orphans the pod, so scaling later will not delete it.

## 2. Capture
```bash
kubectl get pod $POD -n $NS -o yaml > pod.yaml
kubectl logs $POD -n $NS --all-containers --timestamps > logs.txt
kubectl debug -it $POD -n $NS --image=<debug-image> --target=app -- sh   # ephemeral container sharing the target's process namespace
# container checkpoint: ContainerCheckpoint gate (beta, on by default since v1.30); the runtime must implement the CRI checkpoint call
curl -sk -X POST --cert admin.crt --key admin.key https://<node>:10250/checkpoint/$NS/$POD/app
```
The checkpoint archive is written under the kubelet root directory (default `/var/lib/kubelet/checkpoints`), is a tar
of the container including all process memory, and may contain keys: treat it as a secret and
move it off the node. Also pull the audit log entries for the pod's ServiceAccount and the Falco events.

## 3. Eradicate
- Delete the pod; rotate any Secret and ServiceAccount token it could read.
- If container escape is possible (privileged, hostPath, kernel exploit), drain and rebuild the node.
- Patch the image or config hole, then remove the quarantine policy.

## Verify
The quarantined pod shows no network flows (Hubble or CNI logs), evidence files are stored
off-cluster with hashes, and replaced credentials are no longer accepted.

## Checked

Checked 2026-10-27 against Kubernetes website content (main, v1.38 dev tree) and the v1.37 line (latest release at review time).

- Kubelet checkpoint API (`POST /checkpoint/{namespace}/{pod}/{container}`, archive under the kubelet root directory, memory contents warning) and the `ContainerCheckpoint` gate (alpha v1.25, beta default on from v1.30) confirmed.
- Removing a Pod from a ReplicaSet by changing its labels confirmed in the ReplicaSet page; NetworkPolicy isolation semantics and the need for an enforcing network plugin confirmed in the NetworkPolicy page.
- `kubectl debug --image ... --target` confirmed in the debug-running-pod page.
- Removed the unconfirmed `crictl inspect | jq` filesystem step and the pinned busybox tag.

Method: documentation only; no commands were run.
