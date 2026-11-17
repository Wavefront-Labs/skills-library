---
id: computing-software.cloud-infrastructure-engineering.aws.s3-interface-endpoints-for-on-premises-access
name: s3-interface-endpoints-for-on-premises-access
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, vpc-endpoints, s3-interface-endpoint, privatelink, hybrid-connectivity, s3]
level: advanced
status: docs-checked
description: "Reach S3 privately from on-premises over Direct Connect or VPN via S3 interface endpoints, endpoint-specific DNS names and private DNS for inbound resolvers."
sources: ["https://docs.aws.amazon.com/AmazonS3/latest/userguide/privatelink-interface-endpoints.html", "https://docs.aws.amazon.com/vpc/latest/privatelink/vpc-endpoints-s3.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# S3 interface endpoints for on-premises access

Gateway endpoints only work for traffic originating in the VPC. On-prem clients over DX/VPN need an
**interface** endpoint (ENIs with private IPs).

## 1. Create
```bash
aws ec2 create-vpc-endpoint --vpc-id vpc-0abc --vpc-endpoint-type Interface \
  --service-name com.amazonaws.<REGION>.s3 --subnet-ids subnet-a subnet-b --security-group-ids sg-s3vpce \
  --private-dns-enabled --dns-options PrivateDnsOnlyForInboundResolverEndpoint=true
```
- `PrivateDnsOnlyForInboundResolverEndpoint=true` (the default when private DNS is enabled) keeps VPC workloads on the free gateway endpoint
  while queries arriving via a Route 53 Resolver **inbound endpoint** resolve to the interface ENIs.
  Requires a gateway endpoint for S3 in the VPC.
- SG must allow 443 from on-prem CIDRs.

## 2. Client options
- With private DNS + inbound resolver: on-prem DNS forwards `s3.<REGION>.amazonaws.com` to the inbound
  endpoint IPs; clients use normal S3 URLs.
- Without private DNS: endpoint-specific names:
```bash
aws s3 ls s3://my-bucket --region <REGION> \
  --endpoint-url https://bucket.vpce-0abc123-xyz.s3.<REGION>.vpce.amazonaws.com
```
SDKs: set the endpoint URL. The S3 docs use the `bucket.` prefix for bucket operations, `accesspoint.`
for access points and `control.` for the S3 Control API, each followed by `vpce-<id>.s3.<REGION>.vpce.amazonaws.com`.

## 3. Lock the bucket to the endpoint
Bucket policy deny unless `aws:SourceVpce` equals the interface (and gateway) endpoint IDs.

## Cost
Interface endpoints are billed (see AWS PrivateLink pricing); gateway endpoints for S3 have no additional charge but cannot be used from on-premises networks, peered VPCs in other Regions or through a transit gateway. Keep VPC traffic on the gateway endpoint.

## Verify
- [ ] From on-prem, `nslookup s3.<REGION>.amazonaws.com` returns private endpoint IPs.
- [ ] Upload succeeds and CloudTrail data events show `vpcEndpointId` of the interface endpoint.

## Checked

Checked 2026-10-27 against the S3 User Guide page AWS PrivateLink for Amazon S3, the VPC PrivateLink page Gateway endpoints for Amazon S3 and the botocore ec2 model.
Confirmed: interface endpoint DNS names have the form vpce-<id>.s3.<region>.vpce.amazonaws.com and the CLI examples use bucket., accesspoint. and control. prefixes with --endpoint-url; private DNS for inbound resolver endpoints only (option name PrivateDnsOnlyForInboundResolverEndpoint, default true, requires a gateway endpoint in the VPC); on-premises DNS can forward to a Route 53 Resolver inbound endpoint; gateway endpoints have no additional charge and do not allow access from on-premises networks; create-vpc-endpoint flags --private-dns-enabled and --dns-options.

Method: documentation only; no commands were run.
