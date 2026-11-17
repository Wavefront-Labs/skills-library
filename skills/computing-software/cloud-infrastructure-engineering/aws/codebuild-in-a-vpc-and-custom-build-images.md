---
id: computing-software.cloud-infrastructure-engineering.aws.codebuild-in-a-vpc-and-custom-build-images
name: codebuild-in-a-vpc-and-custom-build-images
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, codebuild, codebuild-vpc, custom-build-image, ecr, privileged-mode, docker-layer-cache]
level: practitioner
status: docs-checked
description: "Run CodeBuild inside a VPC to reach private resources (subnets, NAT or endpoints, security groups) and build with custom images from ECR, privileged mode and caching."
sources: ["https://docs.aws.amazon.com/codebuild/latest/userguide/vpc-support.html", "https://docs.aws.amazon.com/codebuild/latest/userguide/use-vpc-endpoints-with-codebuild.html", "https://docs.aws.amazon.com/codebuild/latest/userguide/build-caching.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CodeBuild in a VPC and custom build images

## VPC builds
```bash
aws codebuild update-project --name app-build --vpc-config \
  vpcId=vpc-0abc,subnets=subnet-priv-a,subnet-priv-b,securityGroupIds=sg-build
```
Checklist from the VPC page:
- Choose **private subnets only**, in multiple Availability Zones, separate from other workloads. Put a NAT gateway (or NAT instance) in a public subnet: CodeBuild cannot use an internet gateway because it does not support Elastic IPs on its network interfaces and EC2 does not auto-assign public IPs to interfaces created outside instance launches.
- Security groups: allow no inbound traffic to the builds. Outbound has no CodeBuild-specific requirement, but allow what the build needs (GitHub, S3, and so on). Target resources (RDS, internal APIs) must allow the build's security group.
- Use cases: integration tests against private RDS or ElastiCache, internal load balancers, internal package repositories, S3 buckets that allow only VPC endpoint access, and a fixed NAT Elastic IP for external services that need allow-listing.
- Not supported: shared VPCs.
- For services with PrivateLink you can use interface endpoints instead of NAT; use a NAT gateway for services without PrivateLink support. CodeBuild's own interface endpoint is `com.amazonaws.<region>.codebuild`; endpoints work with Amazon-provided DNS only (use conditional forwarding otherwise). An endpoint policy can limit principals, actions and resources (for example only `StartBuild`, `BatchGetBuilds` and `ListBuildsForProject` on one project).
- The service role needs EC2 permissions to create and manage network interfaces in your VPC: take the exact policy from the "Allow Amazon VPC access in your CodeBuild projects" page rather than from memory.

## Custom images
```bash
aws codebuild update-project --name app-build --environment \
  'type=LINUX_CONTAINER,computeType=BUILD_GENERAL1_MEDIUM,image=<ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/build-images/node20:2026-10,imagePullCredentialsType=SERVICE_ROLE,privilegedMode=true'
```
- `privilegedMode` is needed to run the Docker daemon (`docker build`) in the build.
- `imagePullCredentialsType=SERVICE_ROLE` makes CodeBuild pull with the project's service role, which then needs ECR pull permissions (cross-account also needs the ECR repository policy). Use `ARM_CONTAINER` for Arm environments.
- Pin a tag or digest and rebuild custom images on a schedule to pick up patches.

## Caching
- Two cache types: Amazon S3, or local. Local needs one or more modes: source cache, Docker layer cache, custom cache.
- Docker layer cache is Linux only and requires privileged mode, which gives the container access to all devices; enable it deliberately.

## Verify
- [ ] A build in the VPC reaches the private database and still downloads dependencies (NAT or endpoints).
- [ ] The custom image pulls with the service role; `docker build` works with privileged mode.
- [ ] Build duration improves with the cache on the second run.

## Checked
2026-10-28. Confirmed on the vpc-support, use-vpc-endpoints-with-codebuild and build-caching pages: private subnets, NAT requirement and the reason, multi-AZ and security group guidance, shared-VPC limitation, endpoint name, DNS limit, endpoint policy, cache types and modes, Docker layer cache constraints. Removed as unconfirmed: the list of EC2 permissions, the specific endpoint list for ECR/Logs/STS, the `DOWNLOAD_SOURCE` failure remark, the "Validate VPC settings" button, curated image tags and their start-up behaviour, Docker Hub rate-limit advice, per-host best-effort cache wording, reserved capacity fleet VPC support, and a made-up account ID.
Method: documentation only; no commands were run.
