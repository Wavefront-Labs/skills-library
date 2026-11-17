---
id: computing-software.cloud-infrastructure-engineering.aws.alb-authentication-oidc-cognito
name: alb-authentication-oidc-cognito
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, alb, alb-authentication, alb-oidc, alb-cognito, authenticate-oidc, x-amzn-oidc-data, sso]
level: practitioner
status: docs-checked
description: "Put login in front of apps with ALB authenticate-oidc and authenticate-cognito rules: session cookies, verifying x-amzn-oidc-data JWTs, logout and API paths."
sources: ["https://docs.aws.amazon.com/elasticloadbalancing/latest/application/listener-authenticate-users.html", "https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ALB authentication with OIDC or Cognito

**Goal:** internal tools get SSO at the load balancer, with no auth code in the app — and the
app can still trust *who* the user is.

## 1. Listener rule
```bash
aws elbv2 create-rule --listener-arn "$HTTPS_LISTENER" --priority 10 \
  --conditions Field=host-header,Values=tools.example.com \
  --actions \
   'Type=authenticate-oidc,Order=1,AuthenticateOidcConfig={Issuer=https://login.example.com,AuthorizationEndpoint=https://login.example.com/authorize,TokenEndpoint=https://login.example.com/token,UserInfoEndpoint=https://login.example.com/userinfo,ClientId=abc,ClientSecret=xyz,Scope="openid email profile",SessionTimeout=28800,OnUnauthenticatedRequest=authenticate}' \
   "Type=forward,Order=2,TargetGroupArn=$TG"
```
Cognito variant: `Type=authenticate-cognito` with `UserPoolArn`, `UserPoolClientId`,
`UserPoolDomain`. The IdP app must allow callback `https://tools.example.com/oauth2/idpresponse`.
HTTPS listener only.

## 2. What the app receives
- `x-amzn-oidc-accesstoken` (IdP access token), `x-amzn-oidc-identity` (subject),
  `x-amzn-oidc-data` (JWT of user claims **signed by the ALB**, ES256). Only `x-amzn-oidc-data` is signed;
  the other two are unsigned plaintext headers.
- **Verify the JWT** before trusting claims — anyone reaching targets directly could forge the header:
```python
kid = jwt.get_unverified_header(token)["kid"]
pub = requests.get(f"https://public-keys.auth.elb.{region}.amazonaws.com/{kid}").text
claims = jwt.decode(token, pub, algorithms=["ES256"])
assert jwt.get_unverified_header(token)["signer"] == ALB_ARN
```
Also restrict target SGs to the ALB SG only.

## 3. Session and logout
- The ALB sets a session cookie (name from `SessionCookieName`; use a unique name per rule when apps need
  independent authentication). `SessionTimeout` defaults to 7 days and can be as short as 1 second.
- A client must complete the login within 15 minutes or the ALB returns HTTP 401.
- Logout: the app sets the authentication session cookie's expiration to -1 **and** redirects to the IdP
  logout endpoint (if it has one). The logout landing page cannot sit behind a rule that requires authentication.
  Keep access-token lifetimes short so a deleted cookie cannot be reused for long.

## 4. Mixed paths
- `OnUnauthenticatedRequest`: `authenticate` (default) redirects to the IdP; `deny` returns 401 to requests with
  no authentication information; `allow` forwards without user claims.
- Put a higher-priority rule without an authenticate action for paths that must stay public (for example a health endpoint).

## Gotchas
- Change the client secret by updating the rule (`ClientSecret`, or `UseExistingClientSecret` to keep the current one).
- AJAX calls: with `deny`, calls without authentication information get 401, but a user whose authentication has expired is redirected to the IdP authorization endpoint.

## Verify
- [ ] Unauthenticated browser hit redirects to IdP; after login the app loads.
- [ ] App rejects a request with a hand-crafted `x-amzn-oidc-data` header (signature check fails).
- [ ] Logout returns to the IdP login page; the old cookie no longer grants access.

## Checked

Checked 2026-10-28 against the Application Load Balancer guide (authenticate users using an ALB) and the Elastic Load Balancing v2 service model (botocore).
- Confirmed: authenticate actions on HTTPS listeners only, `AuthenticateOidcConfig` and `AuthenticateCognitoConfig` fields, `OnUnauthenticatedRequest` values `deny`/`allow`/`authenticate`, 7-day default `SessionTimeout` (minimum 1 second), `x-amzn-oidc-*` headers with only `x-amzn-oidc-data` signed using ES256, `signer` ARN check, public key URL, `/oauth2/idpresponse` callback, 15-minute login limit, logout behaviour.
- Removed: the session cookie name and splitting behaviour, the large-claims 431 remark, the claim that health checks bypass listener rules, and the public-internet requirement for IdP endpoints.

Method: documentation only; no commands were run.
