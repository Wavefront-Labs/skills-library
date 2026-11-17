---
id: computing-software.web-development.node-express.alerting-on-attack-patterns
name: alerting-on-attack-patterns
category: computing-software
field: web-development
product: node-express
tags: [security-logging, security-alerting, monitoring, detection, siem, incident-response]
level: practitioner
status: draft
description: "Turning security logs into actionable alerts: credential stuffing, brute force, authorization-failure spikes, admin anomalies, thresholds, routing and runbooks."
sources:
  - https://owasp.org/Top10/A09_2021-Security_Logging_and_Monitoring_Failures/
  - https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html
  - https://attack.mitre.org/techniques/T1110/
  - https://sre.google/sre-book/monitoring-distributed-systems/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Alerting on attack patterns

Logging without alerting is how breaches go unnoticed for months (A09). Start with a handful of high-signal rules.

## 1. Starter detections
| Pattern | Signal | Example rule |
|---|---|---|
| Credential stuffing | many failed logins across many usernames from a set of IPs/ASNs; success ratio collapses | failures > 500/5 min globally or > 20 distinct usernames per IP in 5 min |
| Brute force on one account | repeated failures on one user | > 10 failures/15 min per account (also lock/throttle) |
| Account takeover after stuffing | success following many failures from same IP; new device + password/email change | correlate within 1 h |
| Authorization probing | spike in 403/404 per user/session on object IDs | > 50 403s/10 min per user |
| Admin anomalies | admin login from new country, role grants, mass export | any, outside business hours -> page |
| Injection/scanner noise | validation failures, WAF hits, known scanner UAs | trend dashboard, alert on spikes |
| Token abuse | refresh-token reuse (rotation detection), API key used from new range | any reuse -> revoke family + alert |

## 2. Implementation
- SIEM/log platform queries on structured fields (`event`, `outcome`, `user_id`, `ip`): Datadog monitors, Elastic rules, Grafana Loki alert rules, Splunk, CloudWatch metric filters + alarms.
- Emit counters as metrics (Prometheus `auth_login_failures_total{reason}`) for cheap rate alerts.
- Baselines: alert on deviation from normal (x3 the 7-day same-hour average) instead of static thresholds for traffic-dependent signals.

## 3. Make alerts actionable
- Each alert links a runbook: what it means, how to confirm, how to contain (block IP/ASN at WAF, force password resets, revoke sessions, enable CAPTCHA).
- Route by severity: page for active takeover/admin anomalies; ticket for trends.
- Tune weekly at first; delete alerts nobody acts on. Track mean time to detect in incident reviews.

## 4. Automatic responses
Progressive rate limiting, bot challenges, temporary lockouts, step-up MFA on risky logins - with alerts on when they trigger.

## Verify
Simulate: run a credential-stuffing script against staging (100 users x wrong passwords) and confirm the alert fires within the window and reaches on-call with the runbook link.
