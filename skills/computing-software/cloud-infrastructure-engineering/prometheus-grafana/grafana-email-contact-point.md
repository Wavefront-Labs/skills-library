---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.grafana-email-contact-point
name: grafana-email-contact-point
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [email-contact-point, smtp-config, grafana-contact-points, notification-templates, grafana-alerting]
level: practitioner
status: gated
description: "Configure Grafana email notifications: SMTP settings in grafana.ini, the email contact point (addresses, single email), templated subject/body and delivery troubleshooting."
sources: ["https://grafana.com/docs/grafana/latest/alerting/configure-notifications/manage-contact-points/integrations/configure-email/", "https://grafana.com/docs/grafana/latest/setup-grafana/configure-grafana/#smtp", "https://grafana.com/docs/grafana/latest/alerting/configure-notifications/template-notifications/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Email contact point

## SMTP (grafana.ini or env)
```ini
[smtp]
enabled = true
host = smtp.example.com:587
user = grafana@example.com
password = $__file{/etc/secrets/smtp-password}
from_address = grafana@example.com
from_name = Grafana Alerts
startTLS_policy = MandatoryStartTLS
```
Env form: `GF_SMTP_ENABLED=true`, `GF_SMTP_HOST=...`, `GF_SMTP_FROM_ADDRESS`, `GF_SMTP_FROM_NAME`, `GF_SMTP_STARTTLS_POLICY` (all used here). Restart required. `NoStartTLS` against a plain local SMTP server worked; `MandatoryStartTLS` and the `$__file{...}` password form were not run (gated: unconfirmed, source is paywalled or blocked). The key names `host`, `user`, `password`, `from_address`, `from_name`, `startTLS_policy`, `cert_file`, `key_file`, `skip_verify` all exist in the `[smtp]` section of Grafana 13.2.4 `defaults.ini`.

## Contact point
Alerting > Contact points > Add > Email:
- Addresses: separated by `;` or newlines (`a@example.test;b@example.test` ran).
- "Single email" (`singleEmail: true`): one email to all addresses instead of one per address (one message with `To: a@example.test, b@example.test` arrived; the per-address default was not run).
- Optional message and subject, which accept notification templates:
```
{{ define "custom.email.subject" }}[{{ .Status | toUpper }}] {{ .CommonLabels.alertname }} ({{ len .Alerts.Firing }} firing){{ end }}
```
Reference it in the Subject field as `{{ template "custom.email.subject" . }}`. Run through file provisioning (template plus an `email` contact point with `subject`), an alert arrived with `Subject: [FIRING] email-rule (1 firing)` and the sender `"Grafana Alerts" <grafana@example.test>`. In 13.2.4 the old `POST /api/alertmanager/grafana/config/api/v1/receivers/test` is gone (`This endpoint has been removed`; use `/apis/notifications.alerting.grafana.app/v1beta1/namespaces/default/receivers/<name>/test`).

## Test
"Test" button on the contact point sends a test notification with sample data (UI button not clicked; the replacement API above rejected my request body, so test notifications were not exercised) (gated: unconfirmed, source is paywalled or blocked).

## Troubleshooting
- Check the Grafana log for the notifier error (auth failed, TLS handshake); the logger name was not verified (gated: unconfirmed, source is paywalled or blocked).
- `x509` errors: corporate relay with private CA; fix the trust store, or set `cert_file`/`key_file` (client certificate) as needed; `skip_verify = true` only as a temporary diagnostic.
- Delivered but not received: SPF/DKIM for the from domain, spam folders, relay restrictions.

## Gotchas
- Email is a poor pager; use it for tickets/digests and route pages to an on-call tool.
- Grafana Cloud has its own SMTP; self-hosted needs a relay (SES, SendGrid, Postfix).

## Verify
- [ ] Test notification arrives with the templated subject.

## Checked
Environment: Windows 11, Grafana OSS 13.2.4 with `GF_SMTP_*` env vars pointing at a local aiosmtpd server (no TLS).
- Ran the email contact point end to end: subject template, `;`-separated addresses, `singleEmail`, sender name and address; read the `[smtp]` keys from `defaults.ini`; confirmed the removed receivers/test endpoint.
- Items marked gated were not run, so the skill is `gated`.
