---
id: computing-software.cloud-infrastructure-engineering.alertmanager.email-receiver-fields
name: email-receiver-fields
category: computing-software
field: cloud-infrastructure-engineering
product: alertmanager
tags: [alertmanager, email-config, smtp, html-body]
level: practitioner
status: docs-checked
description: "Fields of email_configs in Alertmanager: to, from, smarthost, auth, require_tls, html and text bodies, and custom headers."
sources: ["https://prometheus.io/docs/alerting/latest/configuration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# email_configs

```yaml
receivers:
- name: team-mails
  email_configs:
  - to: 'team-X+alerts@example.org, team-Y+alerts@example.org'
    send_resolved: true
    headers:
      Subject: '{{ .CommonLabels.alertname }}'
```

Fields:
- `send_resolved`: default `false` for email.
- `to`: required; a comma-separated list of RFC 5322 compliant addresses (template string).
- `from`, `smarthost`, `hello`: default to `global.smtp_from`, `global.smtp_smarthost`, `global.smtp_hello`.
- `auth_username`, `auth_password`, `auth_password_file`, `auth_secret`, `auth_secret_file`, `auth_identity`: default to the matching `global.smtp_auth_*` values. Password and password file are mutually exclusive, as are secret and secret file.
- `require_tls`: default `global.smtp_require_tls`. Go does not support unencrypted connections to remote SMTP endpoints.
- `tls_config`: default `global.smtp_tls_config`.
- `html`: default `'{{ template "email.default.html" . }}'`.
- `text`: optional plain-text body, with no default.
- `headers`: key/value pairs (template strings) that override any headers previously set by the notification implementation.

## Checked

2026-11-03. Confirmed against the Alertmanager Configuration page (prometheus.io/docs/alerting/latest/configuration): email_config fields and defaults. Removed: references to other skills.

Method: documentation only; no commands were run.
