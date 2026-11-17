---
id: computing-software.web-development.node-express.shipping-logs-to-a-siem
name: shipping-logs-to-a-siem
category: computing-software
field: web-development
product: node-express
tags: [siem-integration, detection-rules, sigma-rules, log-shipping, security-monitoring, elastic-common-schema]
level: practitioner
status: docs-checked
description: "Getting web app security events into a SIEM: structured log fields, shipping with Vector or OTel, and writing detections for brute force, stuffing and privilege abuse."
sources:
  - https://www.elastic.co/guide/en/ecs/current/index.html
  - https://github.com/SigmaHQ/sigma
  - https://vector.dev/docs/
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Shipping logs to a SIEM

## 1. Make events machine-readable
JSON logs with consistent field names across services; map to a schema the SIEM understands (for example Elastic Common Schema):
```json
{"@timestamp":"2026-10-18T09:12:44Z","event.category":"authentication","event.action":"login",
 "event.outcome":"failure","user.name":"ada@example.com","source.ip":"203.0.113.7",
 "user_agent.original":"...","http.request.id":"req_abc","service.name":"web"}
```
Security events to emit: login success/failure, MFA enrol/disable, password reset, session revocation, role/permission changes, API key create/delete, access denied (403), data exports, admin actions, rate-limit triggers.

## 2. Ship
- Agents: Vector, Elastic Agent, OpenTelemetry Collector, or your cloud's native log export.
- Enrich at the pipeline: GeoIP, ASN, environment; drop noisy debug logs before the SIEM (cost).
- Buffer and retry on the agent; alert when a source goes silent (missing logs is also an incident signal).

## 3. Detections that pay off
| Detection | Logic |
|---|---|
| Brute force | many failed logins for one account in a short window |
| Credential stuffing | one IP/ASN failing logins for many distinct accounts; or global failure ratio spike |
| Account takeover follow-up | login from new country/ASN followed by email/MFA/password change soon after |
| Privilege escalation | role changed to admin outside the admin workflow or by a non-admin |
| Enumeration / IDOR probing | many 403/404 on object ids from one session |
| Mass export | export volume > N x user's baseline |
Write them as Sigma rules where possible (a generic signature format for SIEM systems), version them in git, and replay sample logs to test.

## 4. Response wiring
Route alerts to on-call with context links (user, IP, recent events); automate safe responses (lock account pending verification, block IP at WAF) for high-confidence rules.

## Verify
- [ ] A scripted 20-attempt failed login against staging produces a SIEM alert within 5 minutes.

## Checked
2026-10-28 Confirmed on the ECS event, user, source, service, http and user_agent pages: `event.category`, `event.action`, `event.outcome`, `user.name`, `source.ip`, `user_agent.original`, `http.request.id`, `service.name`, `@timestamp`; on the Sigma page: generic signature format for SIEM systems; Vector and OpenTelemetry on the Vector docs page. Removed: `tenant.id` (not an ECS field), Fluent Bit, Filebeat, Splunk CIM and cloud log export product names (not on the fetched pages). The detection table and the 5-minute target are design guidance, not documented facts.
Method: documentation only; no commands were run.
