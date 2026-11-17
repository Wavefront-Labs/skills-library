---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.grafana-contact-points-and-notification-policies
name: grafana-contact-points-and-notification-policies
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [grafana, grafana-alerting, contact-points, notification-policies, grafana-notification-policies, policy-tree, matchers, continue-matching, group-by, group-wait, group-interval, repeat-interval, mute-timings, grafana-alert-templates, grafana-notification-templates, go-templates, slack, pagerduty, opsgenie, webhook, email, silences, external-alertmanager, provisioning-alerting, notification-errors]
level: advanced
status: gated
description: "Route Grafana alerts to the right people: contact points, the notification policy tree with matchers/continue/timers, mute timings, notification templates, silences, and testing the path."
sources: ["https://grafana.com/docs/grafana/latest/alerting/configure-notifications/", "https://grafana.com/docs/grafana/latest/alerting/configure-notifications/create-notification-policy/", "https://grafana.com/docs/grafana/latest/alerting/configure-notifications/template-notifications/", "https://grafana.com/docs/grafana/latest/alerting/configure-notifications/mute-timings/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Contact points and notification policies

**Goal:** each firing alert reaches exactly the owning team's channel with the right
urgency, grouped sensibly, quiet during planned windows, and with a message people can act
on without opening Grafana.

## 1. Contact points
One contact point per destination (`payments-pagerduty`, `payments-slack`, `platform-email`),
each with one or more integrations. A policy names a **contact point** (the `name:` below), never an integration `uid`. Secrets (webhook URLs, API keys) go in `settings` with `$VAR` env expansion in files: on Grafana 13.2.4 a `secureSettings:` block was not picked up (the Slack point failed with `recipient must be specified when using the Slack chat API`, the PagerDuty point with `could not find integration key property in settings`). Exports show them as `[REDACTED]`.
```yaml
# provisioning/alerting/contact-points.yaml
apiVersion: 1
contactPoints:
  - orgId: 1
    name: payments-slack
    receivers:
      - uid: payments-slack
        type: slack
        # webhook mode: url in settings and NO recipient/token (recipient + token is the chat API mode)
        settings: { title: '{{ template "slack.title" . }}', text: '{{ template "slack.text" . }}', url: $SLACK_WEBHOOK_PAYMENTS }
        disableResolveMessage: false
  - orgId: 1
    name: payments-pd            # a separate contact point: the policy below routes to it by name
    receivers:
      - uid: payments-pd
        type: pagerduty
        settings: { severity: critical, class: '{{ .CommonLabels.service }}', integrationKey: $PD_KEY_PAYMENTS }
```
Use **Test** in the UI (sends a synthetic alert) after creating; check
`grafana_alerting_notifications_failed_total` (the metric name in Grafana 13.2.4 `/metrics`; the old text had `notification_failed`) or the contact point health view (UI, not clicked) (gated: unconfirmed, source is paywalled or blocked) for errors. The old `receivers/test` API is removed in 13.2.4.

## 2. The policy tree
```yaml
policies:
  - orgId: 1
    receiver: platform-catchall           # root: every alert that matches nothing else
    group_by: [grafana_folder, alertname]
    group_wait: 30s
    group_interval: 5m
    repeat_interval: 4h
    routes:
      - receiver: platform-datasource     # reserved alerts first
        object_matchers: [[alertname, =~, "DatasourceError|DatasourceNoData"]]
        repeat_interval: 1h
      - object_matchers: [[team, =, payments]]
        receiver: payments-slack
        group_by: [alertname, service]
        continue: false
        routes:
          - object_matchers: [[severity, =, page]]
            receiver: payments-pd
            continue: true                 # page AND fall through to Slack sibling below
          - object_matchers: [[severity, =~, "page|ticket"]]
            receiver: payments-slack
            mute_time_intervals: [weekends]
```
Semantics (same as Alertmanager): depth-first, first matching sibling wins unless
`continue: true`; children inherit receiver, `group_by` and timers unless overridden.
`group_by: ['...']` disables grouping (not run here) (gated: unconfirmed, source is paywalled or blocked). The root policy has a receiver in every working example here. This exact tree was provisioned and run: `team=payments, severity=page` reached `payments-pd` AND `payments-slack` once each (`continue: true` on the first child), `severity=ticket` reached `payments-slack` only, an alert with neither label reached `platform-catchall`.
Matchers support `=`, `!=`, `=~`, `!~`; label values are compared as strings.

Design rules:
- Route by **labels you control in rules** (`team`, `severity`, `service`); never by alert name regexes you'll forget to update.
- Catch-all must be visible (a shared Slack channel), never `/dev/null`.
- Pages: short `group_wait` (0–30s), `repeat_interval` ≥ 4h (pager escalation handles re-ping).
- Tickets: longer `group_interval`, mute outside hours.
- Keep `continue` rare and documented; it is the main source of "why did I get this twice".

## 3. Mute timings and silences
```yaml
muteTimes:
  - orgId: 1
    name: weekends
    time_intervals:
      - weekdays: ["saturday", "sunday"]
        location: Europe/London
  - name: change-freeze
    time_intervals: [{ times: [{ start_time: "00:00", end_time: "23:59" }], days_of_month: ["24:26"], months: ["12"] }]
```
Mute timings apply to a **policy** (planned quiet); **silences** apply to **alerts by matchers**
for a duration with a comment (unplanned/ad hoc). Silence from the alert's "Silence"
button narrowly (`alertname`, `service`), set an end time, and review active silences
in handover. Active-time intervals are the inverse (notify only during) (not run here) (gated: unconfirmed, source is paywalled or blocked). Both mute timing examples loaded; a policy muted by an all-week interval produced no email (allow about a minute after a reload).

## 4. Notification templates
Reusable Go templates stored under *Notification templates*, referenced from contact
point fields (a freshly saved template took up to about a minute to take effect: the first alert after saving rendered an empty title). Data: `.Alerts` (`.Firing`, `.Resolved`), `.CommonLabels`, `.CommonAnnotations`,
`.GroupLabels`, `.ExternalURL`; per alert `.Labels`, `.Annotations`, `.Values`,
`.StartsAt`, `.SilenceURL`, `.DashboardURL`, `.PanelURL`, `.GeneratorURL`. The Slack text template rendered `*PAGE* API 5xx ratio 5.213%` with the runbook and silence links (`.DashboardURL` is empty unless the rule is tied to a dashboard panel).
```gotemplate
{{ define "slack.title" }}[{{ .Status | toUpper }}{{ if eq .Status "firing" }}:{{ .Alerts.Firing | len }}{{ end }}] {{ .CommonLabels.alertname }} ({{ .CommonLabels.service }}){{ end }}
{{ define "slack.text" }}{{ range .Alerts -}}
*{{ .Labels.severity | toUpper }}* {{ .Annotations.summary }}
{{ if .Annotations.runbook_url }}<{{ .Annotations.runbook_url }}|Runbook>{{ end }} | <{{ .SilenceURL }}|Silence> | <{{ .DashboardURL }}|Dashboard>
{{ end }}{{ end }}
```
Keep the message: what, where, how bad, link to runbook, link to silence. Preview in the
template editor with a sample payload (UI); a template error at send time = no notification
(check contact point health) (not run here) (gated: unconfirmed, source is paywalled or blocked).

## 5. External Alertmanager
Add an external Alertmanager data source (`jsonData.handleGrafanaManagedAlerts: true`) and set `alertmanagersChoice` (`internal`, `external` or `all`, via `POST /api/v1/ngalert/admin_config`; UI: Alerting settings, not clicked) (gated: unconfirmed, source is paywalled or blocked) to send Grafana-managed alerts there instead of (or as well as)
the built-in one. Use when the org already runs Alertmanager and wants one routing tree;
then policies live in Alertmanager config, not Grafana.

## 6. Provision and test the path end to end
```bash
curl -H "Authorization: Bearer $TOKEN" https://grafana/api/v1/provisioning/policies/export?format=yaml
curl -H "Authorization: Bearer $TOKEN" https://grafana/api/v1/provisioning/contact-points/export
# test routing: create a temporary rule with labels team=payments severity=page and a 0s pending period, or use the "Test" on a contact point
```
Terraform: `grafana_contact_point`, `grafana_notification_policy` (one resource owns the
whole tree), `grafana_mute_timing`, `grafana_message_template` (not run here) (gated: unconfirmed, source is paywalled or blocked).

## Gotchas
- The policy tree is a single object; two teams editing it in the UI overwrite each other.
  Provision it (the file, like `PUT /api/v1/provisioning/policies`, replaces the whole tree), or use nested policies under per-team parent routes with RBAC (RBAC part not run here) (gated: unconfirmed, source is paywalled or blocked).
- Reserved `grafana_folder` label is always present; it is a reasonable default `group_by`.
- Changing `group_by` re-groups and re-sends everything in flight (not run here) (gated: unconfirmed, source is paywalled or blocked).
- `disableResolveMessage: true` on pager integrations means no resolve message is sent, so incidents will not auto-resolve (resolve is a message the integration sends).
- Slack incoming webhooks are per channel; the Slack *API token + recipient* mode (chat API) is the alternative for many channels (not run: it needs a real Slack token) (gated: unconfirmed, source is paywalled or blocked).
- A webhook that does not answer `ok` makes the Slack integration retry (`failed incoming webhook:` in the log), producing repeated deliveries.

## Verify
- [ ] Policy preview (UI "Preview routing" on a rule) shows the intended single receiver per severity.
- [ ] A test alert with `team=payments severity=page` reaches PagerDuty and Slack once each; `severity=ticket` reaches Slack only, and not on a weekend.
- [ ] Contact point health shows no delivery errors in the last 24h.
- [ ] Catch-all receives alerts that lack `team` and someone owns that channel.

## Checked
Environment: Windows 11, Grafana OSS 13.2.4; local webhook sink standing in for Slack and PagerDuty (their `url` settings pointed at it); local SMTP sink; Alertmanager 0.34.1.
- Ran the skill's contact point, template, mute time and policy YAML as file provisioning. It failed in three places, fixed above: `secureSettings` ignored, Slack `recipient` forcing chat-API mode, and the policy naming `payments-pd` which was an integration uid, not a contact point. After the fixes the routing outcomes in the text were observed from `/api/alertmanager/grafana/api/v2/alerts` and the sink logs.
- Metric name from `/metrics`; reserved `grafana_folder` label present on alerts; export redaction.
- Several UI and Terraform lines carry the gated marker, so the skill is `gated`.
