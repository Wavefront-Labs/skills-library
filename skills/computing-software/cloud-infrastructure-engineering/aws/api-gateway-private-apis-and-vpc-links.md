---
id: computing-software.cloud-infrastructure-engineering.aws.api-gateway-private-apis-and-vpc-links
name: api-gateway-private-apis-and-vpc-links
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, api-gateway, private-api, vpc-link, execute-api-endpoint, privatelink, resource-policy, nlb]
level: practitioner
status: docs-checked
description: "Build private API Gateway APIs reachable only through execute-api VPC endpoints, and reach private backends with VPC links (NLB for REST, ALB/NLB/Cloud Map for HTTP APIs)."
sources: ["https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-private-apis.html", "https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-private-api-test-invoke-url.html", "https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-private-integration.html", "https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-vpc-links.html", "https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-private.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Private APIs and VPC links

Two different problems, often confused:
- **Private API** = the *front door* is private (callers inside VPCs).
- **VPC link** = the *backend* is private (API is public or private; integration is inside a VPC).

## 1. Private REST API
1. Interface endpoint for `com.amazonaws.<REGION>.execute-api` in the consumer VPC
   (security group allows 443 from callers).
2. API endpoint type `PRIVATE` and a **resource policy** (mandatory — until one is attached, all calls to the API fail):
```json
{"Version": "2012-10-17", "Statement": [
 {"Effect": "Deny", "Principal": "*", "Action": "execute-api:Invoke", "Resource": "execute-api:/*",
  "Condition": {"StringNotEquals": {"aws:SourceVpce": ["vpce-0abc123"]}}},
 {"Effect": "Allow", "Principal": "*", "Action": "execute-api:Invoke", "Resource": "execute-api:/*"}]}
```
3. Deploy the API again after changing the policy.
Invoke URLs:
- private DNS enabled on the endpoint: `https://<API_ID>.execute-api.<REGION>.amazonaws.com/prod`
- else: `https://<API_ID>-<VPCE_ID>.execute-api.<REGION>.amazonaws.com/prod`, or the endpoint
  DNS name with a `Host: <API_ID>.execute-api.<REGION>.amazonaws.com` header, or the `x-apigw-api-id` header.

**Gotcha:** with private DNS enabled you cannot reach **public** APIs from that VPC through the API Gateway
VPC endpoint; use custom domains for those, or disable private DNS.

## 2. VPC link for REST APIs (NLB)
```bash
aws apigateway create-vpc-link --name orders-link --target-arns "$NLB_ARN"
# integration: type HTTP_PROXY, connectionType VPC_LINK, connectionId <vpclink-id>,
# uri http://internal-orders.example.internal/{proxy}
```
REST API private integrations use a Network Load Balancer owned by the same account as the API; wait for the VPC link status to be `AVAILABLE`.

## 3. VPC link for HTTP APIs
```bash
aws apigatewayv2 create-vpc-link --name orders --subnet-ids subnet-a subnet-b --security-group-ids sg-123
# integration: IntegrationType HTTP_PROXY, ConnectionType VPC_LINK, IntegrationUri = ALB/NLB listener ARN or Cloud Map service ARN
```
HTTP API VPC links are immutable (subnets and security groups cannot be changed). The load balancer or Cloud Map service, VPC link and API must be in the same account.

## Gotchas
- Private APIs have no public endpoint; testing from your laptop needs VPN/bastion/SSM port forwarding.
- Cross-account callers: allow their `aws:SourceVpce` (or `aws:SourceVpc`) in the policy.
- The integration timeout quota still applies to private integrations.

## Verify
- [ ] From inside the VPC, `curl https://<API_ID>.execute-api.<REGION>.amazonaws.com/prod/health` returns 200; from the internet it fails DNS/403.
- [ ] Request from a different VPC endpoint is denied (403 from resource policy).
- [ ] VPC link status `AVAILABLE` and backend access logs show requests from the link's ENIs.

## Checked
Date: 2026-10-24. Documentation release: Amazon API Gateway Developer Guide (awsdocs source, June 2023 snapshot).
Confirmed: private API needs an execute-api interface endpoint and a resource policy (calls fail until attached) with `aws:SourceVpce`/`aws:SourceVpc` conditions; invoke URL forms including `x-apigw-api-id` and the `Host` header; private DNS cannot reach public APIs via the endpoint; REST private integrations use an NLB in the same account; HTTP API VPC links accept ALB, NLB or Cloud Map and are immutable.
Removed as unconfirmed (newer than the snapshot or undocumented): private custom domains shared through RAM, REST VPC link v2 targeting ALBs, NLB fronting an ALB, link security-group rules.

Method: documentation only; no commands were run.
