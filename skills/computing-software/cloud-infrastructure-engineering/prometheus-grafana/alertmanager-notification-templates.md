---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.alertmanager-notification-templates
name: alertmanager-notification-templates
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [alertmanager, template-customization, custom-notification-template, notification-templates, go-templates, slack-template]
level: practitioner
status: verified
description: "Write Alertmanager .tmpl notification templates: data model (.Alerts, .CommonLabels, .GroupLabels), define/template blocks, Slack/email examples, and testing renders."
sources: ["https://prometheus.io/docs/alerting/latest/notifications/", "https://prometheus.io/docs/alerting/latest/notification_examples/", "https://github.com/prometheus/alertmanager/blob/main/template/default.tmpl"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Alertmanager notification templates

## Wire up
```yaml
templates: ['/etc/alertmanager/templates/*.tmpl']
receivers:
  - name: slack-platform
    slack_configs:
      - api_url_file: /etc/alertmanager/secrets/slack-webhook   # or global.slack_api_url; required, check-config fails without it
        channel: '#platform-alerts'
        title: '{{ template "slack.title" . }}'
        text: '{{ template "slack.text" . }}'
        send_resolved: true
```

## Template file
```gotemplate
{{ define "slack.title" -}}
[{{ .Status | toUpper }}{{ if eq .Status "firing" }}:{{ .Alerts.Firing | len }}{{ end }}] {{ .GroupLabels.alertname }} ({{ .CommonLabels.cluster }})
{{- end }}

{{ define "slack.text" -}}
{{ range .Alerts.Firing -}}
*{{ .Labels.severity | toUpper }}* {{ .Annotations.summary }}
{{ if .Annotations.runbook_url }}<{{ .Annotations.runbook_url }}|Runbook> | {{ end }}<{{ .GeneratorURL }}|Query>
{{ range .Labels.SortedPairs }}{{ if not (eq .Name "alertname" "severity") }}`{{ .Name }}={{ .Value }}` {{ end }}{{ end }}
{{ end -}}
{{ if .Alerts.Resolved }}Resolved: {{ range .Alerts.Resolved }}{{ .Labels.instance }} {{ end }}{{ end }}
<{{ template "__alertmanagerURL" . }}|Silence / view>
{{- end }}
```

## Data model
- Top level: `.Status`, `.Receiver`, `.GroupLabels`, `.CommonLabels`, `.CommonAnnotations`, `.ExternalURL`, `.Alerts`.
- `.Alerts.Firing` / `.Alerts.Resolved` filter lists; each alert has `.Labels`, `.Annotations`, `.StartsAt`,
  `.EndsAt`, `.GeneratorURL`, `.Fingerprint`.
- `.Labels.SortedPairs`, `.Labels.Names`, `.Labels.Values`, `.Labels.Remove (stringSlice "a" "b")` (it takes one string slice; two plain arguments fail with `wrong number of args`).
- Functions: `toUpper`, `toLower`, `title`, `join`, `match`, `reReplaceAll`, `safeHtml`, `stringSlice`, `date`,
  `tz`, `since`, `humanizeDuration`.
- Default templates (`__subject`, `__alertmanagerURL`, `slack.default.title`) are in default.tmpl; reuse them.

## Testing renders
`amtool template render --template.glob='templates/*.tmpl' --template.text='{{ template "slack.text" . }}'`
renders against built-in example data (the command exists since 0.23, rendering with the default data was fixed in 0.27; run on 0.34.1). The example data has one firing and one resolved alert with labels such as `label1` and `instance`, so `.Labels.severity` and `.Annotations.summary` render empty there; check those fields by firing a test alert with `amtool alert add` to a test receiver.

## Gotchas
- Templates are Go text/template: a missing label or annotation key prints an empty string (tested on 0.34.1), while an unknown field name such as `.NoSuchField` is an error. Guard optional parts with `{{ if }}`.
- Large groups make long messages (chat services limit message size); summarise with `.Alerts.Firing | len` and cap lists with `slice` (`{{ (slice .Alerts 0 1) | len }}` rendered 1 on 0.34.1).
- Whitespace control `{{-` `-}}` matters for compact chat messages.

## Verify
- [ ] Rendered test notification shows summary, runbook link and silence link.
- [ ] Resolved notifications render without empty sections.
