---
id: computing-software.cloud-infrastructure-engineering.kubernetes.cloud-metadata-endpoint-blocking
name: cloud-metadata-endpoint-blocking
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, egress-control, metadata-endpoint-block, imds, workload-identity, network-policy, node-metadata-concealment]
level: practitioner
status: docs-checked
description: "Stop pods from stealing node credentials via the cloud metadata endpoint (169.254.169.254): IMDSv2 hop limit, NetworkPolicy egress except, and workload identity."
sources: ["https://docs.aws.amazon.com/eks/latest/best-practices/identity-and-access-management.html", "https://docs.cloud.google.com/kubernetes-engine/docs/concepts/workload-identity", "https://learn.microsoft.com/en-us/azure/aks/workload-identity-overview", "https://kubernetes.io/docs/concepts/services-networking/network-policies/", "https://github.com/kubernetes-sigs/network-policy-api"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Blocking the cloud metadata endpoint

A pod that can reach `169.254.169.254` can often fetch the node's cloud credentials and act as the
node: AWS notes that a pod can inherit the rights of the instance profile assigned to its worker
node. This is a classic server-side request forgery escalation.

## AWS
- AWS's EKS best practices block pod access to instance metadata by requiring IMDSv2 and setting the
  PUT response hop limit to 1, on the instance or in the node group launch template:
  `aws ec2 modify-instance-metadata-options --instance-id <id> --http-tokens required --http-put-response-hop-limit 1`.
  AWS warns this stops pods that do not use IRSA or EKS Pod Identity from inheriting the node role,
  and says not to disable instance metadata entirely (components such as the node termination
  handler need it). AWS also documents blocking pod access with iptables on the node.
- Nodes created by eksctl or the official CloudFormation templates are documented as enabling both
  IMDSv1 and IMDSv2 with a hop limit of 2, so pods can reach metadata until you change it.
- Give pods their own credentials via IRSA or EKS Pod Identity (AWS recommends Pod Identity unless you
  have a specific need for IRSA).

## GCP
Workload Identity Federation for GKE deploys the GKE metadata server on every node as a DaemonSet.
It intercepts requests to `169.254.169.254` (`metadata.google.internal`) and serves the subset of
Compute Engine metadata endpoints that Kubernetes workloads need, returning the identity configured
for the calling Pod rather than the node's.

## Azure
Use Microsoft Entra Workload ID, which federates pods to Microsoft Entra-protected services without
managed-identity credentials on the node. Block `169.254.169.254` for pods with the NetworkPolicy
below as defense in depth.

## NetworkPolicy (any cloud, defense in depth)
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: {name: deny-metadata, namespace: shop}
spec:
  podSelector: {}
  policyTypes: [Egress]
  egress:
  - to:
    - ipBlock:
        cidr: 0.0.0.0/0
        except: [169.254.169.254/32]
```
Namespaced policies must exist in every namespace; use a cluster-wide mechanism (Calico
GlobalNetworkPolicy, CiliumClusterwideNetworkPolicy, ClusterNetworkPolicy with a `Deny` action) so new namespaces
are covered.

## Verify
```bash
kubectl -n shop run t --rm -it --image=curlimages/curl --restart=Never -- \
  curl -s -m 3 http://169.254.169.254/latest/meta-data/ || echo blocked
```
Expect `blocked`. This probe is only meaningful on a cluster whose CNI enforces NetworkPolicy.

## Checked

2026-10-27. Release: AWS EKS best practices (main), GKE and AKS documentation, Kubernetes v1.37 docs, network-policy-api (main), October 2026
- Confirmed in the AWS EKS best practices source that IMDSv2-only with hop limit 1 (`--http-tokens required --http-put-response-hop-limit 1`) blocks pod access, the warning about non-IRSA pods, the iptables alternative, and that eksctl and the official CloudFormation templates set hop limit 2 with both IMDS versions enabled.
- Confirmed in the GKE documentation that the GKE metadata server runs as a per-node DaemonSet and intercepts `169.254.169.254` requests; the feature is now named Workload Identity Federation for GKE.
- Confirmed Microsoft Entra Workload ID for AKS; removed the claim that AKS nodes answer for the kubelet identity, which the page read did not state.
- Confirmed the network-policy-api project now describes `ClusterNetworkPolicy` (`policy.networking.k8s.io`, v1alpha2) with `Pass`, `Deny` and `Accept` actions, replacing the old AdminNetworkPolicy name used in this skill.

Method: documentation only; no commands were run.
