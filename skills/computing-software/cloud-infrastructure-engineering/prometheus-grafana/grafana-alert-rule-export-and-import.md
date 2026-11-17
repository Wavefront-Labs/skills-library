---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.grafana-alert-rule-export-and-import
name: grafana-alert-rule-export-and-import
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [alert-rule-export, prometheus-rule-import, grafana-alerting, alerting-provisioning-files, grafana-as-code]
level: practitioner
status: gated
description: "Export Grafana alert rules, contact points and policies to YAML/JSON/HCL for provisioning, and import existing Prometheus rule files into Grafana-managed alerting."
sources: ["https://grafana.com/docs/grafana/latest/alerting/set-up/provision-alerting-resources/export-alerting-resources/", "https://grafana.com/docs/grafana/latest/developers/http_api/alerting_provisioning/", "https://grafana.com/docs/grafana/latest/alerting/alerting-rules/alerting-migration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Exporting and importing alert rules

## Export
- UI: Alerting > Alert rules > folder/group/rule menu > Export; choose YAML, JSON or Terraform (HCL). Same for contact points, notification policies, mute timings.
- "Modify export" lets you edit a rule in the form and export the result without saving it (good for drafting provisioning files).
- API:
```bash
curl -s -H "Authorization: Bearer $TOKEN" "$GRAFANA/api/v1/provisioning/alert-rules/export?format=yaml" > rules.yaml
curl -s -H "Authorization: Bearer $TOKEN" "$GRAFANA/api/v1/provisioning/alert-rules/<uid>/export?format=hcl"
curl -s -H "Authorization: Bearer $TOKEN" "$GRAFANA/api/v1/provisioning/policies/export?format=yaml"
```
Export output is in file-provisioning format (`apiVersion: 1`, `groups:`), ready for `provisioning/alerting/`. `format` defaults to YAML (`text/yaml`) and `format=json` is accepted. The `<uid>/export?format=hcl` call returns a whole `grafana_rule_group` resource for the rule's group. The exported `folder:` value is the folder title (`Payments`), not its uid.

## Import
- File provisioning: drop exported YAML in `provisioning/alerting/` and restart/reload (`POST /api/admin/provisioning/alerting/reload` returned `Alerting config reloaded`; new rules appeared without a restart).
- Prometheus rule files into Grafana-managed: the conversion API works on 13.2.4: `POST /api/convert/prometheus/config/v1/rules/<namespace>` with `Content-Type: application/yaml`, header `X-Grafana-Alerting-Datasource-UID: <prometheus ds uid>` and a rule group body (`name`, `interval`, `rules`) returned `{"status":"success"}`; `GET /api/convert/prometheus/config/v1/rules` returns the stored YAML. The rule got provenance `converted_prometheus`, the label `__converted_prometheus_rule__="true"`, and `isPaused: false` (not paused by default). The UI import wizard was not used here (gated: unconfirmed, source is paywalled or blocked).
- Between instances: export from source, adjust data source UIDs, provision on target.

## Gotchas
- Data source UIDs are embedded in rules; they must exist on the target instance (provision data sources with fixed UIDs).
- Provisioned rules are locked: a `PUT /api/v1/provisioning/alert-rules/<uid>` on a file-provisioned rule returned 409 `provenanceMismatch` (`cannot update with provided provenance 'api', needs 'file'`) and the ruler API refused the group (`request affects resources created via provisioning API`). To edit, change the files. To create API-managed objects that stay editable in the UI send the header `X-Disable-Provenance: true` (a contact point created with it showed no provenance).
- Templated annotations using `$values` refer to ref IDs; keep them when editing exports.

## Verify
- [ ] Re-exporting after provisioning gives equivalent YAML. It is not byte-identical: the export added `intervalMs`, `maxDataPoints`, and expanded defaults (and the folder title replaced the folder name used in the file).

## Checked
Environment: Windows 11, Grafana OSS 13.2.4 local, Prometheus 3.15.1.
- Ran the export calls (yaml default, json, single-rule hcl), file-provisioned rules and the reload endpoint, the 409 and ruler refusal on a provisioned rule, `X-Disable-Provenance`, and the Prometheus conversion API with a one-rule YAML file.
- The Alerting UI export menu and import wizard were not clicked; that statement carries the gated marker, so the skill is `gated`.
