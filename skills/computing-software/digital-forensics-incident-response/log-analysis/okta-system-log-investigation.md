---
id: computing-software.digital-forensics-incident-response.log-analysis.okta-system-log-investigation
name: okta-system-log-investigation
category: computing-software
field: digital-forensics-incident-response
product: log-analysis
tags: [okta-system-log, okta, identity-provider, mfa-fatigue, session-hijacking, sso, cloud-identity, dfir]
level: practitioner
status: draft
description: "Investigate Okta System Log events for account takeover, MFA fatigue, admin abuse and session hijacking: key eventTypes, fields, API export and queries."
sources: ["https://developer.okta.com/docs/reference/api/system-log/", "https://developer.okta.com/docs/reference/api/event-types/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Okta System Log investigation

**Goal:** scope identity compromise in an Okta tenant, since Okta access often means access to
every federated application.

## Getting the data
- Admin Console > Reports > System Log (search, export CSV). Retention is **90 days**: export
  early or stream to the SIEM (Log Streaming to AWS EventBridge/Splunk, or SIEM integrations).
- API: `GET /api/v1/logs?since=2026-09-01T00:00:00Z&until=...&filter=actor.alternateId eq "user@corp.com"`
  with an API token (SSWS) or OAuth app; paginate with the `Link: rel="next"` header.

## Important fields
`eventType`, `displayMessage`, `outcome.result` (SUCCESS/FAILURE/DENY/CHALLENGE) and
`outcome.reason`, `actor` (who), `target[]` (what), `client.ipAddress`, `client.userAgent`,
`client.geographicalContext`, `securityContext` (ASN, ISP, `isProxy`),
`authenticationContext.externalSessionId` (session ID: track a session across events),
`debugContext.debugData` (`behaviors` like New Geo-Location/New Device, `risk`,
`threatSuspected`, `requestUri`, `dtHash` device token).

## Event types to know
| Activity | eventType |
|---|---|
| Sign-in / session | `user.session.start`, `user.authentication.sso`, `user.authentication.verify`, `user.session.end` |
| MFA | `user.authentication.auth_via_mfa`, `system.push.send_factor_verify_push`, `user.mfa.okta_verify.deny_push`, `user.mfa.factor.activate`, `user.mfa.factor.deactivate`, `user.mfa.factor.reset_all` |
| Password | `user.account.reset_password`, `user.account.update_password` |
| Admin | `user.account.privilege.grant`, `group.user_membership.add`, `policy.lifecycle.update`, `policy.rule.update`, `system.api_token.create` |
| Support access | `user.session.impersonation.initiate` / `.grant` (Okta support impersonation) |
| Identity providers | `system.idp.lifecycle.create` (new IdP: federation backdoor) |
| Threats | `security.threat.detected`, `user.account.lock` |

## Investigation patterns
- **MFA fatigue:** many `system.push.send_factor_verify_push` with deny/timeout outcomes, then
  a success, often from a new geo/ASN.
- **Session hijack (stolen cookie):** activity under an existing `externalSessionId` from a new
  IP/user-agent without a corresponding `user.session.start`.
- **Help-desk social engineering:** factor reset (`user.mfa.factor.reset_all`) by an admin
  followed by enrolment of a new factor and sign-in from a new device.
- **Persistence:** new admin roles, API tokens, new IdP, policy changes weakening MFA, new
  OAuth app grants.
- Pivot to app access: `user.authentication.sso` targets show which applications were opened.

## Containment pointers
Clear user sessions, reset factors and password, revoke API tokens, review admin role
assignments and IdP/policy changes over the whole incident window.

## Self-check
You have a per-session timeline (by externalSessionId) for the compromised accounts, the list of
apps accessed, and every admin/config change in the window.
