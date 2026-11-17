---
id: computing-software.cloud-infrastructure-engineering.aws.eks-cluster-operations
name: eks-cluster-operations
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, eks, eks-cluster, kubernetes, managed-node-group, fargate-profile, karpenter, eksctl, irsa, pod-identity, eks-access-entries, aws-auth, vpc-cni, ip-exhaustion, prefix-delegation, eks-addons, cluster-upgrade, control-plane-logging, aws-load-balancer-controller, ebs-csi, efs-csi, eks-auto-mode]
level: advanced
status: gated
description: "Operate EKS clusters: eksctl create, access entries, IRSA vs Pod Identity, VPC CNI IP planning, managed add-ons, node groups vs Karpenter, and in-place version upgrades."
sources: ["https://docs.aws.amazon.com/eks/latest/userguide/getting-started.html", "https://docs.aws.amazon.com/eks/latest/userguide/access-entries.html", "https://docs.aws.amazon.com/eks/latest/userguide/pod-identities.html", "https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html", "https://docs.aws.amazon.com/eks/latest/userguide/update-cluster.html", "https://docs.aws.amazon.com/eks/latest/best-practices/networking.html", "https://eksctl.io/usage/schema/", "https://karpenter.sh/docs/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# EKS cluster operations

**Goal:** an EKS cluster that engineers can authenticate to, where pods get AWS
permissions without node-wide credentials, that does not run out of IPs, and that can be
upgraded one minor version at a time without surprises. Generic Kubernetes operation is
under `computing-software.cloud-infrastructure-engineering.kubernetes`; this skill is
the AWS-specific layer.

## 1. Create
```yaml
# cluster.yaml  (eksctl create cluster -f cluster.yaml)
apiVersion: eksctl.io/v1alpha5
kind: ClusterConfig
metadata: {name: prod, region: eu-west-1, version: "1.31"}
accessConfig:
  authenticationMode: API_AND_CONFIG_MAP   # API = access entries; keep CONFIG_MAP only during migration
vpc:
  id: vpc-0abc
  subnets:
    private: {eu-west-1a: {id: subnet-a}, eu-west-1b: {id: subnet-b}, eu-west-1c: {id: subnet-c}}
  clusterEndpoints: {privateAccess: true, publicAccess: true}
  publicAccessCIDRs: ["<OFFICE_CIDR>/32"]
cloudWatch:
  clusterLogging: {enableTypes: [api, audit, authenticator, controllerManager, scheduler]}
addons:
  - {name: vpc-cni, version: latest, configurationValues: '{"env":{"ENABLE_PREFIX_DELEGATION":"true"}}'}
  - {name: coredns, version: latest}
  - {name: kube-proxy, version: latest}
  - {name: eks-pod-identity-agent, version: latest}
  - {name: aws-ebs-csi-driver, version: latest, useDefaultPodIdentityAssociations: true}
managedNodeGroups:
  - name: system
    instanceType: m7g.large
    amiFamily: AmazonLinux2023
    minSize: 2; maxSize: 4; desiredCapacity: 2
    privateNetworking: true
    labels: {role: system}
    taints: [{key: CriticalAddonsOnly, value: "true", effect: NoSchedule}]
```
- Subnets: tag `kubernetes.io/role/internal-elb=1` (private) and
  `kubernetes.io/role/elb=1` (public) so the Load Balancer Controller can find them.
- Control-plane ENIs live in the subnets you list; give them ≥ 16 free IPs each and
  never delete those subnets while the cluster exists.
- **EKS Auto Mode** (`autoModeConfig.enabled: true`) lets AWS run nodes, Karpenter, LB
  controller and CSI for you — simplest path for new clusters if you accept its constraints.

## 2. Who can `kubectl`
Use **access entries** (IAM principal → Kubernetes access policy), not the `aws-auth`
ConfigMap:
```bash
aws eks create-access-entry --cluster-name prod --principal-arn arn:aws:iam::<ACCOUNT_ID>:role/platform-admins
aws eks associate-access-policy --cluster-name prod --principal-arn arn:aws:iam::<ACCOUNT_ID>:role/platform-admins \
  --policy-arn arn:aws:eks::aws:cluster-access-policy/AmazonEKSClusterAdminPolicy --access-scope type=cluster
aws eks update-kubeconfig --name prod --region eu-west-1
```
The creator principal is admin only while `bootstrapClusterCreatorAdminPermissions` is
true — add a named admin role before anyone leaves. Policies: `ClusterAdmin`, `Admin`
(namespace-scoped), `Edit`, `View`; finer control = access entry + RBAC `RoleBinding`
to the entry's `kubernetesGroups`.

## 3. Pod permissions: IRSA vs Pod Identity
| | IRSA | EKS Pod Identity |
|---|---|---|
| Mechanism | OIDC provider per cluster + role trust policy with `sub` condition | `eks-pod-identity-agent` add-on + association API |
| Role reuse across clusters | Trust policy per cluster OIDC URL | One role, many associations |
| Needs | `eksctl utils associate-iam-oidc-provider` | Add-on + `eks:CreatePodIdentityAssociation` |
| Works outside EKS | Yes (any OIDC k8s) | EKS only; not Fargate pods or Windows |
Pod Identity is the default for new work:
```bash
aws eks create-pod-identity-association --cluster-name prod --namespace app \
  --service-account api --role-arn arn:aws:iam::<ACCOUNT_ID>:role/api-pod
```
Role trust: principal `pods.eks.amazonaws.com`, actions `sts:AssumeRole` **and**
`sts:TagSession`. Either way, block node-role credential leakage: set IMDS hop limit 1
on node groups (eksctl `metadataOptions.httpPutResponseHopLimit: 1`) or use the
Pod Identity agent's network policy.

## 4. Networking: do not run out of IPs
- VPC CNI gives each pod a VPC IP; default per-ENI secondary IPs cap pods per node
  (`m5.large` = 29). **Prefix delegation** (`ENABLE_PREFIX_DELEGATION=true`) assigns /28
  prefixes and raises the cap to the kubelet `max-pods` (set `--max-pods` via
  `useMaxPods`/bootstrap), but needs contiguous free address blocks, so fragmented subnets can fail (gated: unconfirmed, source is paywalled or blocked).
- Plan subnets large (/19 per AZ) or use **custom networking** (`AWS_VPC_K8S_CNI_CUSTOM_NETWORK_CFG`
  + `ENIConfig` per AZ) to put pods in a secondary CIDR (100.64.0.0/16) that the rest of
  the VPC does not consume.
- Security groups for pods (`ENABLE_POD_ENI`) attach SGs per pod via `SecurityGroupPolicy`
  — needed when an RDS SG must admit only one workload.
- `kubectl describe node | grep -A5 Allocatable` and the CNI metrics
  (`awscni_assigned_ip_addresses`) show headroom; `FailedCreatePodSandBox … no available IP addresses`
  is the symptom of exhaustion.

## 5. Nodes: managed node groups vs Karpenter
- **Managed node groups**: ASG-backed, AWS handles draining on update
  (`aws eks update-nodegroup-version`), supports Spot (`spot: true` with diversified
  `instanceTypes`), launch template for custom AMI/user data. Good for a steady system pool.
- **Karpenter**: provisions right-sized nodes per pending pod in seconds, consolidates,
  handles Spot interruption; install via Helm with an IRSA/Pod Identity role, an SQS
  interruption queue, and `NodePool` + `EC2NodeClass` CRDs. Run Karpenter itself on the
  managed system node group (never on nodes it manages). Set `consolidationPolicy: WhenEmptyOrUnderutilized`
  and `expireAfter` (e.g. `720h`) so nodes rotate onto new AMIs.
- Fargate profiles: per-namespace/label serverless pods; no DaemonSets, no EBS, one pod per micro-VM, slower start (gated: unconfirmed, source is paywalled or blocked). Use for isolated batch or when you cannot run nodes.

## 6. Add-ons and storage
Prefer **EKS managed add-ons** (`aws eks describe-addon-versions --kubernetes-version 1.31`)
so upgrades are `update-addon`; `resolveConflicts: OVERWRITE` on first install when a
self-managed copy exists. Essentials beyond the core four: `aws-ebs-csi-driver` (any
PVC with `gp3` StorageClass — the legacy in-tree provisioner is gone), `aws-efs-csi-driver`
for RWX, `aws-load-balancer-controller` (Helm, not managed add-on on most versions) for
`Ingress` → ALB and `Service type=LoadBalancer` → NLB with `service.beta.kubernetes.io/aws-load-balancer-type: external`.

## 7. Upgrades
Each Kubernetes version has a standard support window and then extended support at a higher
control-plane price (see the EKS pricing and versions pages) — upgrade on cadence. One minor at a time:
1. `kubectl get --raw /metrics | grep apiserver_requested_deprecated_apis` and
   **EKS upgrade insights** (`aws eks list-insights`) for removed APIs.
2. `aws eks update-cluster-version --name prod --kubernetes-version 1.32` (control plane,
   API stays up).
3. Update add-ons to versions compatible with the new release (`describe-addon-versions`).
4. Node groups: `update-nodegroup-version` (rolling, respects PDBs; `--force` ignores
   PDBs) or bump Karpenter `EC2NodeClass` AMI selector and let drift rotate.
5. Update `kubectl` / client libraries within one minor skew.
From Kubernetes 1.28 the kubelet may be up to **three** minor versions older than the kube-apiserver
(per the EKS update docs); check `kubectl get nodes` before each step. After a control plane upgrade
you can roll back to the previous version within 7 days (see "Roll back a cluster" in the EKS docs).

## Gotchas
- `error: You must be logged in to the server (Unauthorized)` — the IAM principal has no
  access entry (or wrong cluster in kubeconfig); `aws sts get-caller-identity` first.
- Deleting the VPC CNI add-on removes pod networking cluster-wide; the managed add-on
  with `preserve` keeps resources on delete.
- CoreDNS on the system node group only if the group tolerates its default scheduling;
  with taints on every node CoreDNS stays `Pending` and nothing resolves.
- Cluster security group vs node security group: the cluster SG must allow 443 from
  nodes and ephemeral ports back; custom SGs on node groups must be added to it.
- Public endpoint with `0.0.0.0/0` is the default; restrict `publicAccessCIDRs` or go private + VPN/bastion.
- Unconfirmed: exact extended-support pricing multiplier and Auto Mode feature parity per region.

## Verify
- [ ] `kubectl get nodes` all `Ready`, same minor as control plane; `aws eks list-insights` shows no `ERROR`.
- [ ] A pod with the associated service account runs `aws sts get-caller-identity` and sees the pod role, not the node role.
- [ ] Node `Allocatable.pods` matches the planned density; subnet free-IP count leaves > 20% headroom.
- [ ] Control-plane `audit` log stream exists in CloudWatch `/aws/eks/prod/cluster`.
- [ ] An `Ingress` produces an ALB in the tagged public subnets; a `gp3` PVC binds.

## Checked

Date: 2026-11-02. Confirmed on the EKS User Guide pages in sources (getting started, access entries, Pod Identity, IAM roles for service accounts, cluster update, networking best practices): access entries and authentication-mode changes, Pod Identity and IRSA as the two pod-IAM routes, upgrade flow. Removed as not stated there: the 10-15 minute control-plane upgrade time. Left, marked gated: the Fargate and prefix-delegation specifics, because the pages fetched do not state them.

Method: documentation only; no commands were run.
