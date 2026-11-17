---
id: computing-software.cloud-infrastructure-engineering.alertmanager.template-examples-slack
name: template-examples-slack
category: computing-software
field: cloud-infrastructure-engineering
product: alertmanager
tags: [alertmanager, templating, slack-templates, define-template]
level: practitioner
status: docs-checked
description: "Worked Alertmanager template examples: wiki link in Slack text, CommonAnnotations, ranging over Alerts, and reusable named templates from files."
sources: ["https://prometheus.io/docs/alerting/latest/notification_examples/", "https://prometheus.io/docs/alerting/latest/configuration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Notification template examples

All examples use Go templating inside alertmanager.yml.

Link to a runbook built from group labels:

```yaml
route:
  receiver: 'slack-notifications'
  group_by: [alertname, datacenter, app]
receivers:
- name: 'slack-notifications'
  slack_configs:
  - channel: '#alerts'
    text: 'https://internal.myorg.net/wiki/alerts/{{ .GroupLabels.app }}/{{ .GroupLabels.alertname }}'
```

Use annotations set in the Prometheus rule. Prometheus templates (`$labels`) apply in the rule; Alertmanager templates apply in the receiver:

```yaml
text: "<!channel> \nsummary: {{ .CommonAnnotations.summary }}\ndescription: {{ .CommonAnnotations.description }}"
```

Range over every alert in the group:

```yaml
title: "{{ range .Alerts }}{{ .Annotations.summary }}\n{{ end }}"
text: "{{ range .Alerts }}{{ .Annotations.description }}\n{{ end }}"
```

Reusable named templates: put definitions in a file and list it under `templates`:

```
{{ define "slack.myorg.text" }}https://internal.myorg.net/wiki/alerts/{{ .GroupLabels.app }}/{{ .GroupLabels.alertname }}{{ end}}
```

```yaml
templates:
- '/path/to/templates/myorg.tmpl'
receivers:
- name: 'slack-notifications'
  slack_configs:
  - channel: '#alerts'
    text: '{{ template "slack.myorg.text" . }}'
```

The `templates` path's last component may use a wildcard such as `templates/*.tmpl`.

## Checked

2026-11-08. Confirmed against the Notification template examples page (GroupLabels runbook link, CommonAnnotations, range over Alerts, reusable define/template) and the configuration reference (templates path last component may use a wildcard).

Method: documentation only; no commands were run.
