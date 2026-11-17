---
id: computing-software.cloud-infrastructure-engineering.aws.ecr-private-pulls-via-vpc-endpoints
name: ecr-private-pulls-via-vpc-endpoints
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, ecr, ecr-vpc-endpoints, privatelink, s3-gateway-endpoint, fargate, private-subnets]
level: practitioner
status: docs-checked
description: "Pull ECR images from private subnets without NAT: ecr.api and ecr.dkr interface endpoints, the S3 gateway endpoint for layers, logs endpoint for Fargate, and endpoint policies."
sources: ["https://docs.aws.amazon.com/AmazonECR/latest/userguide/vpc-endpoints.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Private ECR pulls via VPC endpoints

## Endpoints needed
| Endpoint | Type | Why |
|---|---|---|
| `com.amazonaws.<region>.ecr.api` | Interface | `GetAuthorizationToken`, describe/list APIs |
| `com.amazonaws.<region>.ecr.dkr` | Interface | Docker registry API (manifests) |
| `com.amazonaws.<region>.s3` | **Gateway** | image layers are served from S3 |
| `com.amazonaws.<region>.logs` | Interface | `awslogs` driver for Fargate tasks in a VPC without an internet gateway |
```bash
for s in ecr.api ecr.dkr logs; do
  aws ec2 create-vpc-endpoint --vpc-id $VPC --vpc-endpoint-type Interface \
    --service-name com.amazonaws.eu-west-1.$s --subnet-ids $SUBNETS \
    --security-group-ids $SG_ENDPOINTS --private-dns-enabled
done
aws ec2 create-vpc-endpoint --vpc-id $VPC --vpc-endpoint-type Gateway \
  --service-name com.amazonaws.eu-west-1.s3 --route-table-ids $PRIVATE_RTS
```
- The ECR docs require private DNS to be enabled on the `ecr.dkr` endpoint.
- The endpoint security group must allow inbound HTTPS (443) from the resources that pull.
- The S3 gateway endpoint must be associated with the **route tables** of the workload subnets.
- ECS on EC2, and Fargate platform version 1.4.0 or later, need both ECR endpoints plus the S3 gateway endpoint; Fargate 1.3.0 or earlier needs only `ecr.dkr` plus S3.

## Endpoint policies
The S3 gateway endpoint policy, if restricted, must allow the ECR layer bucket (`prod-<region>-starport-layer-bucket`):
```json
{"Effect":"Allow","Principal":"*","Action":"s3:GetObject",
 "Resource":"arn:aws:s3:::prod-eu-west-1-starport-layer-bucket/*"}
```
ECR interface endpoints also support an endpoint policy; see the endpoint policy section of the ECR VPC endpoints page.

## Gotchas
- Layers are downloaded from S3, so a missing S3 gateway endpoint breaks pulls in a subnet with no other route to S3.
- Interface endpoints and the S3 gateway endpoint need to exist in each Region you pull from.
- Interface endpoints are billed; check current VPC endpoint pricing before replicating them across many VPCs.

## Verify
- [ ] Task in a subnet with no NAT route starts and pulls its image.
- [ ] Flow logs show traffic to endpoint ENIs, none via NAT for ECR.

## Checked
2026-10-27. Documentation: Amazon ECR User Guide, Amazon ECR interface VPC endpoints (AWS PrivateLink), read this date. Confirmed: endpoint names com.amazonaws.region.ecr.dkr and ecr.api, S3 gateway endpoint requirement, layer bucket ARN arn:aws:s3:::prod-region-starport-layer-bucket/* and the s3:GetObject endpoint policy example, Fargate platform-version rules, CloudWatch Logs endpoint for awslogs in a VPC without an internet gateway, private DNS on ecr.dkr. Removed unconfirmed claims about sts/secretsmanager endpoints, error strings, pull-through cache egress, replication, SourceVpce and endpoint-policy condition keys.
Method: documentation only; no commands were run.
