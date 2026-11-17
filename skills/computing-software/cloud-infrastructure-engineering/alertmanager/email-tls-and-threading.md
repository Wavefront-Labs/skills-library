---
id: computing-software.cloud-infrastructure-engineering.alertmanager.email-tls-and-threading
name: email-tls-and-threading
category: computing-software
field: cloud-infrastructure-engineering
product: alertmanager
tags: [alertmanager, email-threading, implicit-tls, force-implicit-tls]
level: advanced
status: docs-checked
description: "Email receiver force_implicit_tls versus port auto-detection, and threading options enabled and thread_by_date for grouping emails in one thread."
sources: ["https://prometheus.io/docs/alerting/latest/configuration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Email implicit TLS and threading

Implicit TLS: `force_implicit_tls` (global `smtp_force_implicit_tls`, per receiver `force_implicit_tls`) controls direct TLS connections.
- `true`: use implicit TLS (direct TLS connection) on any port. The reference calls this recommended for security.
- unset (nil, default): auto-detect from the port for backward compatibility. Port 465 uses implicit TLS; other ports use explicit TLS (STARTTLS).

```yaml
receivers:
  - name: email-implicit-tls
    email_configs:
      - to: oncall@example.org
        smarthost: smtp.example.com:8465
        force_implicit_tls: true
  - name: email-default
    email_configs:
      - to: oncall@example.org
        smarthost: smtp.example.com:465   # auto-detects implicit TLS
```

Threading puts notifications for the same alert group in one email thread:

```yaml
threading:
  enabled: true
  thread_by_date: daily
```

- `enabled`: default `false`.
- `thread_by_date`: the date granularity used to thread. Accepted values are `daily` (default) and `none`; `none` groups by alert group key with no date.

With `daily`, the thread key includes the current date; with `none` it is only the alert group key.

## Checked

2026-11-08. Confirmed against the Alertmanager configuration reference (email_configs): force_implicit_tls semantics (true forces implicit TLS on any port, nil auto-detects, 465 implicit, others explicit), global smtp_force_implicit_tls, and threading enabled (default false) and thread_by_date (daily default, none).

Method: documentation only; no commands were run.
