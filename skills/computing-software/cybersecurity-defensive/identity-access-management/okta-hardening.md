---
id: computing-software.cybersecurity-defensive.identity-access-management.okta-hardening
name: okta-hardening
category: computing-software
field: cybersecurity-defensive
product: identity-access-management
tags: [okta-hardening, okta, identity-provider-hardening, admin-session-binding, phishing-resistant-mfa, okta-system-log, cloud-identity]
level: advanced
status: draft
description: "Harden an Okta org: admin role scoping, phishing-resistant MFA for admins, session policies and admin session ASN binding, API token hygiene, HAR/support access and log streaming."
sources: ["https://help.okta.com/en-us/content/topics/security/security-best-practices.htm", "https://sec.okta.com/articles/2023/11/unauthorized-access-oktas-support-case-management-system-root-cause", "https://developer.okta.com/docs/reference/api/system-log/", "https://www.cisa.gov/resources-tools/resources/scuba-okta"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Okta org security hardening

## Admin access
- Least-privilege admin roles (custom roles with resource sets) instead of Super Admin; 2-4 Super Admins max, dedicated admin accounts.
- Admin Console app sign-on policy: phishing-resistant authenticator (FIDO2/Okta FastPass with phishing resistance) required, managed device, short session.
- **Admin session ASN binding** and IP binding (Settings -> Security) so a stolen admin session cookie used from another network is revoked.
- Protected actions (re-authentication for sensitive admin operations) enabled.

## End-user policies
- Global session policy: MFA required, session lifetime limited, no persistent cookies on unmanaged devices.
- Authentication policies per app; high-risk apps require phishing-resistant authenticators and device assurance.
- Disable weak authenticators (SMS/voice, security question) or restrict to recovery with additional factors.
- ThreatInsight in "log and block" mode; behaviour detection rules (new country, new device) feeding policies.
- Block legacy authentication protocols to O365 via Okta app sign-on policy.

## Tokens and integrations
- API tokens inherit the creating admin's permissions and are long-lived: use OAuth 2.0 service apps with scoped grants instead; inventory and revoke unused tokens; network restrictions on tokens.
- Review third-party apps with Okta API scopes.

## Support and HAR files
- Restrict Okta support access (time-boxed "Give access to Okta Support"), sanitise HAR files before upload (2023 support system breach exposed session tokens from HARs).

## Logging
- Stream the System Log to the SIEM (log streaming to Splunk/EventBridge, or API polling); retention in Okta is 90 days.
- Detections: `user.session.access_admin_app` from new IPs, `system.api_token.create`, `policy.lifecycle.update`, `user.mfa.factor.deactivate`, `application.lifecycle.update`, admin role grants (`user.account.privilege.grant`).

## Verify
- [ ] ScubaGear-style review (CISA SCuBA Okta baseline) with findings closed.
- [ ] All admins use phishing-resistant authenticators.
- [ ] System Log in SIEM with detections firing on test events.
