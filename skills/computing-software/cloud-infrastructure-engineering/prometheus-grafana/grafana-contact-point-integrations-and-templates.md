---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.grafana-contact-point-integrations-and-templates
name: grafana-contact-point-integrations-and-templates
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [grafana-alerting, contact-points, grafana-slack-integration, grafana-pagerduty-integration, grafana-teams-integration, grafana-webhook-contact-point, custom-webhook-template, notification-template-functions, template-data-reference, test-contact-point, notification-preview, grafana-alert-templates]
level: practitioner
status: gated
description: "Configure Grafana contact points (Slack app, PagerDuty, Teams, webhook with custom payload), write notification templates against the template data, and test and preview them."
sources: ["https://grafana.com/docs/grafana/latest/alerting/configure-notifications/manage-contact-points/", "https://grafana.com/docs/grafana/latest/alerting/configure-notifications/template-notifications/reference/", "https://grafana.com/docs/grafana/latest/alerting/configure-notifications/manage-contact-points/integrations/webhook-notifier/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Contact points and notification templates

## Integrations
- **Slack**: a Bot token (`xoxb-`, scopes `chat:write`, `files:write` for images) with a channel (chat API mode, needs both `token` and `recipient`) or an incoming webhook (`url` only; adding a `recipient` without a token is rejected). Title/Text fields accept templates (the webhook mode ran with a template; the token mode needs a real Slack workspace) (gated: unconfirmed, source is paywalled or blocked).
- **PagerDuty**: Integration (routing) key from an Events API v2 service (`integrationKey` in `settings`; the payload sent had `routing_key`, `dedup_key`, `event_action: trigger`, `payload.severity`, `class`, `component`, `group`); set Severity from a label (`{{ .CommonLabels.severity }}`), Class/Component/Group for PD event grouping. PagerDuty's own incident resolution was not exercised (gated: unconfirmed, source is paywalled or blocked).
- **Microsoft Teams**: Workflows (Power Automate) webhook URL; legacy O365 connectors are retired (vendor statement, not checked here) (gated: unconfirmed, source is paywalled or blocked).
- **Webhook**: URL, HTTP method, auth (basic/bearer), max alerts, and a **custom payload** template (`settings.payload.template`) so the receiver gets exactly the JSON it wants (the `payload` setting was accepted by the API; delivery of a custom payload was not observed here) (gated: unconfirmed, source is paywalled or blocked). `toJson` is NOT defined in Grafana notification templates (saving it failed with `function "toJson" not defined`); use `data.ToJSON` and `tmpl.Exec`. This version rendered valid JSON through the template tester:
```gotemplate
{{ define "jira.payload" }}{"fields":{"project":{"key":"OPS"},"summary":{{ .CommonAnnotations.summary | data.ToJSON }},
 "description":{{ tmpl.Exec "default.message" . | data.ToJSON }},"labels":["grafana","{{ .CommonLabels.team }}"]}}{{ end }}
```

## Templates (Alerting -> Contact points -> Notification templates)
```gotemplate
{{ define "short.title" }}[{{ .Status | toUpper }}{{ if gt (len .Alerts.Firing) 0 }}:{{ len .Alerts.Firing }}{{ end }}] {{ .CommonLabels.alertname }}{{ end }}
{{ define "short.body" }}{{ range .Alerts.Firing }}
- {{ .Labels.service }}: {{ .Annotations.summary }} ({{ .ValueString }})
  {{ if .DashboardURL }}Dashboard: {{ .DashboardURL }}{{ end }} {{ if .SilenceURL }}Silence: {{ .SilenceURL }}{{ end }}
{{ end }}{{ end }}
```
Template data: `.Receiver`, `.Status`, `.Alerts` (`.Firing`, `.Resolved`), `.GroupLabels`, `.CommonLabels`,
`.CommonAnnotations`, `.ExternalURL`; per alert `.Labels`, `.Annotations`, `.Values`, `.ValueString`,
`.StartsAt`, `.EndsAt`, `.GeneratorURL`, `.SilenceURL`, `.DashboardURL`, `.PanelURL`, `.Fingerprint`, `.OrgID`
(all of the per-alert ones rendered in a delivered notification; `.Values` prints as `map[A:1 C:1]`, `.StartsAt` as `2026-10-22 17:06:00 +1000 AEST`).
Functions that saved and rendered in notification templates on 13.2.4: `toUpper`, `toLower`, `title`, `join`, `reReplaceAll`, `date`, `tz`, `len`, `slice`, `stringSlice`, `safeHtml`, `match`, `urlquery`, `trimSpace`, plus `data.ToJSON`, `coll.Dict`, `tmpl.Exec`. NOT defined there: `humanize`, `humanizePercentage`, `humanizeDuration`, `humanize1024`, `toJson`, `toString`, `graphLink`, `tableLink`, `externalURL`, `pathPrefix`, `humanizeTimestamp`, `stripPort` (saving each failed with `function "..." not defined`). `humanizePercentage` DOES work in alert rule annotations, which use a different template set.

## Test and preview
- Contact point -> **Test**: sends a predefined or custom (labels/annotations) test notification (UI; the old `receivers/test` API returns `This endpoint has been removed`) (gated: unconfirmed, source is paywalled or blocked).
- Template editor -> **Preview**: the API behind it, `POST /api/alertmanager/grafana/config/api/v1/templates/test` with `{template, name, alerts[]}`, returned each `define` block rendered. A newly saved template can take up to about a minute before notifications use it.
- Failures: the metric `grafana_alerting_notifications_failed_total` exists in `/metrics`.

## Verify
- [ ] Test notification arrives in each integration with the templated format.
- [ ] Webhook receiver parses the custom payload without transformation code.

## Checked
Environment: Windows 11, Grafana OSS 13.2.4, local webhook and SMTP sinks.
- Saved every function name used in the skill as a template through `PUT /api/v1/provisioning/templates/<name>` (parse check) and rendered the list in a delivered webhook notification and through the template tester API; the skill's short.title/short.body templates ran and rendered.
- PagerDuty and Slack (webhook mode) integrations delivered to a local sink, so the payload keys are observed.
- Items marked gated were not run, so the skill is `gated`.
