---
id: computing-software.it-support-helpdesk.desktop-support.entra-sign-in-errors-and-saas-sso
name: entra-sign-in-errors-and-saas-sso
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, aadsts-errors, risky-users, saas-sso-troubleshooting, entra-sign-in-logs, sso, conditional-access]
level: practitioner
status: docs-checked
description: "Diagnose Entra sign-in failures from AADSTS codes, remediate risky users with ID Protection, and troubleshoot SAML single sign-on to SaaS apps."
sources:
  - "https://learn.microsoft.com/en-us/entra/identity-platform/reference-error-codes"
  - "https://learn.microsoft.com/en-us/entra/id-protection/howto-identity-protection-remediate-unblock"
  - "https://learn.microsoft.com/en-us/entra/identity/enterprise-apps/debug-saml-sso-issues"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# entra-sign-in-errors-and-saas-sso

## Common AADSTS codes
| Code | Name and meaning | Action |
|---|---|---|
| 50126 | InvalidUserNameOrPassword: wrong credentials; some are expected from user mistakes | Normal noise unless repeated |
| 50053 | IdsLocked: account locked after too many sign-in attempts with bad credentials | See Remediate risks and unblock users |
| 50057 | UserDisabled: account disabled | Admin can re-enable |
| 50055 | InvalidPasswordExpiredPassword: password expired | User offered a reset, or admin resets it |
| 50144 | User's on-premises Active Directory password expired | New password or self-service reset |
| 50076 | UserStrongAuthClientAuthNRequired: MFA required (Conditional Access, per-user enforcement or new location) | Retry with MFA |
| 50079 | UserStrongAuthEnrollmentRequired: user must register security info (or get the MFA claim from a federated IdP) | Register MFA |
| 53003 | BlockedByConditionalAccess: policy does not allow token issuance | Review the applied Conditional Access policy |
| 530032 | Blocked by a tenant-level security policy | Check tenant security policies |
| 700016 | Application not found in directory or tenant; not installed or consented, wrong identifier or wrong tenant | Check app id and tenant |
| 65001 | DelegationDoesNotExist: user or admin has not consented to the app | Interactive consent request |
| 50105 | EntitlementGrantsNotFound: user not assigned to a role for the app | Assign the user to the app |
| 50011 | InvalidReplyTo: reply address missing or not matching those configured for the app | Add the reply address to the app registration |

## Risky users (Entra ID Protection)
- Needs Entra ID P2 (or Entra Suite) for full features. Roles: User Administrator to reset passwords, Security Operator to dismiss user risk, Security Administrator for risk-based policies.
- Risk-based Conditional Access lets users self-remediate: sign-in risk clears when they pass MFA; user risk clears with a secure password change (MFA first, then change; not the SSPR flow). Users who cannot do MFA are blocked and need admin help.
- Admin options: generate a temporary password (Protection > Identity Protection > Risky users, or Users > All users, Reset password; user must change it at next sign-in), require a password change, dismiss risk, confirm compromised and secure the account, unblock.
- Hybrid users' on-premises changes need password hash sync and the Allow on-premises password change to reset user risk setting.

## SAML SSO troubleshooting
- Test: Entra ID > Enterprise apps > the app > Single sign-on > SAML > Test single sign-on (at least Cloud Application Administrator). If Test is greyed out, fill and save the required Basic SAML Configuration attributes first.
- The My Apps Secure Sign-in Extension (Chrome, Edge) captures the SAML request and response; without it use a tool such as Fiddler. A Fix it button appears when the cause is an Entra misconfiguration.
- Without the extension: copy the error message (it has CorrelationID and Timestamp, needed for support cases), paste it into Get resolution guidance on the Test page.
- Check the SAML request: destination matches the Entra SAML Single Sign-on Service URL; issuer equals the identifier configured for the app; AssertionConsumerServiceURL is where the app expects the token.
- Error on the app page after sign-in means Entra issued a token the app rejected. In the SAML response check the NameID value and format, the claims issued, and the signing certificate. Then ask the app vendor what is missing.

## Verify
The next attempt succeeds, any risk is remediated or dismissed, and Test single sign-on works for the app.

## Checked
Date: 2026-11-09. Confirmed in the three Microsoft Learn pages (the 50053 row only up to its first cause, as the page text was cut). Removed as unconfirmed: the sign-in log tab walkthrough, the error lookup page, Revoke-MgUserSignInSession and inbox-rule steps, certificate expiry as classic outage, SCIM and "user does not exist in the app", OIDC notes and SP vs IdP initiated notes.
Method: docs-checked 2026-11-09 against the three Microsoft Learn pages listed in sources, downloaded and read (error codes page by targeted search).
