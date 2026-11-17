---
id: computing-software.cybersecurity-defensive.wazuh.alert-levels-and-outputs
name: alert-levels-and-outputs
category: computing-software
field: cybersecurity-defensive
product: wazuh
tags: [alerts, log-alert-level, email-alert-level, alerts-json, syslog-output, smtp-relay]
level: practitioner
status: docs-checked
description: "Set Wazuh log_alert_level and email_alert_level, find alerts.json and alerts.log, and forward alerts by syslog, email or database."
sources:
  - https://documentation.wazuh.com/current/user-manual/manager/alert-management.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Alerts are stored by default in `/var/ossec/logs/alerts/alerts.log` and `/var/ossec/logs/alerts/alerts.json`. Filebeat sends them to the Wazuh indexer by default; they can also go to syslog servers, email or a database.

Thresholds in the `<alerts>` block of `/var/ossec/etc/ossec.conf`:
- `log_alert_level`: default `3`, range 1 to 16.
- `email_alert_level`: default `12`, range 1 to 16. It overrides granular email settings.
- The rule option `alert_by_email` can override both thresholds; `no_email_alert` and `no_log` also control per-rule behaviour.

Restart `wazuh-manager` after any configuration change.

Gotchas:
- A rule below the `<alerts>` minimum level will not trigger an email even if it matches.
- Wazuh does not handle SMTP authentication directly, so an SMTP relay such as Postfix is needed for servers like Gmail.
- Database output requires compiling the manager from source with MySQL or PostgreSQL support.
- Syslog output defaults to UDP port 514; with no `<level>` set, all alerts are forwarded.

## Checked

2026-11-08. Read the whole Alert management page. Confirmed: default alert files, Filebeat to indexer, log_alert_level 3 and email_alert_level 12 with range 1 to 16, override behaviour and alert_by_email, no_email_alert and no_log, restart advice, syslog_output default UDP 514 and level behaviour, no SMTP authentication and Postfix relay, database output needing a source build with MySQL or PostgreSQL. Removed: the claim that lowering log_alert_level grows volume (not on the page) and the note about topics the page omits.
Method: documentation only; no commands were run.
