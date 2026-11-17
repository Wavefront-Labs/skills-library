---
id: computing-software.web-development.node-express.web-incident-response-runbook
name: web-incident-response-runbook
category: computing-software
field: web-development
product: node-express
tags: [incident-response-web, breach-response, session-revocation, credential-rotation, forensics, security]
level: advanced
status: docs-checked
description: "Web app incident response runbook: triage, evidence preservation, containment (revoke sessions, rotate secrets, WAF), removing persistence, recovery, notification."
sources:
  - https://csrc.nist.gov/pubs/sp/800/61/r3/final
  - https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html
  - https://gdpr-info.eu/art-33-gdpr/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Web incident response runbook

## 0. Before anything happens
Named incident commander rota, contact list (hosting, legal, DPO, PR), break-glass access, centralised logs with enough retention for investigations, backups tested, and this runbook rehearsed in a tabletop.

## 1. Triage
- Open an incident channel and a timeline doc; record every action with UTC time.
- Classify: what data/systems, ongoing or past, how detected. Assign severity.

## 2. Preserve evidence before changing things
Snapshot affected servers/volumes and databases, export relevant logs (app, WAF, CDN, cloud audit logs like CloudTrail), save malicious payloads/requests. Do not reboot or wipe first.

## 3. Contain
| Situation | Actions |
|---|---|
| Account takeover / session theft | revoke all sessions (rotate session secret or bump a global session version), force password reset, invalidate refresh tokens and API keys |
| Leaked secrets (`.env`, repo, logs) | rotate every exposed credential first (DB, cloud keys, OAuth client secrets, signing keys), then purge history |
| Active exploitation of a bug | WAF rule / feature flag off / take the endpoint offline; patch |
| Compromised dependency | pin to a safe version, rebuild from clean caches, rotate secrets the build could read |
| XSS exploited | deploy fix + strict CSP; revoke sessions (tokens may have been exfiltrated) |

## 4. Eradicate persistence
Check for: new admin users or role changes, API keys, OAuth apps/webhooks added, SSH keys, cron jobs/scheduled tasks, modified code or uploaded web shells, new IAM users/access keys, DNS changes, mailbox forwarding rules.

## 5. Recover
Restore from known-good backups if integrity is in doubt; redeploy from source; heightened monitoring for re-entry; staged return to service.

## 6. Notify
- GDPR: personal data breach likely to risk individuals' rights -> supervisory authority within 72 hours of awareness; affected users without undue delay if high risk. Other regimes (US state laws, HIPAA, contracts) have their own clocks; involve legal early.
- Customers/status page: factual, what happened, what you did, what they should do.

## 7. Learn
Blameless review after the incident: timeline, root cause, detection gap, actions with owners; update detections and this runbook.

## Verify
- [ ] Tabletop exercise run on a regular schedule; "revoke all sessions" and "rotate DB credentials" have tested scripts.

## Checked
2026-10-28 Confirmed: GDPR Article 33 (72 hours after becoming aware, notify the supervisory authority; reasons for delay) on gdpr-info.eu; NIST SP 800-61 Rev. 3 is the incident response guidance. Removed unsourced figures: 90+ day log retention, two-week review window, 12-month tabletop cadence, first-hour label.
Method: documentation only; no commands were run.
