---
id: computing-software.cloud-infrastructure-engineering.aws.cognito-threat-protection-waf-and-quotas
name: cognito-threat-protection-waf-and-quotas
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, cognito, threat-protection, cognito-waf, adaptive-authentication, compromised-credentials, cognito-quotas, toomanyrequestsexception]
level: practitioner
status: docs-checked
description: "Harden Cognito user pools: threat protection (adaptive auth, compromised credentials) in audit then enforce, AWS WAF on the pool, and request-rate quotas with retry handling."
sources: ["https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pool-settings-threat-protection.html", "https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-waf.html", "https://docs.aws.amazon.com/cognito/latest/developerguide/quotas.html", "https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-sign-in-feature-plans.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cognito threat protection, WAF and quotas

## Threat protection
Formerly "advanced security features"; requires the **Plus** feature plan on the user pool.
- **Adaptive authentication:** risk score (low/medium/high) per sign-in from device, IP and
  behaviour; per level choose allow, optional MFA, required MFA or block.
- **Compromised credentials:** compares credentials with leaked-credential lists and commonly
  guessed passwords; for sign-in, sign-up and password change the action is block or allow
  (`BLOCK`/`NO_ACTION`). It does not detect compromised credentials in SRP or custom authentication.
- Adaptive authentication works with `USER_PASSWORD_AUTH`, `ADMIN_USER_PASSWORD_AUTH` and
  `USER_SRP_AUTH`; threat protection cannot be used with federated sign-in.
- Per-risk-level actions (`LowAction`, `MediumAction`, `HighAction`): `NO_ACTION`, `MFA_IF_CONFIGURED`,
  `MFA_REQUIRED`, `BLOCK`. IP "always block" and "always allow" lists use CIDR notation.
- Modes: `AUDIT` (log risk only) then `ENFORCED`.
```bash
aws cognito-idp set-risk-configuration --user-pool-id "$POOL" \
  --compromised-credentials-risk-configuration 'Actions={EventAction=BLOCK}' \
  --account-takeover-risk-configuration file://ato.json
aws cognito-idp admin-list-user-auth-events --user-pool-id "$POOL" --username alice
```
- Run AUDIT for two weeks or more (the documented best practice), review risk events (console or
  `admin-list-user-auth-events`; Plus can push activity logs to an external AWS service), then enforce.
  Give feedback on false positives with `admin-update-auth-event-feedback` (`Valid`/`Invalid`).
- Client apps should send device data (`UserContextData.EncodedData`) via the SDK so scores are accurate;
  server-side flows pass `UserContextData.IpAddress`.

## AWS WAF on the user pool
```bash
aws wafv2 associate-web-acl --web-acl-arn "$ACL" \
  --resource-arn arn:aws:cognito-idp:<REGION>:<ACCOUNT_ID>:userpool/<POOL_ID>
```
- Protects the classic hosted UI, managed login and the user pool API service endpoints; one web ACL per user pool.
- Body-based rules work only for requests to the user pools API (managed login and hosted UI
  requests do not forward the body), and rules cannot match PII such as usernames in the body.
- A newly created web ACL can take seconds to minutes to propagate; associating early returns `WAFUnavailableEntityException`.
- Requests blocked by AWS WAF do not count toward the user pool request-rate quotas.
- Use rate-based rules per IP, AWS managed IP reputation lists and geo rules.

## Quotas
- API calls fall into request-rate **categories** (for example UserAuthentication and UserCreation; the
  Cognito quotas page lists every category and its operations), each with a per-second quota that
  applies per Region. Many are adjustable; check Service Quotas for current values.
- Exceeding gives `TooManyRequestsException`: retry with exponential backoff and jitter.
- Quotas apply per category, so a bulk admin loop can throttle other operations in the same category; throttle it and run it off-peak.
- Per-pool resource quotas (app clients, groups, identity providers) are separate.

## Gotchas
- Threat protection requires the Plus feature plan; check the Cognito pricing page for current cost.
- WAF in COUNT first; a too-tight rate rule locks out offices behind one NAT IP.
- Blocked requests from "always block" IPs still count toward the request-rate quotas, and threat protection does not rate-limit high-volume traffic.

## Verify
- [ ] Risk events visible in AUDIT; a test sign-in from a new country/device scores higher.
- [ ] Known breached password is rejected after enabling compromised-credentials BLOCK.
- [ ] WAF sampled requests show the user pool traffic; load test respects quotas without errors.

## Checked

Checked 2026-10-27 against the Amazon Cognito Developer Guide (threat protection, AWS WAF, quotas, feature plans) and the botocore cognito-idp model.
- Confirmed: Plus plan requirement, AUDIT then ENFORCED with two weeks or more of audit, risk actions (NO_ACTION, MFA_IF_CONFIGURED, MFA_REQUIRED, BLOCK), compromised-credentials actions (BLOCK, NO_ACTION), `admin-update-auth-event-feedback` values (Valid/Invalid), `UserContextData.IpAddress`.
- Added from the docs: no compromised-credential detection for SRP or custom auth, no threat protection for federated sign-in, one web ACL per pool, body rules only for the user pools API, blocked requests do not count toward quotas.
- Removed: `X-Amz-Target` matching claim, per-MAU price comparison, and the log-export destinations that the plan table does not name.

Method: documentation only; no commands were run.
