---
id: computing-software.cloud-infrastructure-engineering.aws.api-gateway-authorizers
name: api-gateway-authorizers
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, api-gateway, lambda-authorizer, cognito-authorizer, iam-authorization-apigw, jwt-authorizer, authentication, sigv4]
level: practitioner
status: docs-checked
description: "Secure API Gateway with Lambda (token/request), Cognito and JWT authorizers or IAM SigV4: choosing one, caching, policy output, context passing and 401/403 debugging."
sources: ["https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-use-lambda-authorizer.html", "https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-lambda-authorizer.html", "https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-integrate-with-cognito.html", "https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-jwt-authorizer.html", "https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-authorization-flow.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# API Gateway authorizers

**Goal:** every route authenticates callers with the cheapest mechanism that fits, and a
401/403 can be explained from logs.

## 1. Pick the mechanism
| Caller | REST API | HTTP API |
|---|---|---|
| End users with Cognito tokens | Cognito user pool authorizer | JWT authorizer (issuer = pool) |
| End users with any OIDC IdP | Lambda authorizer | JWT authorizer |
| AWS principals (services, other accounts) | `AWS_IAM` (SigV4) | `AWS_IAM` |
| API keys, custom headers, IP rules, opaque tokens | Lambda authorizer | Lambda authorizer (simple response) |

## 2. Lambda authorizer (REST, REQUEST type)
```python
def handler(event, context):
    token = event["headers"].get("authorization", "")
    claims = verify(token)                      # raise/return deny on failure
    effect = "Allow" if claims else "Deny"
    arn = event["methodArn"].split("/")[0] + "/*"   # wildcard so the cached policy covers all routes
    return {
        "principalId": claims.get("sub", "anonymous") if claims else "anonymous",
        "policyDocument": {"Version": "2012-10-17", "Statement": [
            {"Action": "execute-api:Invoke", "Effect": effect, "Resource": arn}]},
        "context": {"tenantId": claims.get("tenant", "") if claims else ""}  # strings/numbers/bools only
    }
```
- REST: cache TTL default 300 s, maximum 3600 s, 0 disables caching; keyed on identity sources (e.g. `method.request.header.Authorization`).
  A policy scoped to one `methodArn` and cached gives **403 on other routes** for the same
  token — return a wildcard resource or set TTL 0.
- Returning the error `"Unauthorized"` (documented as `callback("Unauthorized")`) gives 401; a Deny policy gives 403; any other error string gives 500.
- Backend reads `event.requestContext.authorizer.tenantId` (REST) /
  `requestContext.authorizer.lambda.tenantId` (HTTP API).
- HTTP API (payload format 2.0): enabling simple responses lets the function return `{"isAuthorized": true, "context": {...}}`; the authorizer then fully allows or denies every request matching the cached identity-source values.

## 3. Cognito / JWT
REST: `--type COGNITO_USER_POOLS --provider-arns <pool ARN>`; the ID token authorizes on identity claims;
an access token authorizes on custom scopes set as the method's `authorizationScopes`.
HTTP API JWT authorizer: `IdentitySource=$request.header.Authorization`,
`JwtConfiguration={Issuer=https://cognito-idp.<REGION>.amazonaws.com/<POOL_ID>,Audience=[<CLIENT_ID>]}`.
The JWT authorizer accepts a token whose `aud` or `client_id` claim matches one of the configured audiences.

## 4. IAM (SigV4)
Method `authorizationType=AWS_IAM`; callers need `execute-api:Invoke` on
`arn:aws:execute-api:<REGION>:<ACCOUNT_ID>:<API_ID>/<STAGE>/<METHOD>/<PATH>`. Cross-account:
add a resource policy allowing the other account's principal too.

## Gotchas
- API Gateway must be allowed to invoke the authorizer function (`aws lambda add-permission --principal apigateway.amazonaws.com`);
  failing to connect to the authorizer returns the `AUTHORIZER_CONFIGURATION_ERROR` gateway response (500).
- Authorizer function errors surface as 500, not 401; check its own logs and
  keep it fast (it runs before every uncached request).
- Resource policy + Lambda authorizer (REST): the resource policy is evaluated before the authorizer (an explicit deny stops the request) and again with the authorizer's policy; see the authorization-flow page.

## Verify
- [ ] No token → 401; valid token → 200; valid token for wrong tenant/scope → 403.
- [ ] Execution logs (REST) show `Authorizer ... Incoming identity` and the cached-policy hit on a second call.
- [ ] Cached token calling a second route still returns 200 (wildcard resource works).

## Checked
Date: 2026-10-24. Documentation release: Amazon API Gateway Developer Guide (awsdocs source, June 2023 snapshot) plus the current botocore `apigateway` and `apigatewayv2` models.
Confirmed: REST authorizer result TTL default 300 s and maximum 3600 s; Node `callback("Unauthorized")` gives 401 and other errors give 500; Deny gives 403; HTTP API simple responses and `isAuthorized`; Cognito identity vs access token and scopes; JWT `aud` or `client_id`; `AUTHORIZER_CONFIGURATION_ERROR` is a 500 gateway response; resource-policy and authorizer evaluation order.
Removed as unconfirmed: the exact exception name for a missing invoke permission and the claim that authorizer timeouts return 500.

Method: documentation only; no commands were run.
