---
id: computing-software.cybersecurity-defensive.falco.falcosidekick-forwarding
name: falcosidekick-forwarding
category: computing-software
field: cybersecurity-defensive
product: falco
tags: [falcosidekick, alert-forwarding, http-output, slack, prometheus]
level: intro
status: docs-checked
description: "Forward Falco alerts to chat, alerting, logging and storage systems through Falcosidekick fed by Falco http_output."
sources:
  - https://falco.org/docs/concepts/outputs/forwarding/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Falco alerts in JSON format are easy to consume downstream. Falcosidekick is a proxy forwarder acting as a central point for a fleet of Falco instances, which send alerts to it through their HTTP outputs.

It can also add custom fields to alerts, filter them by priority and expose a Prometheus metrics endpoint. It is configured with a YAML file, environment variables, or both, and can be deployed beside Falco in Kubernetes using the official Falco Helm chart.

Output groups it supports include:
- Chat: Slack, Rocketchat, Mattermost, Teams, Webex, Discord, Google Chat, Telegram.
- Metrics and observability: Datadog, Influxdb, Prometheus, Wavefront, Dynatrace, OTEL Metrics.
- Alerting: AlertManager, Opsgenie, PagerDuty, Grafana OnCall.
- Logs: Elasticsearch, Loki, AWS CloudWatchLogs.

Each output has its own settings page in the Falcosidekick repository docs/outputs directory.

Install in Kubernetes with the Falco chart: `helm install falco falcosecurity/falco -n falco --create-namespace --set falcosidekick.enabled=true --set tty=true`; add `--set falcosidekick.webui.enabled=true` for the Falcosidekick UI. In Docker, configure it with environment variables, for example `docker run -d -p 2801:2801 -e SLACK_WEBHOOKURL=<webhook-url> falcosecurity/falcosidekick:<version>`. On a host, put a config file in `/etc/falcosidekick/config.yaml` and run `falcosidekick -c <config-file>`, for instance from a systemd unit. Full docs live at github.com/falcosecurity/falcosidekick.

Gotcha: Falcosidekick receives alerts through Falco HTTP outputs, and Falco `http_output` supports only unencrypted HTTP or HTTPS with a valid (not self-signed) certificate.

## Checked

2026-11-08. Read the cited forwarding page in full and corrected details to match it.

Method: documentation only; no commands were run.
