---
id: computing-software.cybersecurity-defensive.cloud-security.kubernetes-incident-response
name: kubernetes-incident-response
category: computing-software
field: cybersecurity-defensive
product: cloud-security
tags: [cloud-incident-response, kubernetes-incident-response, pod-isolation, container-forensics, network-policy-quarantine, cordon-node, eks-ir]
level: advanced
status: draft
description: "Respond to a compromised Kubernetes workload: isolate pods with labels and NetworkPolicy, cordon nodes, capture container state, scope via audit logs, rotate credentials."
sources: ["https://aws.github.io/aws-eks-best-practices/security/docs/incidents/", "https://kubernetes.io/docs/concepts/services-networking/network-policies/", "https://www.cncf.io/blog/2021/11/12/kubernetes-forensics/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Kubernetes incident response

Pods are ephemeral: if you delete or let a deployment replace the compromised pod, evidence disappears.
Isolate first, keep it running, capture, then remove.

## 1. Identify
From the alert (Falco/GuardDuty/EDR), get cluster, namespace, pod, container ID, node, service account,
image digest.

## 2. Isolate without destroying
- **Remove from service**: relabel the pod so the ReplicaSet/Service selector no longer matches
  (`kubectl label pod <p> app- quarantine=true --overwrite`); the controller spins up a replacement and the
  compromised pod keeps running, detached from traffic.
- **Network quarantine**: NetworkPolicy denying all ingress/egress for `quarantine=true`:
  ```yaml
  apiVersion: networking.k8s.io/v1
  kind: NetworkPolicy
  metadata: {name: quarantine, namespace: prod}
  spec:
    podSelector: {matchLabels: {quarantine: "true"}}
    policyTypes: [Ingress, Egress]
  ```
  (requires a CNI that enforces NetworkPolicy).
- **Node**: `kubectl cordon <node>` so nothing new schedules there; consider isolating the node at
  cloud level (security group) if escape is suspected.
- **Credentials**: the pod's service account token and any cloud identity (IRSA/Pod Identity, node role)
  are compromised: remove RBAC bindings/ revoke, rotate secrets it could read.

## 3. Capture
- `kubectl get pod <p> -o yaml`, `kubectl describe`, `kubectl logs --all-containers --previous`.
- Container filesystem diff and archive: `kubectl exec` is risky (changes state); prefer node-level tools:
  `crictl inspect <id>`, `crictl ps`, runtime checkpoint (`kubectl debug`/CRIU-based checkpoint API,
  beta), or copy the container's overlay upper dir from the node.
- Node memory and disk: snapshot the node volume (EBS snapshot) and capture memory (LiME/AVML) if escape suspected.
- Audit logs (API server), CloudTrail/cloud logs, Falco/EDR events, VPC flow logs for the node/pod IPs.

## 4. Scope
Audit log queries for the service account and any users: exec, secret reads, new pods/bindings, webhooks.
Check image provenance (was the image itself malicious?), other pods from the same image.

## 5. Eradicate and recover
Delete quarantined pods after capture, drain and replace nodes, fix the root cause (vulnerable app,
exposed dashboard, over-privileged SA), redeploy from trusted images, rotate secrets.

## Gotchas
- Autoscalers or `kubectl delete` by well-meaning engineers destroy evidence: announce a freeze.
- Distroless images lack shells; use ephemeral debug containers (`kubectl debug -it <pod> --image=busybox --target=<c>`) with care.

## Verify
Quarantined pod has no network connectivity (test from it), replacement serves traffic, evidence hashes
recorded, and no further suspicious audit events for the SA.
