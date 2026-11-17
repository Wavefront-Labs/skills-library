---
id: computing-software.cloud-infrastructure-engineering.alertmanager.jira-receiver-fields
name: jira-receiver-fields
category: computing-software
field: cloud-infrastructure-engineering
product: alertmanager
tags: [alertmanager, jira-config, issue-creation, transitions]
level: advanced
status: docs-checked
description: "jira_configs fields: api_url and api_type, project, summary and description templates, labels, priority, resolve and reopen transitions, fields."
sources: ["https://prometheus.io/docs/alerting/latest/configuration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# jira_configs

Alertmanager creates and updates Jira issues via REST API v2 or v3. Both have the same feature set; v2 supports Wiki Markup for descriptions and v3 supports Atlassian Document Format. The default `jira.default.description` template only works with v2. Only tested against Jira Cloud; Data Center may work but is not guaranteed.

```yaml
jira_configs:
- api_url: https://company.atlassian.net/rest/api/2/
  project: OPS
  issue_type: Bug
  resolve_transition: Done
  reopen_transition: Reopen
  reopen_duration: 2h
  labels: ['alertmanager', '{{ .CommonLabels.severity }}']
  http_config:
    basic_auth: {username: me@example.org, password_file: /path/to/pat}
```

Fields:
- `api_url`: full API path required; default `global.jira_api_url`. `api_type`: `auto` (default), `cloud` or `datacenter`.
- `project`: project key (required). `issue_type`.
- `summary` and `description`: each has `template` and `enable_update` (default `true`; false stops updating an existing issue).
- `priority`, `labels`: template strings.
- `resolve_transition`: target status must have category done. `reopen_transition`: target must not be done. Names can be localized.
- `wont_fix_resolution`: with `reopen_transition`, ignore issues with that resolution. `reopen_duration`: reopen if not older than this, by `resolutiondate`.
- `fields`: other and custom fields, e.g. `components: { name: "Monitoring" }`.

Auth: Jira Cloud uses `basic_auth` with email and PAT; Data Center uses `authorization` credentials.

## Checked

2026-11-03. Confirmed against the Alertmanager Configuration page (prometheus.io/docs/alerting/latest/configuration): jira_config fields, API v2/v3 note, auth notes.

Method: documentation only; no commands were run.
