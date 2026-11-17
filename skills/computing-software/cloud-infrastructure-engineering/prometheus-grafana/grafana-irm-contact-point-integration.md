---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.grafana-irm-contact-point-integration
name: grafana-irm-contact-point-integration
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [irm-contact-point, grafana-irm, grafana-oncall, grafana-contact-points, escalation-chain-steps]
level: practitioner
status: docs-checked
description: "Send Grafana OSS or Enterprise alerts to Grafana IRM through a Webhook contact point, with an optional heartbeat alert rule that monitors alerting itself."
sources: ["https://grafana.com/docs/grafana/latest/alerting/configure-notifications/manage-contact-points/integrations/configure-oncall/", "https://grafana.com/docs/oncall/latest/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Grafana IRM contact point integration

Grafana IRM is the on-call and incident response product in Grafana Cloud, and a paid add-on billed on monthly active
IRM users (see the vendor's pricing and invoice docs). For Grafana OSS and Enterprise, alerts reach it through a
webhook contact point, then IRM routes them via escalation chains. These steps do not apply to Grafana Cloud Alerting,
which has its own documentation.

## Setup
1. In IRM: Alerts & IRM -> IRM -> Integrations -> + New integration, select **Alertmanager** (preconfigured IRM
   templates for Grafana and Prometheus alerts) or **Webhook** (default templates), add a title, description and team,
   click Create Integration, and copy the HTTP Endpoint URL. An existing Alertmanager or Webhook integration also works.
2. In Grafana: Alerts & IRM -> Alerting -> Notification configuration -> Contact points -> + Add contact point, enter
   a name, choose integration **Webhook**, paste the IRM endpoint URL as the URL, Save contact point.
3. Use the contact point's Test button, then check the test alert group appears in IRM.
4. Attach the contact point to the paging branch of your notification policy tree.

Menu paths and names move between Grafana versions; treat them as lower confidence. See the "Webhook contact point"
page for the payload format and "Configure IRM alert templates" for processing incoming messages in IRM.

## Heartbeat monitoring (optional)
A heartbeat makes IRM create a new alert group if Grafana Alerting stops sending alerts.
1. In the IRM integration: three-dot menu -> Heartbeat Settings; copy the Endpoint URL and set the heartbeat
   interval (the time after which IRM starts a new alert group without a heartbeat).
2. Create a second Webhook contact point in Grafana using the heartbeat endpoint URL.
3. Create a Grafana-managed alert rule that always fires (for example a Prometheus query `vector(1) > 0`), with a
   pending period shorter than the heartbeat interval, routed to the heartbeat contact point.
4. Set group wait 0s, group interval 1s, and a repeat interval shorter than the heartbeat interval, so alerts are
   forwarded before the interval elapses.
5. The Heartbeat column on the IRM Integrations page shows the status.

## Gotchas
- Policy grouping in Grafana (`group_by`) is yours to match to how responders work; the pages above do not describe how
  IRM groups the incoming webhook messages, so test with your own alerts.

## Verify
- [ ] A test alert reaches the intended escalation chain in IRM.
- [ ] The heartbeat column is healthy, and stopping the heartbeat rule produces an IRM alert group.

## Checked
Checked 2026-11-08 against "Configure Grafana IRM for Alerting" (webhook contact point, integration types, heartbeat)
and the Grafana IRM overview page (product description, paid add-on). The IRM integration-reference URL in the old
`sources` returned 404 and was dropped. Removed: the "Grafana IRM" contact point type, Jinja2 route example, default
grouping and resolve behaviour, repeat-interval grouping behaviour, and the OnCall OSS end-of-support claim, none of
which the readable pages state.
Method: documentation only; no commands were run.
