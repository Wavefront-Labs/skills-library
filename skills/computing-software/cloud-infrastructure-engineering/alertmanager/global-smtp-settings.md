---
id: computing-software.cloud-infrastructure-engineering.alertmanager.global-smtp-settings
name: global-smtp-settings
category: computing-software
field: cloud-infrastructure-engineering
product: alertmanager
tags: [alertmanager, smtp, global-config, email-defaults]
level: practitioner
status: docs-checked
description: "Global SMTP defaults in alertmanager.yml: smarthost, from, hello, auth methods, require_tls and implicit TLS, inherited by email_configs."
sources: ["https://prometheus.io/docs/alerting/latest/configuration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Global SMTP settings

The `global` block holds defaults inherited by every email receiver, so SMTP details are written once.

```yaml
global:
  smtp_from: alerts@example.org
  smtp_smarthost: smtp.example.org:587
  smtp_hello: localhost          # default "localhost"
  smtp_auth_username: user
  smtp_auth_password_file: /path/to/smtp-password
  smtp_require_tls: true         # default true
```

Key points from the reference:
- `smtp_smarthost` includes the port. Port 25 is usual, or 587 for SMTP over TLS (STARTTLS).
- `smtp_from` is a template string; `smtp_hello` is the hostname announced to the server.
- Auth: CRAM-MD5, LOGIN and PLAIN are supported. If `smtp_auth_username` is empty, Alertmanager does not authenticate. PLAIN is only supported over TLS.
- `smtp_auth_password` and `smtp_auth_password_file` serve LOGIN and PLAIN; `smtp_auth_identity` serves PLAIN; `smtp_auth_secret` and `smtp_auth_secret_file` serve CRAM-MD5.
- `smtp_require_tls` defaults to true. Go does not support unencrypted connections to remote SMTP endpoints.
- `smtp_tls_config` sets the default TLS client settings for SMTP receivers.
- `smtp_force_implicit_tls` forces implicit TLS regardless of SMTP port.

Each `email_configs` entry overrides these with its own `from`, `smarthost`, `hello`, `auth_*`, `require_tls` and `tls_config` fields, which default to the matching global value.

## Checked

2026-11-03. Confirmed against the Alertmanager Configuration page (prometheus.io/docs/alerting/latest/configuration): global smtp_* settings and defaults.

Method: documentation only; no commands were run.
