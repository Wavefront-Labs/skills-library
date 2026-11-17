---
id: computing-software.digital-forensics-incident-response.log-analysis.google-workspace-audit-log-investigation
name: google-workspace-audit-log-investigation
category: computing-software
field: digital-forensics-incident-response
product: log-analysis
tags: [google-workspace-audit, google-workspace, gmail-logs, drive-audit, oauth-token-audit, reports-api, cloud-identity, dfir]
level: practitioner
status: draft
description: "Investigate Google Workspace compromise with Admin audit, login, token, Drive and Gmail logs via the console, Reports API, GAM, BigQuery and the investigation tool."
sources: ["https://support.google.com/a/answer/9725685", "https://developers.google.com/admin-sdk/reports/v1/reference/activities/list", "https://github.com/GAM-team/GAM"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Google Workspace audit logs

**Goal:** scope account takeover, data exfiltration and admin abuse in Google Workspace.

## Where logs live
- Admin console > Reporting > **Audit and investigation**: Admin, Login, OAuth (token), Drive,
  Gmail (message log events), SAML, Groups, Devices, Rules, Calendar, Meet and more.
- **Security investigation tool** (Enterprise Plus / Education Plus etc.): query and act (e.g.
  delete phishing emails) across log sources.
- **Reports API** `activities.list` with `applicationName` = `login`, `admin`, `token`,
  `drive`, `saml`, `groups`, `mobile`, `user_accounts`, ...
- **BigQuery export** (Enterprise editions) for long retention and SQL.
- Retention for most audit logs is about **6 months** (varies by log and edition); export early.

## GAM examples
```bash
gam report login user all start 2026-09-01 end 2026-09-30 > login.csv
gam report token user victim@corp.com > token.csv          # OAuth grants/revokes
gam report admin start -30d > admin.csv
gam report drive user victim@corp.com event download > drive_dl.csv
gam user victim@corp.com show tokens                         # current OAuth grants
```

## Key events
| Log | Events of interest |
|---|---|
| Login | `login_success`, `login_failure`, `suspicious_login`, `login_challenge`, `2sv_disable`, `2sv_enroll`, `gov_attack_warning`, `account_disabled_hijacked` |
| Admin | `GRANT_ADMIN_PRIVILEGE`, `CREATE_USER`, `CHANGE_PASSWORD`, `CHANGE_TWO_STEP_VERIFICATION_ENROLLMENT`, `ADD_TO_TRUSTED_APPS` / API access changes, domain-wide delegation changes |
| Token (OAuth) | `authorize` events with app name, client ID and scopes (Gmail/Drive full access scopes are high risk) |
| Drive | `download`, `copy`, `change_user_access`, `change_document_visibility` (to "anyone with link"/external), `create` of large numbers of copies |
| Gmail / user settings | forwarding address added, filters created (rules that auto-forward or delete), delegation granted |

## Investigation patterns
- **Account takeover:** suspicious login from new ASN/country, then 2SV changes, forwarding
  rules, OAuth app grants, mass Drive downloads or sharing changes.
- **Malicious OAuth app:** `authorize` with broad scopes shortly after a phishing email; the app
  keeps access after a password reset unless the token is revoked.
- **Admin abuse/persistence:** new super admins, domain-wide delegation to a service account,
  new SSO profile.
- **Exfiltration:** Takeout usage, Drive downloads and external shares from the account,
  Gmail forwarding.

## Containment pointers
Reset password and sign-out sessions (`gam user <u> signout`), revoke OAuth tokens and app
passwords, remove forwarding/filters/delegates, review admin roles and API controls.

## Self-check
Timeline covers login, token, admin, Drive and Gmail settings events for each compromised
user, with data accessed or shared listed.
