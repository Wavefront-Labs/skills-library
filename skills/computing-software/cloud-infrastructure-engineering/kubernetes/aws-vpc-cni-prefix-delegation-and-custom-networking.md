---
id: computing-software.cloud-infrastructure-engineering.kubernetes.aws-vpc-cni-prefix-delegation-and-custom-networking
name: aws-vpc-cni-prefix-delegation-and-custom-networking
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, cni, aws-vpc-cni, prefix-delegation, ip-exhaustion, eks]
level: practitioner
status: docs-checked
description: "Tune the AWS VPC CNI: prefix delegation for pod density, warm IP targets, custom networking with ENIConfig for secondary CIDRs, and max-pods alignment."
sources: ["https://docs.aws.amazon.com/eks/latest/userguide/cni-increase-ip-addresses.html", "https://docs.aws.amazon.com/eks/latest/userguide/cni-increase-ip-addresses-procedure.html", "https://docs.aws.amazon.com/eks/latest/userguide/cni-custom-network.html", "https://docs.aws.amazon.com/eks/latest/userguide/cni-custom-network-tutorial.html", "https://github.com/aws/amazon-vpc-cni-k8s/blob/master/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AWS VPC CNI tuning

Pods get real VPC IPs from network interfaces attached to the node; the instance type caps the
number of interfaces and IPs per interface, so a node can run out of pod IPs before it runs out
of CPU or memory.

## Prefix delegation (more pods per node)
```bash
kubectl set env daemonset aws-node -n kube-system ENABLE_PREFIX_DELEGATION=true
kubectl set env daemonset aws-node -n kube-system WARM_PREFIX_TARGET=1
```
Each interface slot gets a /28 IPv4 prefix instead of a single secondary IP. Nitro instances
only; Linux and Windows procedures differ. Max pods stays capped: 110 by default, and managed
node groups enforce at most 110 for instances with fewer than 30 vCPUs and 250 otherwise.
- Managed node groups without a launch template, or with one that has no AMI ID, calculate
  max pods automatically. Self-managed node groups and launch templates with an AMI ID must
  set max pods themselves (`maxPods` in eksctl, `--max-pods` kubelet argument).
- AWS recommends creating new node groups for the transition rather than rolling existing
  nodes, because nodes holding both IPs and prefixes advertise inconsistent capacity.
- Subnets need contiguous free /28 blocks; fragmented subnets fail with
  `InsufficientCidrBlocks`. Use a subnet CIDR reservation for prefixes, or a new subnet.

## Warm pool knobs
`WARM_ENI_TARGET` (default 1), `WARM_IP_TARGET`, `MINIMUM_IP_TARGET`, `WARM_PREFIX_TARGET`.
Setting `WARM_IP_TARGET` or `MINIMUM_IP_TARGET` overrides `WARM_PREFIX_TARGET`. Lower values
save IPs in crowded subnets, at the cost of more EC2 API calls and slower pod start under bursts.

## Custom networking (pods in a secondary CIDR)
Solves node-subnet IP exhaustion by putting pod interfaces in subnets from an additional VPC
CIDR block, in the same Availability Zones as the node subnets.
```bash
kubectl set env daemonset aws-node -n kube-system AWS_VPC_K8S_CNI_CUSTOM_NETWORK_CFG=true
kubectl set env daemonset aws-node -n kube-system ENI_CONFIG_LABEL_DEF=topology.kubernetes.io/zone
```
```yaml
apiVersion: crd.k8s.amazonaws.com/v1alpha1
kind: ENIConfig
metadata: {name: eu-west-1a}          # matches the zone label value
spec:
  subnet: subnet-0abc...
  securityGroups: [sg-0123...]
```
With custom networking no IPs from the primary network interface go to pods, which lowers max
pods; recalculate it. Not available for IPv6 clusters. Nodes that ran pods before the switch
must be replaced (the EKS tutorial terminates them or deletes their node group). With the
default `AWS_VPC_K8S_CNI_EXTERNALSNAT=false`, traffic leaving the VPC still uses the primary
interface's subnet and security groups.

## Verify
```bash
kubectl -n kube-system get ds aws-node -o jsonpath='{.spec.template.spec.containers[0].env}' | jq
kubectl get node <n> -o jsonpath='{.status.allocatable.pods}'
```

## Checked
Checked 2026-10-27 against the Amazon EKS User Guide source (awsdocs/amazon-eks-user-guide:
prefix assignment considerations and procedure, custom networking considerations and
tutorial) and the amazon-vpc-cni-k8s README (`WARM_ENI_TARGET` default 1, /28 prefixes,
`ENI_CONFIG_LABEL_DEF`, `AWS_VPC_K8S_CNI_CUSTOM_NETWORK_CFG`): /28 prefixes, Nitro only,
contiguous blocks and `InsufficientCidrBlocks`, CIDR reservations, the 110/250 managed node
group cap, automatic max-pods calculation, new node groups for the transition, override order
of warm targets, primary interface excluded under custom networking, terminating existing
nodes. Removed the unconfirmed m5.large 29-to-110 figure, the max-pods calculator invocation
and a Karpenter claim.

Method: documentation only; no commands were run.
