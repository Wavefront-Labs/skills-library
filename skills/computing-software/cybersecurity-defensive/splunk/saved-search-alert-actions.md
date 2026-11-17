---
id: computing-software.cybersecurity-defensive.splunk.saved-search-alert-actions
name: saved-search-alert-actions
category: computing-software
field: cybersecurity-defensive
product: splunk
tags: [splunk, siem-dashboards, alert-actions, webhook, email-alerts, savedsearches-conf, trigger-conditions, alert-throttling]
level: practitioner
status: draft
description: "Configure Splunk alerts and alert actions: trigger conditions, per-result vs once, throttling, webhook payloads to chat/ticketing, email limits and failure monitoring."
sources: ["https://docs.splunk.com/Documentation/Splunk/latest/Alert/Aboutalerts", "https://docs.splunk.com/Documentation/Splunk/latest/Alert/Webhooks", "https://docs.splunk.com/Documentation/Splunk/latest/Admin/Savedsearchesconf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Splunk alerts and alert actions

For teams without ES (or for operational alerts alongside it), plain scheduled alerts do the job.

## Alert definition (savedsearches.conf)
```
[Brute force against VPN]
search = index=vpn action=failure | stats count dc(user) as users by src | where count>50
cron_schedule = */15 * * * *
dispatch.earliest_time = -20m@m
dispatch.latest_time = -5m@m
enableSched = 1
alert_type = number of events
alert_comparator = greater than
alert_threshold = 0
alert.digest_mode = 0          # 0 = trigger per result, 1 = once per search
alert.suppress = 1
alert.suppress.fields = src
alert.suppress.period = 4h
alert.severity = 4
action.webhook = 1
action.webhook.param.url = https://hooks.example.com/services/XXXX
```
- Latest time a few minutes behind now absorbs indexing lag; earliest overlaps the previous
  window slightly. Overlap plus throttling avoids both gaps and duplicates.
- "Per result" with throttling on the entity field = one alert per attacker per window.

## Actions
- **Webhook**: POSTs JSON with `result` (first row only), `search_name`, `results_link`. For
  multi-row or custom payloads (Teams, Slack blocks, Jira), use a dedicated add-on alert action
  or a custom alert action app.
- **Email**: `action.email.to`, `action.email.inline = 1`, `action.email.format = table`; mail
  server set in Settings > Server settings > Email. Large attachments are capped (`maxresults`).
- **Log event / Output to lookup / Add to triggered alerts**: useful for audit and for chaining.
- Custom alert actions: an app with `alert_actions.conf` plus a script in `bin/` reading JSON on stdin.

## Webhook allow list
Splunk 9.x restricts webhook destinations: Settings > Server settings > Webhook allow list
(alert_actions.conf `[webhook] enable_allowlist`). Add the endpoint or the action fails.

## Monitoring
```
index=_internal sourcetype=splunkd component=sendmodalert action=webhook
| stats count by action_status, sid
```
Failures show HTTP errors; schedule this as its own alert. Also check skipped runs in
`index=_internal sourcetype=scheduler status=skipped`.

## Gotchas
- Real-time alerts consume a search slot permanently; use scheduled every 1-5 minutes.
- Alerts run as the owner; if the owner leaves and is disabled, alerts stop (orphaned searches).
  Reassign in Settings > All configurations > Reassign Knowledge Objects.
- Secrets in webhook URLs are readable by anyone who can read the saved search.

## Verify
Force a test by temporarily lowering the threshold and confirm one message per entity arrives
and the result link opens the search.
