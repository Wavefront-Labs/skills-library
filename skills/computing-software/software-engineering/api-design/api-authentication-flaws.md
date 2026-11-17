---
id: computing-software.software-engineering.api-design.api-authentication-flaws
name: api-authentication-flaws
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, api-authentication-flaws, broken-authentication, owasp-api-top-10, credential-stuffing, token-handling, api-security]
level: practitioner
status: docs-checked
description: "Close broken authentication holes in APIs (OWASP API2:2023): login throttling, no secrets in URLs, token validation and re-authentication."
sources: ["https://owasp.org/API-Security/editions/2023/en/0xa2-broken-authentication/", "https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Broken authentication in APIs (OWASP API2:2023)

## Checklist
- Never send auth tokens, passwords or API keys in the URL; OWASP lists this as a vulnerability. Use the `Authorization` header.
- Treat "forgot / reset password" and other credential-recovery endpoints like login endpoints: same brute-force, rate-limit and lockout protection.
- Put anti-brute-force protection on `/login`, `/token` and OTP verification that is stricter than the normal API rate limit, plus lockout or captcha against attacks on one account, and weak-password checks.
- Key the failed-login counter on the account, not only the source IP, so attackers cannot spread attempts over many IP addresses (Authentication Cheat Sheet). Exponential lockout (short, doubling) is one option; make sure lockout cannot be abused to deny service to other users.
- Account for batching: a GraphQL endpoint that accepts an array of `login` mutations in one request defeats a per-request rate limit (OWASP scenario #1). Count attempts, not HTTP requests.
- Use standards (OAuth 2.0 / OIDC) from a maintained library; do not reinvent authentication, token generation or password storage. OAuth is not authentication by itself, and API keys are for authenticating API clients, not users.
- Validate token authenticity: reject unsigned or weakly signed JWTs (`{"alg":"none"}`) and check the expiration date. See the jwt-validation skill for the rest.
- Require re-authentication (current password or step-up) before sensitive operations such as changing the account email address, password or 2FA phone number. Without it, a stolen token plus an email change and password reset takes over the account (OWASP scenario #2).
- Return a generic message and similar response time for unknown user and wrong password, and the same HTTP status in both cases (Authentication Cheat Sheet).
- Prefer multi-factor authentication where possible.
- Microservices must not be reachable by other services without authentication, and must not rely on weak or predictable tokens.

## Example probe
```bash
# 200 requests, same account, should start returning 429 well before the end
for i in $(seq 1 200); do
  curl -s -o /dev/null -w "%{http_code}\n" -X POST https://api.example.test/login \
    -d '{"email":"a@example.test","password":"x'$i'"}' -H 'Content-Type: application/json'
done | sort | uniq -c
```

## Gotchas
- Throttling per IP only is defeated by rotating proxies; also key on the target account.
- Unauthenticated "forgot password" endpoints are often less protected than login.

Verify: run the probe above against a staging copy and confirm 429/lockout appears; confirm tokens sent in `?access_token=` are rejected.

## Checked
2026-11-08. Confirmed against the OWASP API Security Top 10 2023 page API2 (vulnerability list, prevention list, both scenarios) and the OWASP Authentication Cheat Sheet (login throttling, account-keyed lockout, generic errors, constant-time response, re-authentication). Removed unsupported specifics: access-token lifetimes in minutes, rotating refresh tokens with reuse detection, revoke on password change, and the exact JWT claim list (`iss`, `aud`); the rationale that URL tokens land in logs and Referer headers is not stated on these pages and was removed. The probe command was not run.
Method: documentation only; no commands were run.
