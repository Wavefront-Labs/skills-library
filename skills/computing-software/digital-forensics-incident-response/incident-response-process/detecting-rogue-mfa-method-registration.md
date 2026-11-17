---
id: computing-software.digital-forensics-incident-response.incident-response-process.detecting-rogue-mfa-method-registration
name: detecting-rogue-mfa-method-registration
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [mfa-method-registration, business-email-compromise, account-containment, entra-id, dfir]
level: advanced
status: docs-checked
description: "After Entra ID account takeover, review audit logs for attacker-added MFA methods, then remove them with Require re-register MFA, session revocation and Graph phone cmdlets."
sources: ["https://learn.microsoft.com/en-us/entra/identity/monitoring-health/concept-audit-logs", "https://learn.microsoft.com/en-us/entra/identity/authentication/howto-mfa-userdevicesettings"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Detecting rogue MFA method registration

**Goal:** after stealing a session or password, attackers may add their own authentication method
so access survives a password reset. Find and remove those methods. Scope here is Microsoft
Entra ID, per the two cited Microsoft Learn pages.

## Detect
- Entra audit logs record every logged event: changes to applications, groups, users and
  licenses. Entries are system generated and cannot be changed or deleted, so they are reliable
  evidence of what was changed and when.
- Each entry shows date and time, the service, category and name of the activity, and status.
  Opening an entry gives a correlation ID, details of the actor and target resource, and where
  applicable old and new values of changed properties.
- In the audit log details the IP address reflects the OAuth client's IP address (the TCP peer of
  the service's endpoint), so compare it with sign-in logs rather than assuming it is the user's
  device address.
- Filter audit logs to the compromised user as target and read the activities around the first
  suspicious sign-in, looking for authentication-method changes by an unexpected actor or at an
  unexpected time. The audit activity reference lists the exact activity names; this skill does
  not assert them.
- Also check the user's current methods in the admin center (user, Authentication methods) and
  list phone methods with `Get-MgUserAuthenticationPhoneMethod -UserId <upn>`. Check for phone
  numbers the user does not recognise.
- Admins with the Authentication Administrator role can add methods for a user, including phone
  numbers, so review who performed any addition.

## Remediate (Authentication Administrator or higher)
- In the user's Authentication methods blade: **Require re-register MFA** deactivates the user's
  hardware OATH tokens and deletes phone numbers, Microsoft Authenticator apps and software OATH
  tokens; the user is asked to set up a new method at next sign-in.
- **Reset password** assigns a temporary password that must be changed at next sign-in.
- **Revoke sessions** invalidates the user's refresh tokens, forcing reauthentication.
- Delete app passwords (Multifactor authentication, Manage user settings, Delete all existing app
  passwords); non-browser apps tied to them stop working until new ones are created.
- To remove one phone method: `Remove-MgUserAuthenticationPhoneMethod -UserId <upn>
  -PhoneAuthenticationMethodId <id>`. Connect with scopes `UserAuthenticationMethod.Read.All`
  and `UserAuthenticationMethod.ReadWrite.All`.

## Gotchas
- Email may be used for self-service password reset but not for authentication, yet it still
  gives an attacker a recovery route; review it too.
- Public profile contact fields are not authentication methods and should not be used for MFA.
- Users cannot update their own user object, but they can add or change methods under My Sign-Ins
  Security info, so a stolen session can do so.

## Verify
After remediation the user has only methods they recognise (re-registered by them), sessions are
revoked, and no further method changes appear in the audit log for the account.

## Checked
Checked 2026-11-08 against the two cited Microsoft Learn pages. Removed because those pages do
not state them: specific audit activity names and the KQL query, Okta and Google Workspace event
names (Okta page not used), the Conditional Access "Register security information" user action,
Temporary Access Pass guidance, and the Authenticator-specific removal cmdlet.
Method: docs-only read of cited pages, 2026-11-08
