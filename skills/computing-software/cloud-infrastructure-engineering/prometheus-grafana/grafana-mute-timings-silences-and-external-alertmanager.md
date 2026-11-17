---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.grafana-mute-timings-silences-and-external-alertmanager
name: grafana-mute-timings-silences-and-external-alertmanager
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [grafana-alerting, mute-timings, mute-timing-schedule, recurring-mute-timings, grafana-silences, silence-api, external-alertmanager-datasource, forward-to-alertmanager]
level: practitioner
status: gated
description: "Suppress Grafana alert notifications with recurring mute timings and silences (UI and API), and route Grafana-managed alerts to an external Alertmanager data source."
sources: ["https://grafana.com/docs/grafana/latest/alerting/configure-notifications/mute-timings/", "https://grafana.com/docs/grafana/latest/alerting/configure-notifications/create-silence/", "https://grafana.com/docs/grafana/latest/alerting/set-up/configure-alertmanager/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mute timings, silences and external Alertmanagers

## Mute timings (recurring)
Alerting -> Notification policies -> Mute timings (UI path not clicked here) (gated: unconfirmed, source is paywalled or blocked). Intervals take `times`, `weekdays`, `days_of_month`, `months` and a **location** (time zone); in files `weekdays: ["monday:saturday", "sunday"]` is valid but `"monday:sunday"` was rejected (HTTP 400 `bad request data`), because ranges must ascend and Sunday is the first day. Attach them to policies with `mute_time_intervals` in the policy: a policy muted by an all-week interval produced no email while the rule stayed `Alerting` in Grafana (only notifications are held). Allow about a minute after a provisioning reload before testing: the first alert after the reload was still delivered. Attaching a mute timing to a rule with simplified routing (`notification_settings.mute_time_intervals`) is stored but I could not get it to suppress, so do not rely on it (gated: unconfirmed, source is paywalled or blocked). Use **active time intervals** for the inverse (notify only within business hours) (not run here) (gated: unconfirmed, source is paywalled or blocked).

## Silences (one-off)
UI: Alerting -> Silences -> New: matchers (`service=checkout`, regex `=~`), start/end, comment. Or from a firing
alert's "Silence" action (pre-filled matchers).
```bash
curl -s -XPOST https://grafana/api/alertmanager/grafana/api/v2/silences \
  -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' -d '{
  "matchers":[{"name":"service","value":"checkout","isRegex":false,"isEqual":true}],
  "startsAt":"<now or later, RFC 3339 UTC>","endsAt":"<in the future, e.g. 2h later>",
  "createdBy":"deploy-bot","comment":"release 4.12"}'
curl -s https://grafana/api/alertmanager/grafana/api/v2/silences -H "Authorization: Bearer $TOKEN" | jq '.[] | select(.status.state=="active")'
```
Use real current timestamps: a window that had already ended was refused (`end time can't be in the past`), and a silence starting later is created in state `pending`, then `active`. The call returns `{"silenceID":"..."}`. The path segment `grafana` addresses the built-in Alertmanager; the data source UID worked for an external one (`/api/alertmanager/<ds-uid>/api/v2/silences`).
Permissions: a Viewer service account got 403 naming `alert.silences:create` among the needed permissions.

## External Alertmanager
1. Add an **Alertmanager data source** (`type: alertmanager`, `jsonData.implementation: prometheus` ran; Mimir is the other implementation, not run), URL, auth. Enable "Receive Grafana Alerts" (`jsonData.handleGrafanaManagedAlerts: true`).
2. Choose where Grafana-managed alerts go: `POST /api/v1/ngalert/admin_config` with `{"alertmanagersChoice":"internal"|"external"|"all"}` (all three accepted, other values rejected with `Invalid alertmanager choice specified`); the UI location is Alerting -> Settings (not clicked here) (gated: unconfirmed, source is paywalled or blocked).
3. Routing, silences and templates then live in that Alertmanager's config; Grafana shows its alerts and silences
   in the UI when the data source is selected.
Use when an organisation already runs a central Alertmanager (or Mimir's) and wants one routing tree for
Prometheus and Grafana alerts.

## Verify
- [ ] A test alert during a mute timing produces no notification and fires afterwards if still active.
- [ ] Silences created via API appear in the UI and expire on time.
- [ ] With external AM selected, Grafana alerts appear in that AM's `/api/v2/alerts` (took one to two minutes after the setting changed on 13.2.4; then the firing alerts arrived).

## Checked
Environment: Windows 11, Grafana OSS 13.2.4, Alertmanager 0.34.1 on localhost.
- Ran: silence POST with fixed past dates (refused), with real times (accepted, `pending`, listed with `status.state`), Viewer SA refused; external Alertmanager data source, `admin_config` choices, silence POST via the data source uid, and external `/api/v2/alerts` receiving Grafana alerts; mute timing files (`monday:sunday` rejected, ranges valid) and a policy mute that suppressed an email. A plain Alertmanager 0.34.1 also muted a route with the same interval.
- UI paths and some behaviours carry the gated marker, so the skill is `gated`.
