---
id: computing-software.cloud-infrastructure-engineering.aws.appsync-private-apis-and-custom-domains
name: appsync-private-apis-and-custom-domains
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, appsync, appsync-private-api, appsync-custom-domain, interface-endpoint, graphql, privatelink]
level: practitioner
status: docs-checked
description: "Expose AppSync only inside VPCs with private APIs and interface endpoints, or publicly on your own hostname with custom domain names and an ACM certificate."
sources: ["https://docs.aws.amazon.com/appsync/latest/devguide/using-private-apis.html", "https://docs.aws.amazon.com/appsync/latest/devguide/custom-domain-name.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AppSync private APIs and custom domains

## Private APIs
- Visibility is chosen at creation: `--visibility PRIVATE`; it cannot be changed afterwards.
```bash
aws appsync create-graphql-api --name internal-orders --authentication-type AWS_IAM --visibility PRIVATE
aws ec2 create-vpc-endpoint --vpc-id "$VPC" --vpc-endpoint-type Interface \
  --service-name com.amazonaws.eu-west-1.appsync-api --subnet-ids $SUBNETS \
  --security-group-ids "$SG" --private-dns-enabled
```
- Two endpoint services exist: `com.amazonaws.<region>.appsync-api` (data plane: GraphQL and real-time
  access to private APIs, required) and `com.amazonaws.<region>.appsync` (control plane: managing APIs
  from the VPC). The private API and the VPC must be in the same account and Region.
- With private DNS (the VPC needs `enableDnsHostnames` and `enableDnsSupport`), clients call the normal
  `https://<api-id>.appsync-api.<region>.amazonaws.com/graphql` and resolve to the endpoint ENIs; without
  private DNS use the endpoint-specific `vpce` hostname plus the `Host` header (or `x-appsync-domain`) naming the API.
- Real-time subscriptions use the `appsync-realtime-api` hostname over the same data plane endpoint.
- The endpoint security group must allow HTTPS from clients.
- Restrict who can create private APIs, or force them, with the IAM condition key `appsync:Visibility`
  (value `PRIVATE`). AWS recommends IAM authorization for callers inside the VPC.
- A private DNS endpoint also catches calls to public AppSync APIs on their generated URL from that VPC, so give
  public APIs a custom domain name to call them from the VPC. The console query editor reaches a private API only
  if your browser can route to the VPC.

## Custom domain names (public APIs)
```bash
aws appsync create-domain-name --domain-name api.example.com \
  --certificate-arn arn:aws:acm:us-east-1:111122223333:certificate/...
aws appsync associate-api --domain-name api.example.com --api-id "$API"
aws appsync get-domain-name --domain-name api.example.com --query 'domainNameConfig.appsyncDomainName'
```
- The certificate must be a public or imported ACM certificate in **us-east-1** (creating a custom domain
  sets up a CloudFront distribution using SNI); wildcard names such as `*.example.com` need a wildcard certificate.
- The caller needs `cloudfront:updateDistribution` and `acm:DescribeCertificate` on the certificate.
- Create a DNS record (CNAME, or a Route 53 alias) from `api.example.com` to the returned `appsyncDomainName`;
  without it requests cannot reach AppSync. The domain can be a subdomain or the zone apex.
- Endpoints become `https://api.example.com/graphql` and `wss://api.example.com/graphql/realtime`.
- Only TLS 1.2 and TLS 1.3 are supported.

## Verify
- [ ] From inside the VPC a query succeeds; from outside the VPC the private API is unreachable.
- [ ] `curl https://api.example.com/graphql` with auth returns data; the certificate matches.

## Checked

2026-10-27, AWS documentation (current release as read on that date). AWS AppSync Developer Guide private APIs and custom domain name pages; botocore appsync 2017-07-25 model (visibility GLOBAL/PRIVATE, create-domain-name, associate-api). Fixed: two PrivateLink services exist, appsync-api (data plane, required for private APIs) and appsync (control plane); private DNS endpoints intercept calls to public APIs on generated URLs, so public APIs need a custom domain name; the ACM certificate may be public or imported and must be in us-east-1; custom domains support only TLS 1.2 and 1.3 and wildcard names. Confirmed: visibility set only at creation, same account and Region, appsync:Visibility condition key, Host or x-appsync-domain header with vpce hostnames, CloudFront-backed custom domain, graphql/realtime URL forms, required IAM actions. Removed unsourced claims on Route 53 Resolver inbound endpoints, propagation time, WAF and one-API-per-domain blue/green swaps.
Method: documentation only; no commands were run.
