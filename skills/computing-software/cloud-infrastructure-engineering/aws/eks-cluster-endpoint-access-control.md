---
id: computing-software.cloud-infrastructure-engineering.aws.eks-cluster-endpoint-access-control
name: eks-cluster-endpoint-access-control
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, eks, cluster-endpoint-access, private-cluster, public-access-cidrs, kubectl-access, api-server]
level: practitioner
status: docs-checked
description: "Choose and change EKS API endpoint access: public, public+private, or private-only; restrict public CIDRs; and reach a private cluster from CI, VPN or a bastion."
sources: ["https://docs.aws.amazon.com/eks/latest/userguide/cluster-endpoint.html", "https://docs.aws.amazon.com/eks/latest/userguide/private-clusters.html", "https://docs.aws.amazon.com/eks/latest/best-practices/control-plane.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EKS cluster endpoint access

## 1. Modes
| Mode | API server reachable from | Nodes reach API via |
|---|---|---|
| Public only (default) | internet (optionally limited by CIDR) | public endpoint (traffic leaves the VPC but not Amazon's network) |
| Public + private | internet (CIDR-limited) and inside the VPC | private VPC endpoint |
| Private only | inside the VPC and connected networks | private VPC endpoint |
Recommended: **public + private with tight public CIDRs**, or **private only** for
regulated environments. Authentication (IAM + access entries) applies in all modes; the
endpoint setting is network-level defence in depth.

## 2. Change it
```bash
aws eks update-cluster-config --name prod --resources-vpc-config \
  endpointPublicAccess=true,endpointPrivateAccess=true,publicAccessCidrs="203.0.113.0/24,198.51.100.10/32"
aws eks describe-update --name prod --update-id <id>
aws eks describe-cluster --name prod --query 'cluster.resourcesVpcConfig'
```
Poll `describe-update` until the update finishes. Public CIDRs only filter the public
endpoint; they do not affect the private endpoint. Remember CI/CD runners and the people running kubectl.

## 3. Private endpoint DNS
With private access on, the cluster's endpoint hostname resolves to private IPs **inside
the VPC** (EKS creates and manages a Route 53 private hosted zone that does not appear in
your account; the VPC needs `enableDnsHostnames` and `enableDnsSupport` set to true and
`AmazonProvidedDNS` in its DHCP options set). The EKS docs do not describe DNS for
other networks: a connected network or peered VPC needs its own resolution of the
endpoint name to the private IPs. The cluster security group must allow ingress on
port 443 from those sources.

## 4. Reaching a private-only cluster
- **Connected network**: connect via a transit gateway or other connectivity option and
  allow ingress on 443 from that network in the cluster security group.
- **EC2 bastion host** in the cluster VPC running kubectl; allow 443 from it in the cluster
  security group. Map its IAM principal in your RBAC configuration before removing public access.
- **CloudShell**: for private clusters, Connect in the EKS console launches a VPC
  environment that can reach the private endpoint.
- **CI/CD**: run the pipeline from inside the VPC or a connected network.

## 5. Private-only cluster prerequisites
Nodes in private subnets need VPC endpoints for what they call without internet:
`ec2`, `ecr.api`, `ecr.dkr`, `s3`, `logs`, `elasticloadbalancing`, `sts` (IRSA),
`oidc-eks` (IRSA setup from inside the VPC), `eks-auth` (Pod Identity), and `ssm` (SSM
Agent, optional). Use the form `com.amazonaws.<REGION>.<service>` and enable private DNS names.

## Gotchas
- Turning off public access while your kubectl is outside the VPC locks you out until you
  are on the private network; do it from inside.
- `publicAccessCidrs` must include the egress IPs of anything external (CI SaaS runners).
- The cluster security group rules control access to the private endpoint.

## Verify
- [ ] `describe-cluster` shows the intended access flags and CIDRs.
- [ ] From an unlisted IP, `kubectl get ns` times out; from the allowed network it works.
- [ ] Inside the VPC, `dig <endpoint-host>` returns private IPs; nodes are `Ready` with no NAT dependency (private-only).

## Checked
2026-10-28: Confirmed against EKS User Guide cluster-endpoint and private-clusters pages: public/private mode behaviour, the Route 53 private hosted zone and the VPC DNS settings it needs, port 443 ingress from connected networks and bastions, CloudShell VPC environment for private clusters, and the VPC endpoint list (ec2, ecr.api, ecr.dkr, s3, elasticloadbalancing, ssm, logs, sts, oidc-eks, eks-auth). Read end to end. Removed: the 40 public CIDR figure, Route 53 Resolver/Profiles forwarding steps, the SSM port-forwarding document name, the claim that Cloud9 is retired (the page still documents it, so it was dropped), the autoscaling endpoint, and the claim that additional security groups cannot be changed after creation.

Method: documentation only; no commands were run.
