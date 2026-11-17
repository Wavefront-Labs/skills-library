---
id: computing-software.cloud-infrastructure-engineering.aws.interface-endpoint-dns-and-connectivity-troubleshooting
name: interface-endpoint-dns-and-connectivity-troubleshooting
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, vpc-endpoints, privatelink, endpoint-troubleshooting, endpoint-dns-resolution, private-dns, interface-endpoint]
level: practitioner
status: draft
description: "Debug interface VPC endpoints: private DNS not resolving, traffic still going via NAT, SG/policy denials, AZ coverage gaps, and on-prem or cross-VPC resolution."
sources: ["https://docs.aws.amazon.com/vpc/latest/privatelink/privatelink-troubleshoot.html", "https://docs.aws.amazon.com/vpc/latest/privatelink/privatelink-access-aws-services.html", "https://docs.aws.amazon.com/vpc/latest/privatelink/vpc-endpoints-access.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Interface endpoint troubleshooting

## 1. Is traffic actually using the endpoint?
```bash
dig +short sqs.eu-west-1.amazonaws.com
```
- Private IPs from your subnets = private DNS is working.
- Public AWS IPs = private DNS off, or the resolver is not the VPC resolver, or the
  query comes from a VPC that does not have the endpoint.
Flow logs on the endpoint ENIs (their description is "VPC Endpoint Interface vpce-...")
show whether traffic arrives.

## 2. Private DNS not resolving
| Cause | Check / fix |
|---|---|
| `PrivateDnsEnabled` false | `aws ec2 describe-vpc-endpoints --vpc-endpoint-ids vpce-... --query 'VpcEndpoints[].PrivateDnsEnabled'`; modify with `--private-dns-enabled` |
| VPC lacks `enableDnsSupport`/`enableDnsHostnames` | both must be true for private DNS |
| Instance uses a custom resolver (AD DNS, on-prem) | that resolver must forward `amazonaws.com` (or the service names) to the VPC resolver via Route 53 Resolver inbound endpoint |
| Query from a different VPC (spoke) | private DNS works only in the endpoint's VPC; for central endpoints create a private hosted zone per service name associated with spokes, or use Route 53 Profiles |
| Conflicting private hosted zone | a PHZ for `amazonaws.com` or the service name in the VPC overrides the endpoint's zone |
| Only regional name works | some SDKs use dual-stack or FIPS hostnames (`sqs.eu-west-1.api.aws`, `*-fips`), which need their own endpoints or DNS records |

## 3. Resolves privately but connections fail
- **Endpoint security group** must allow inbound 443 from the client CIDRs/SGs. The
  default is the VPC default SG, which often allows only itself.
- **Endpoint policy** denies the action or resource: error is `AccessDenied ... no VPC
  endpoint policy allows` (or explicit deny). Check with `describe-vpc-endpoints
  --query 'VpcEndpoints[].PolicyDocument'`.
- **Bucket/key/queue resource policies** with `aws:SourceVpce` or `aws:SourceVpc`
  conditions referencing a different endpoint ID.
- **AZ coverage**: the endpoint has ENIs only in the subnets you chose. A client in an AZ
  without an endpoint ENI still works (DNS returns all ENIs) but crosses AZs; if the
  service does not support that AZ at all, choose subnets in supported AZs
  (`describe-vpc-endpoint-services --service-names ... --query
  'ServiceDetails[].AvailabilityZones'`).
- **NACLs** on the endpoint subnets must allow 443 in and ephemeral out.
- **Gateway vs interface for S3**: with both, S3 traffic uses the gateway endpoint unless
  the client targets the interface endpoint DNS name (`bucket.vpce-...s3...`). When you
  enable private DNS on an S3 interface endpoint alongside a gateway endpoint, tick
  "Enable private DNS only for inbound endpoint" so in-VPC traffic keeps using the free
  gateway endpoint while on-prem clients use the interface endpoint.

## 4. On-premises clients
On-prem reaches interface endpoints over VPN/DX. DNS: on-prem resolvers conditionally
forward the service names to a Route 53 Resolver **inbound endpoint** in the VPC.
Without that, on-prem resolves public IPs and goes over the internet.

## 5. Quick isolation test from an instance
```bash
nslookup ssm.eu-west-1.amazonaws.com
curl -sv --max-time 5 https://ssm.eu-west-1.amazonaws.com/ -o /dev/null 2>&1 | grep -E 'Connected|SSL|HTTP/'
aws sts get-caller-identity --endpoint-url https://sts.eu-west-1.amazonaws.com --region eu-west-1
```
A TCP connect that times out points at SG/NACL; a TLS or HTTP 403 points at policy.

## Gotchas
- STS global endpoint (`sts.amazonaws.com`) does not use the regional STS interface
  endpoint; configure SDKs for regional STS.
- SSM Session Manager needs `ssm`, `ssmmessages` and `ec2messages` endpoints (plus `s3`,
  `logs`, `kms` if those features are used).
- ECR pulls need `ecr.api`, `ecr.dkr` and the S3 gateway endpoint (layers are in S3).

## Verify
- [ ] `dig` returns endpoint private IPs from every client VPC that should use it.
- [ ] NAT gateway `BytesOutToDestination` drops for that service after rollout.
- [ ] A test API call succeeds; a call violating the endpoint policy is denied with the endpoint-policy message.
