---
id: computing-software.cloud-infrastructure-engineering.ansible.controller-metrics-endpoint-and-activity-stream-auditing
name: controller-metrics-endpoint-and-activity-stream-auditing
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, controller-api-cli, controller-metrics, api-v2-metrics, activity-stream, prometheus, audit]
level: advanced
status: gated
description: "Scrape automation controller's /api/v2/metrics/ with Prometheus for capacity and job health, and query the activity stream API to audit who changed what."
sources: ["https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/html-single/configuring_automation_execution/", "https://docs.ansible.com/projects/awx/en/latest/rest_api/filtering.html", "https://legacy-controller-docs.ansible.com/automation-controller/latest/html/controllercli/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Controller metrics endpoint and activity stream auditing

## Metrics for Prometheus
`GET /api/v2/metrics/` returns Prometheus text format (requires a user with system auditor or
admin, or token).
```yaml
# prometheus.yml
scrape_configs:
  - job_name: awx
    metrics_path: /api/v2/metrics/
    scheme: https
    scrape_interval: 60s
    authorization:
      type: Bearer
      credentials_file: /etc/prometheus/awx_token      # OAuth2 token of an auditor user
    static_configs:
      - targets: [awx.example.com]
```
Useful series include per-node capacity (e.g. `awx_instance_remaining_capacity`), queueing/running
job counts and job outcome counters — names vary by version, so read the endpoint output before
writing alerts (gated: unconfirmed, source is paywalled or blocked).
Alert examples: pending jobs > 0 for 15 min; remaining capacity < 10%; failure ratio of
scheduled templates > 0.

In HA, scrape through the load balancer; metrics are aggregated.

## Activity stream: who changed what
Every create/update/delete/associate on API objects is recorded.
```bash
# changes to a job template
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://awx.example.com/api/v2/job_templates/42/activity_stream/?order_by=-timestamp" | jq '.results[] | {timestamp, operation, actor: .summary_fields.actor.username, changes}'

# everything a user did in a window
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://awx.example.com/api/v2/activity_stream/?actor__username=jdoe&timestamp__gte=2026-10-01T00:00:00Z"
```
Filters: `object1=credential`, `operation=delete`, `timestamp__gte`, `actor__username`.
Credential **values** are never included; changes show `$encrypted$`.

Retention: the "Cleanup Activity Stream" management job — set the retention (days of data to keep)
to meet audit requirements, or ship records out first via the logging settings (the
`activity_stream` logger, routing to an external log aggregator).

## Gotchas
- Metrics scraping with a personal admin token ties monitoring to a person; create a dedicated auditor service account.
- Large activity streams slow the UI; keep retention reasonable and archive externally.
- Changes made via `awx-manage` or directly in the DB may not appear in the activity stream.

## Verify
- [ ] Prometheus target is UP and `awx_pending_jobs_total` is graphed.
- [ ] Editing a template in a test shows an activity stream entry with your user and the changed fields.

## Checked

- 2026-10-31: the metrics endpoints (`/api/v2/metrics`, and `/api/controller/v2/metrics/` on 2.5)
with Prometheus-style output, `awx_instance_remaining_capacity`, activity stream logging
(`activity_stream` logger), `awx activity_stream list`, the Cleanup Activity Stream management
job, system/application monitoring guidance, filtering lookups and `page_size` max 200 confirmed
in AAP 2.5 Configuring automation execution, the AWX CLI reference and the AWX REST API filtering page.
- Removed: the exact metric-name list beyond `awx_instance_remaining_capacity` (kept as a gated,
non-load-bearing example with the endpoint-output caveat) and the `?subsystemonly=1`/`?dbonly=1`
query flags (undocumented).
Method: documentation only; no commands were run.
