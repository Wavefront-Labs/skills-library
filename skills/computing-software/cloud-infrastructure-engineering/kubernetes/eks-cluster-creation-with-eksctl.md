---
id: computing-software.cloud-infrastructure-engineering.kubernetes.eks-cluster-creation-with-eksctl
name: eks-cluster-creation-with-eksctl
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, eks, eksctl, eks-node-group, eks-addons, pod-identity, access-entries, aws]
level: practitioner
status: docs-checked
description: "Create a production EKS cluster with an eksctl ClusterConfig: endpoint access, managed node groups, EKS add-ons with Pod Identity, access entries, and the day-one gotchas."
sources: ["https://eksctl.io/usage/schema/", "https://eksctl.io/usage/access-entries/", "https://eksctl.io/usage/addons/", "https://eksctl.io/usage/pod-identity-associations/", "https://eksctl.io/usage/vpc-cluster-access/", "https://eksctl.io/usage/nodegroup-managed/", "https://eksctl.io/usage/custom-ami-support/", "https://docs.aws.amazon.com/eks/latest/userguide/kubernetes-versions.html", "https://kubernetes-sigs.github.io/aws-load-balancer-controller/latest/deploy/subnet_discovery/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Creating EKS clusters with eksctl

## ClusterConfig (commit it)
```yaml
apiVersion: eksctl.io/v1alpha5
kind: ClusterConfig
metadata: {name: prod, region: eu-west-1, version: "1.36"}   # a version in EKS standard support
vpc:
  id: vpc-0abc
  subnets:
    private:
      eu-west-1a: {id: subnet-a}
      eu-west-1b: {id: subnet-b}
      eu-west-1c: {id: subnet-c}
  clusterEndpoints: {privateAccess: true, publicAccess: true}
  publicAccessCIDRs: ["203.0.113.0/24"]
accessConfig:
  authenticationMode: API            # access entries, no aws-auth ConfigMap
  bootstrapClusterCreatorAdminPermissions: false
  accessEntries:
  - principalARN: arn:aws:iam::111122223333:role/platform-admins
    accessPolicies:
    - policyARN: arn:aws:eks::aws:cluster-access-policy/AmazonEKSClusterAdminPolicy
      accessScope: {type: cluster}
addonsConfig:
  autoApplyPodIdentityAssociations: true   # recommended IAM via Pod Identity where the add-on supports it
addons:
- {name: eks-pod-identity-agent, version: latest}
- {name: vpc-cni, version: latest}
- {name: coredns, version: latest}
- {name: kube-proxy, version: latest}
- {name: aws-ebs-csi-driver, version: latest}
managedNodeGroups:
- name: system-a
  instanceTypes: [<type-a>, <type-b>]
  amiFamily: AmazonLinux2023
  minSize: 2
  maxSize: 6
  desiredCapacity: 3
  privateNetworking: true
  labels: {pool: system}
  taints: [{key: CriticalAddonsOnly, value: "true", effect: NoSchedule}]
  updateConfig: {maxUnavailablePercentage: 33}
cloudWatch:
  clusterLogging: {enableTypes: [api, audit, authenticator]}
secretsEncryption: {keyARN: arn:aws:kms:eu-west-1:111122223333:key/...}
```
```bash
eksctl create cluster -f cluster.yaml --dry-run    # prints the full resulting ClusterConfig
eksctl create cluster -f cluster.yaml
eksctl utils describe-addon-versions --kubernetes-version 1.36
```

## Day-one gotchas
- Pick a version in EKS standard support; versions in extended support cost extra and age out
  (the EKS release calendar lists the dates).
- `amiFamily` defaults to `AmazonLinux2` in eksctl; set `AmazonLinux2023` explicitly.
- Private-only API endpoint: eksctl does not support creating a cluster with only private
  access (it could not join the nodes). Create with private and public access (restrict
  `publicAccessCIDRs`), then switch with
  `eksctl utils update-cluster-vpc-config -f cluster.yaml --approve`. Afterwards kubectl and
  `eksctl delete cluster` must run from inside the VPC (or from CIDRs added via `vpc.extraCIDRs`).
- Subnets need the tag `kubernetes.io/role/internal-elb` (private) or `kubernetes.io/role/elb`
  (public), value `1` or empty, for load balancer subnet discovery.
- VPC CNI gives pods VPC IPs, so small subnets run out quickly. Plan large subnets, enable
  prefix delegation (`ENABLE_PREFIX_DELEGATION=true`), or use custom networking on a secondary
  CIDR.
- `updateConfig` takes `maxUnavailable` or `maxUnavailablePercentage`, not both, and
  `maxUnavailable` cannot exceed `maxSize`.
- Setting both Pod Identity and IRSA for one add-on is a validation error.

## Verify
```bash
aws eks describe-cluster --name prod --query 'cluster.{v:version,ep:resourcesVpcConfig,auth:accessConfig}'
aws eks list-addons --cluster-name prod; kubectl get nodes -L pool
kubectl auth whoami
```
- [ ] Add-ons ACTIVE; nodes Ready in all three AZs; audit logs arriving in CloudWatch.

## Checked
Checked 2026-10-27 against the eksctl user docs (eksctl-io/eksctl userdocs: access entries,
add-ons and `utils describe-addon-versions`, pod identity associations and
`addonsConfig.autoApplyPodIdentityAssociations`, cluster endpoint access, managed node group
`updateConfig`, CloudWatch logging `enableTypes`, KMS `secretsEncryption`, dry run, AMI
families), the EKS Kubernetes versions page (awsdocs/amazon-eks-user-guide: 1.34-1.36 in
standard support, 1.31-1.33 in extended support, 1.31 extended support ending
26 November 2026) and the AWS Load Balancer Controller subnet discovery page. Corrected the
private-only endpoint at creation (not supported by eksctl), moved the version off 1.31 (now
in extended support), replaced per-add-on `useDefaultPodIdentityAssociations` (documented for
migrating existing add-ons) with `autoApplyPodIdentityAssociations`, and removed unconfirmed
pod-count, CloudFormation and node-group immutability claims.

Method: documentation only; no commands were run.
