---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.grafana-oncall-alert-grouping-and-auto-resolve
name: grafana-oncall-alert-grouping-and-auto-resolve
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [grafana-oncall, oncall-grouping-id, oncall-autoresolve, jinja2-templates, alert-groups]
level: advanced
status: docs-checked
description: "Grafana OnCall behavioral templates (grouping ID, autoresolution, auto acknowledge) and why to keep Alertmanager defaults and send_resolved on."
sources: ["https://github.com/grafana/oncall/blob/dev/docs/sources/configure/jinja2-templating/_index.md", "https://github.com/grafana/oncall/blob/dev/docs/sources/configure/integrations/_index.md", "https://github.com/grafana/oncall/blob/dev/docs/sources/configure/integrations/references/alertmanager/index.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OnCall grouping and auto-resolve templates

**Goal:** one alert group per incident, and groups that resolve themselves.

## Alert flow
An alert arrives at the integration's Unique URL as an HTTP POST with a JSON payload. It is routed by the Routing
Template, grouped by the Grouping ID Template, rendered by the Appearance Templates, published to ChatOps, escalated
through the route's chain, and acknowledged or resolved according to the Behavioral Templates.

## Templates (Jinja2 over `payload`, edited per integration)
- Every alert has the fields Title, Message, Image Url, Grouping Id, Resolved by source, Acknowledged by source and
  Source link.
- Behavioral templates: `Grouping Id` (applied to every incoming payload after routing; decides grouping),
  `Autoresolution` (status `Resolved by source`), `Auto acknowledge` (status `Acknowledged by source`), `Source link`.
- Autoresolution and auto acknowledge are conditional templates, and conditional templates must output `True` to apply,
  for example `{{ True if payload.state == 'OK' else False }}`.
- Docs mapping example for a Grafana Alerting payload: `{{ payload.ruleId }}` is the Grouping Id and
  `{{ 1 if payload.state == 'OK' else 0 }}` is the resolve signal.
- Edit under Integration page -> Templates -> Edit: the editor shows the example payload, the template, and the
  rendered result; choose a recent alert group payload or Use custom payload. For systems without a built-in
  integration, use a Webhook integration and write the templates yourself.

## Alertmanager integration
- Add a `webhook_configs` receiver whose `url` is the OnCall integration URL (the trailing slash is required), with
  `send_resolved: true` so OnCall can autoresolve, and `max_alerts` below 100 to keep requests small.
- The docs say OnCall relies on Alertmanager's grouping and autoresolution, recommend configuring grouping in
  Alertmanager and keeping the default OnCall grouping and autoresolution templates, and warn that changing them can
  cause incorrect grouping and autoresolution. Customise only if you disabled grouping in Alertmanager.

## Verify
- [ ] A test firing payload creates one alert group; the matching resolved payload (`send_resolved: true`) closes it.

## Checked

2026-11-08. Confirmed against the raw OnCall docs in the grafana/oncall repository (configure/jinja2-templating,
configure/integrations index, integrations/references/alertmanager). The grafana.com URLs redirect to a generic page,
so these replaced them in `sources`. Removed as unconfirmed: the custom service+alertname grouping example, the
generic webhook example, the design guidance, and the "Send demo alert" tip; the old claim that you tune grouping in
OnCall was reversed to match the Alertmanager page's recommendation.
Method: documentation only; no commands were run.
