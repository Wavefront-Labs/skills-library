---
id: computing-software.systems-network-administration.keepalived.global-defs-email-alerts
name: global-defs-email-alerts
category: computing-software
field: systems-network-administration
product: keepalived
tags: [systems-network-administration, keepalived, global-defs, email-alerts, smtp, notification-email, smtp-server]
level: practitioner
status: docs-checked
description: "global_defs email settings: notification_email recipients, notification_email_from, smtp_server and the SMTP connect timeout, with the case-study values."
sources:
  - https://keepalived.readthedocs.io/en/latest/configuration_synopsis.html
  - https://keepalived.readthedocs.io/en/latest/case_study_healthcheck.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# global_defs: email alerts

Inside `global_defs`:

| Keyword | Meaning | Case-study value |
|---|---|---|
| `notification_email { ... }` | Block of recipient addresses | admin@domain.com and a second address |
| `notification_email_from` | Address used in SMTP MAIL FROM | keepalived@domain.com |
| `smtp_server` | Remote SMTP server | 192.168.200.20 |
| `smtp_connect_timeout` | SMTP stream timeout | 30 |

The synopsis table spells the timeout `smtp_connection_timeout` in one place, but the case study uses `smtp_connect_timeout`; copy the case-study spelling. The page gives no defaults for these keywords.

Mail is sent for state changes; `smtp_alert` inside a `vrrp_instance` enables notification on MASTER transitions.

Verify: force a failover and confirm the recipient mailbox receives a message from the configured sender.

## Checked

2026-11-04. Confirmed the global_defs keywords, the smtp_connection_timeout spelling inconsistency and smtp_alert on the configuration synopsis page, the case-study values on the Healthcheck case study page, and that SMTP notifications cover healthchecker activity and VRRP state transitions on the Software Design page. Nothing removed.

Method: documentation only; no commands were run.
