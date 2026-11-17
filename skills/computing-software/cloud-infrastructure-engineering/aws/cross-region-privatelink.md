---
id: computing-software.cloud-infrastructure-engineering.aws.cross-region-privatelink
name: cross-region-privatelink
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, privatelink, cross-region-privatelink, private-dns-verification, endpoint-service, inter-region, vpc-peering]
level: practitioner
status: docs-checked
description: "Consume PrivateLink services across regions: native cross-region endpoint services (supported regions), private DNS verification, and the older inter-region peering workaround."
sources: ["https://docs.aws.amazon.com/vpc/latest/privatelink/privatelink-share-your-services.html", "https://docs.aws.amazon.com/vpc/latest/privatelink/manage-dns-names.html", "https://aws.amazon.com/blogs/networking-and-content-delivery/introducing-cross-region-connectivity-for-aws-privatelink/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cross-region PrivateLink

**Goal:** a consumer VPC in region B privately reaches an endpoint service hosted in region A.

## 1. Native cross-region (provider enables regions)
Announced on 11 December 2024: an endpoint service can accept endpoints from other regions. Only NLB-based services
can enable cross-region access; the announcement said AWS services and Marketplace services were not supported at
that time.
```bash
aws ec2 modify-vpc-endpoint-service-configuration --service-id vpce-svc-123 \
  --add-supported-regions eu-west-1 us-west-2
```
Consumer in eu-west-1:
```bash
aws ec2 create-vpc-endpoint --region eu-west-1 --vpc-endpoint-type Interface \
  --service-name com.amazonaws.vpce.us-east-1.vpce-svc-123 --service-region us-east-1 \
  --vpc-id vpc-eu --subnet-ids subnet-1 subnet-2 --security-group-ids sg-1
```
- Cross-region actions are gated behind the permission-only IAM action `vpce:AllowMultiRegion`; without it the
  cross-region calls fail.
- IAM condition keys: `ec2:VpceMultiRegion` (boolean: service has cross-region enabled, or endpoint connects to such a
  service) and `ec2:VpceServiceRegion` (limit which remote service regions consumers may use).
- Cross-region connectivity does not require AZ alignment between provider and consumer, unlike in-region PrivateLink.
- The consumer endpoint gets a regional DNS name plus one DNS name per endpoint AZ.

## 2. Private DNS verification
For consumers to use your friendly name (`api.example.com`) with private DNS, the provider verifies domain ownership:
add the TXT record from
`describe-vpc-endpoint-service-configurations --query 'ServiceConfigurations[*].PrivateDnsNameConfiguration'`
to public DNS and run `start-vpc-endpoint-service-private-dns-verification`. The private DNS name is ready for
consumers when the verification status is `verified`; if it later changes, new connection requests are denied but
existing connections are not affected. A subdomain added later must be verified (or its parent domain).

## 3. Legacy pattern (before native support)
Consumers needed inter-region VPC peering or Transit Gateway peering to reach an endpoint in the service's region.
Prefer native cross-region where the service is eligible.

## Verify
- [ ] `aws ec2 describe-vpc-endpoint-services --service-names com.amazonaws.vpce.us-east-1.vpce-svc-123 --service-regions us-east-1` from region B lists the service.
- [ ] Consumer endpoint `Available`; a request over it succeeds.
- [ ] Private DNS verification shows `verified`.

## Checked

2026-10-28. Confirmed against the AWS Networking blog post "Introducing cross-region connectivity for AWS PrivateLink" (11 December 2024: NLB-based services only, vpce:AllowMultiRegion, ec2:VpceMultiRegion and ec2:VpceServiceRegion keys, no AZ alignment, legacy peering), the PrivateLink User Guide DNS-name page (verification status, subdomains), and the botocore ec2 model (AddSupportedRegions, ServiceRegion, ServiceRegions).
Removed or corrected: the "provider NLB must be in AZs the consumer can map to" gotcha (the blog says no AZ alignment is needed), the inter-region data transfer charge line, the claim that some AWS-managed services support cross-region endpoints, the private-hosted-zone transit-VPC details, Route 53 failover advice, and "endpoint policies and SG rules work the same".
Method: documentation only; no commands were run.
