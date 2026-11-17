---
id: computing-software.cloud-infrastructure-engineering.aws.eks-network-policies-and-security-groups-for-pods
name: eks-network-policies-and-security-groups-for-pods
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, eks, network-policies-eks, security-groups-for-pods, vpc-cni, pod-isolation, sg-policy]
level: advanced
status: docs-checked
description: "Isolate pod traffic on EKS: VPC CNI Kubernetes NetworkPolicy enforcement, SecurityGroupPolicy for per-pod security groups, when to use each, and how to debug."
sources: ["https://docs.aws.amazon.com/eks/latest/userguide/cni-network-policy.html", "https://docs.aws.amazon.com/eks/latest/userguide/security-groups-for-pods.html", "https://docs.aws.amazon.com/eks/latest/best-practices/network-security.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EKS network policies and security groups for pods

## 1. Two tools
| | Kubernetes NetworkPolicy (VPC CNI) | Security groups for pods |
|---|---|---|
| Scope | pod-to-pod, namespace, CIDR rules in K8s terms | AWS SG on a pod's branch ENI |
| Best for | east-west isolation inside the cluster | pod access to AWS resources that use SGs (RDS, ElastiCache) |
| Implementation | VPC CNI network policy support | trunk/branch ENIs (Nitro instances) |
| Selector | labels | `SecurityGroupPolicy` CRD by pod/SA labels |
Many clusters use both: NetworkPolicy for default-deny between namespaces, SGs for pods
for database access.

## 2. Enable NetworkPolicy in the VPC CNI
Turn on network policy in the VPC CNI add-on settings as described on the EKS network policy page.
It applies to EC2 Linux nodes only, not Fargate or Windows. Then standard policies work:
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: {name: default-deny, namespace: payments}
spec: {podSelector: {}, policyTypes: [Ingress, Egress]}
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: {name: allow-api-to-db-and-dns, namespace: payments}
spec:
  podSelector: {matchLabels: {app: api}}
  policyTypes: [Egress]
  egress:
    - to: [{namespaceSelector: {matchLabels: {kubernetes.io/metadata.name: kube-system}},
            podSelector: {matchLabels: {k8s-app: kube-dns}}}]
      ports: [{protocol: UDP, port: 53}, {protocol: TCP, port: 53}]
    - to: [{ipBlock: {cidr: 10.20.8.0/22}}]
      ports: [{protocol: TCP, port: 5432}]
```
Always allow DNS when adding egress deny. Cluster-wide policies (ClusterNetworkPolicy) need a recent VPC CNI; the EKS page gives the minimum version.

## 3. Security groups for pods
```bash
kubectl -n kube-system set env daemonset aws-node ENABLE_POD_ENI=true
```
(on the EKS add-on use configuration values). Nodes must be a Nitro instance type listed as trunking-compatible
(the t family is not supported); the node gets a trunk ENI, pods matching a policy get branch ENIs.
```yaml
apiVersion: vpcresources.k8s.aws/v1beta1
kind: SecurityGroupPolicy
metadata: {name: api-db-access, namespace: payments}
spec:
  serviceAccountSelector: {matchLabels: {role: api}}
  securityGroups: {groupIds: [sg-0apipods]}
```
Then the RDS SG allows `sg-0apipods` on 5432. Pod SG must also allow kubelet probes from
the node SG and DNS egress. `POD_SECURITY_GROUP_ENFORCING_MODE=standard` lets
NetworkPolicy and pod SGs both apply; `strict` (default) enforces only SGs for those pods.

## 4. Debugging
- NetworkPolicy: `kubectl get policyendpoints -A` shows the PolicyEndpoint objects EKS creates (do not edit them).
- Pod SG: VPC flow logs on the pod's ENI show SG rejects.
- Test with an ephemeral pod: `kubectl run t --rm -it --image=busybox -- nc -zv db 5432`.

## Gotchas
- Fargate pods support security groups for pods but not VPC CNI network policies.
- With `standard` mode, pod traffic leaving the VPC is translated to the node's primary interface, so the node's SG rules apply to it.

## Checked
2026-11-01: confirmed against the EKS VPC CNI network policy and security groups for pods pages (trunking-compatible Nitro, t family unsupported, strict default and standard mode, Fargate, EC2 Linux only, PolicyEndpoint CRD). Removed: add-on config key, minimum version, eBPF, agent log path and event-log setting, pod-eni annotation, ENI limit and connection-persistence claims.
Method: documentation only; no commands were run.

## Verify
- [ ] Default-deny in each app namespace; a test pod from another namespace cannot connect.
- [ ] API pods reach the database; other pods are refused by the RDS SG.
