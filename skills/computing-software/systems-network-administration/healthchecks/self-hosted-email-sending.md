---
id: computing-software.systems-network-administration.healthchecks.self-hosted-email-sending
name: self-hosted-email-sending
category: computing-software
field: systems-network-administration
product: healthchecks
tags: [healthchecks, smtp-settings, implicit-tls, explicit-tls, email-host]
level: practitioner
status: docs-checked
description: "Configure outgoing SMTP for self-hosted Healthchecks: host, port 465 implicit TLS versus port 587 explicit TLS, credentials and the related settings."
sources:
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/self_hosted.md
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/self_hosted_configuration.md
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Healthchecks needs SMTP for login links and alerts. Without `EMAIL_HOST`, no email can be sent.

Implicit TLS (recommended; preferred under RFC 8314):
- `EMAIL_PORT=465`, `EMAIL_USE_SSL=True`, `EMAIL_USE_TLS=False`

Explicit TLS:
- `EMAIL_PORT=587`, `EMAIL_USE_TLS=True`

Common to both: `DEFAULT_FROM_EMAIL` (sender address), `EMAIL_HOST` (SMTP server), `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`.

Defaults: `EMAIL_PORT` 587, `EMAIL_USE_TLS` True, `EMAIL_USE_SSL` False, `DEFAULT_FROM_EMAIL` healthchecks@example.org.

Secrets can come from a file: `EMAIL_HOST_PASSWORD_FILE` supplies `EMAIL_HOST_PASSWORD` and takes precedence.

`EMAIL_USE_VERIFICATION` (default True) requires users to verify addresses added to email integrations by clicking a link.

Use a TLS certificate, not an SSL one. These settings build the `settings.MAILERS` dictionary. `hc/local_settings.py` can override any Django setting and takes precedence over environment variables.

## Checked

2026-11-04. Confirmed against the Healthchecks self-hosted page, server configuration page and README: implicit TLS on 465 and explicit TLS on 587 settings, the RFC 8314 preference, defaults for EMAIL_PORT, EMAIL_USE_TLS, EMAIL_USE_SSL and DEFAULT_FROM_EMAIL, EMAIL_HOST_PASSWORD_FILE precedence, EMAIL_USE_VERIFICATION, MAILERS construction and local_settings.py precedence. Nothing removed.

Method: documentation only; no commands were run.
