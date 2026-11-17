---
id: computing-software.cloud-infrastructure-engineering.google-cloud.cloud-ngfw-threat-logs-and-alerting
name: cloud-ngfw-threat-logs-and-alerting
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-ngfw, ngfw-threat-logs, intrusion-prevention, firewall-threat-logs, security-profiles, log-based-alerts]
level: practitioner
status: docs-checked
description: "Read Cloud NGFW Enterprise threat logs from intrusion prevention, query by severity and threat ID, alert on critical detections, and tune security profile overrides."
sources: ["https://cloud.google.com/firewall/docs/about-intrusion-prevention", "https://cloud.google.com/firewall/docs/about-security-profiles", "https://cloud.google.com/firewall/docs/configure-intrusion-prevention", "https://cloud.google.com/firewall/docs/configure-security-profiles"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud NGFW threat logs and alerting

When a firewall policy rule uses `apply_security_profile_group` with a threat prevention profile,
traffic is inspected by firewall endpoints, and a detection is logged or dropped according to the action for the threat.

## Actions
- Deny logs the threat and drops the packet.
- Alert logs the threat and allows the session.
- Allow ignores the threat, if detected.

## Query and alert
Find the exact log name and field names for threat logs in the Cloud NGFW logging documentation or by opening one entry in Logs Explorer; this skill does not assert them. Then:
```bash
gcloud logging metrics create ngfw_critical_threats \
  --log-filter='<your threat-log filter for CRITICAL severity>'
```
Alert on the metric and route it to your SOC.

## Tuning
- Use threat prevention security profiles to override the default action for a severity level; start with `ALERT` and move to `DENY` after review.
- Override per threat ID for false positives:
  ```bash
  gcloud network-security security-profiles threat-prevention add-override ips-prof \
    --organization=<ORG> --location=global --threat-ids=<ID> --action=ALLOW
  ```
- Severity-level actions: `--severities=MEDIUM --action=ALERT`.

## Gotchas
- Firewall endpoints are zonal resources.

## Verify
- [ ] A test detection generates a threat log and alert.

## Checked
2026-10-28. Confirmed on the Cloud NGFW about-security-profiles, about-intrusion-prevention and configure-intrusion-prevention pages: DENY, ALERT and ALLOW semantics, severity-level overrides through threat prevention profiles, `--action` values, `apply_security_profile_group`, zonal endpoints. gcloud commands and flags passed check_commands. Removed: the log name and jsonPayload field names (the threat-logs page the skill cited does not exist), `--freshness` query, alert thresholds and the remaining gotchas, none of which the fetched pages confirm.
Method: documentation only; no commands were run.
