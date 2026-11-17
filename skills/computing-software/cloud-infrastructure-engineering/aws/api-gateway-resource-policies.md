---
id: computing-software.cloud-infrastructure-engineering.aws.api-gateway-resource-policies
name: api-gateway-resource-policies
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, api-gateway, apigw-resource-policy, resource-policy, aws-sourceip, aws-sourcevpce, private-api, cross-account-api]
level: practitioner
status: docs-checked
description: "Restrict REST APIs with API Gateway resource policies: IP allow/deny, VPC endpoint conditions for private APIs, cross-account callers, evaluation with IAM auth, and redeploying."
sources: ["https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-resource-policies.html", "https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-resource-policies-create-attach.html", "https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-authorization-flow.html", "https://docs.aws.amazon.com/apigateway/latest/developerguide/limits.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# API Gateway resource policies

**Goal:** limit who can call a REST API by source IP, VPC/VPC endpoint or AWS account, at the
gateway. Resource policies are a REST API feature and work with private, edge-optimized and Regional endpoints.

## ARN format
`arn:aws:execute-api:<region>:<account>:<api-id>/<stage>/<METHOD>/<path>`; `execute-api:/*` is a
shorthand for the current API in the policy.

## IP allow list
```json
{"Version":"2012-10-17","Statement":[
 {"Effect":"Allow","Principal":"*","Action":"execute-api:Invoke","Resource":"execute-api:/*"},
 {"Effect":"Deny","Principal":"*","Action":"execute-api:Invoke","Resource":"execute-api:/*",
  "Condition":{"NotIpAddress":{"aws:SourceIp":["203.0.113.0/24","198.51.100.10/32"]}}}]}
```
## Private API reachable only from one VPC endpoint
```json
{"Effect":"Deny","Principal":"*","Action":"execute-api:Invoke","Resource":"execute-api:/*",
 "Condition":{"StringNotEquals":{"aws:SourceVpce":"vpce-0abc123"}}}
```
plus an Allow for `*`. Use `aws:SourceVpc` to allow any endpoint in a VPC. Private APIs
**require** a resource policy; until one is attached all calls fail.

## Cross-account with IAM auth
Allow `"Principal":{"AWS":"arn:aws:iam::444455556666:role/caller"}` and set the method
authorization to `AWS_IAM`; the caller also needs `execute-api:Invoke` in its own identity policy.

## Evaluation
- Same account, IAM auth: Allow in either the identity policy or the resource policy suffices
  (explicit Deny wins).
- Cross account, IAM auth: both must Allow.
- Lambda/Cognito authorizers follow the same table as IAM: same account, an Allow from either side suffices and an explicit Deny wins; with a Lambda authorizer the resource policy is also checked for explicit denials before the authorizer runs.

## Apply
```bash
aws apigateway update-rest-api --rest-api-id "$API" \
  --patch-operations 'op=replace,path=/policy,value="<JSON-escaped policy document>"'
aws apigateway create-deployment --rest-api-id "$API" --stage-name prod
```
The policy value is the JSON-escaped policy string. Updating the policy does not change runtime behaviour until you **deploy the API**.

## Gotchas
- For many CIDRs or rate rules, consider AWS WAF on the stage; the resource policy length quota is 8192 characters (increasable).

## Verify
- [ ] Call from an allowed IP/endpoint returns 200; from outside returns 403.
- [ ] Stage deployment timestamp is after the policy change.

## Checked
Date: 2026-10-24. Documentation release: Amazon API Gateway Developer Guide (awsdocs source, June 2023 snapshot).
Confirmed: `execute-api:/*` shorthand; `update-rest-api` with `/policy` and a JSON-escaped value; deployment required after a policy change; policies apply to private, edge-optimized and Regional APIs; private APIs fail until a policy is attached; `aws:SourceVpc` and `aws:SourceVpce`; same-account versus cross-account evaluation (Table A and Table B); 8192-character policy limit.
Removed as unconfirmed: the `jq` pipeline, CloudFront edge-IP behaviour, the exact 403 message text and the HTTP API remark.

Method: documentation only; no commands were run.
