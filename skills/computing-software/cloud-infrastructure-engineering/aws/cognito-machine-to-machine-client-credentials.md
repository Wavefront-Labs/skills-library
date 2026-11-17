---
id: computing-software.cloud-infrastructure-engineering.aws.cognito-machine-to-machine-client-credentials
name: cognito-machine-to-machine-client-credentials
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, cognito, client-credentials, resource-server, custom-scopes, m2m-auth, oauth2]
level: practitioner
status: docs-checked
description: "Use Cognito for service-to-service auth: resource servers and custom scopes, client credentials grant, token endpoint calls, API Gateway scope checks, caching and cost."
sources: ["https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-define-resource-servers.html", "https://docs.aws.amazon.com/cognito/latest/developerguide/token-endpoint.html", "https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-pre-token-generation.html", "https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-integrate-with-cognito.html", "https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-jwt-authorizer.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cognito machine-to-machine (client credentials)

## 1. Resource server and scopes
```bash
aws cognito-idp create-resource-server --user-pool-id eu-west-1_ABC \
  --identifier https://api.example.com --name orders-api \
  --scopes ScopeName=orders.read,ScopeDescription="read orders" ScopeName=orders.write,ScopeDescription="write orders"
```
Scopes appear in tokens as `https://api.example.com/orders.read`.

## 2. Confidential app client for a service
```bash
aws cognito-idp create-user-pool-client --user-pool-id eu-west-1_ABC --client-name billing-svc \
  --generate-secret --allowed-o-auth-flows client_credentials \
  --allowed-o-auth-scopes https://api.example.com/orders.read \
  --allowed-o-auth-flows-user-pool-client --access-token-validity 60 \
  --token-validity-units AccessToken=minutes
```
The token endpoint needs a user pool **domain** (Cognito prefix domain or custom domain).
Without a domain, create the client with `--explicit-auth-flows ALLOW_CLIENT_TOKEN_AUTH` (this
flow is mutually exclusive with user flows) and call `aws cognito-idp get-client-token`
(`GetClientToken`: client ID, an active secret, optional scopes; no IAM authorization).
One client per calling service so scopes are per service. Store the secret in Secrets Manager.

## 3. Getting a token
```bash
curl -s -X POST https://auth.example.com/oauth2/token \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -u "$CLIENT_ID:$CLIENT_SECRET" \
  -d 'grant_type=client_credentials&scope=https://api.example.com/orders.read'
```
Response: `access_token`, `expires_in`, `token_type: Bearer`. No ID or refresh token in
this grant. Cache the token until shortly before expiry: M2M billing reflects active M2M app
clients and total token-request volume, and requests also count toward request-rate quotas.

## 4. Protecting the API
- **API Gateway REST**: Cognito user pool authorizer with **authorization scopes** on the
  method (`orders.read`); requests must send the access token (not ID token) in the
  configured header.
- **API Gateway HTTP API**: JWT authorizer with issuer
  `https://cognito-idp.eu-west-1.amazonaws.com/eu-west-1_ABC` and audience = the app
  client ID(s); route `AuthorizationScopes`.
- **Self-validation**: verify JWT signature with the pool's JWKS
  (`/.well-known/jwks.json`), `iss`, `token_use = access`, `client_id` claim (no `aud` in
  access tokens), `exp`, and required `scope`. Use `aws-jwt-verify`.
- **ALB** authentication is for interactive users, not M2M.

## 5. Customising M2M tokens
Pre token generation Lambda trigger (V3_0 event, Essentials or Plus feature plan) can add claims
or scopes to client credentials tokens, e.g. a `tenant` claim per client. Pass extra context with
the `aws_client_metadata` form parameter on the token request.

## Gotchas
- Using a user-facing client for M2M mixes concerns; keep separate clients.
- Rotating a client secret: an app client can have up to two active secrets, so add the new
  secret, deploy it, then remove the old one.
- Keep access-token lifetimes short and cache tokens in the caller.

## Verify
- [ ] Token request with the service's credentials returns a token containing only its allowed scopes.
- [ ] API call with a token lacking the method's scope returns 401/403.
- [ ] Clients cache tokens (token endpoint request rate low and stable).

## Checked

Checked 2026-10-27 against the Amazon Cognito Developer Guide (scopes, M2M and resource servers; token endpoint; pre token generation), the API Gateway Developer Guide and the aws-cli create-user-pool-client reference.
- Corrected: a user pool domain is only needed for the token endpoint; the domainless `GetClientToken` operation with the `ALLOW_CLIENT_TOKEN_AUTH` flow was added to the skill.
- Corrected: an app client can hold two active secrets (rotation without a new client); V3_0 pre token generation event (Essentials/Plus) customizes M2M tokens.
- Confirmed: client_secret_basic and form-encoded token requests, M2M billing basis (active M2M app clients and token requests), REST authorizer scopes and HTTP API JWT authorizer issuer/audience (client_id) behaviour.
- Removed: unsupported claim that client-credentials tokens cannot be revoked, and the unconfirmed token-endpoint rate statement.

Method: documentation only; no commands were run.
