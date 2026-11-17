---
id: computing-software.messaging-and-integration.celery.celery-message-signing-auth-serializer
name: celery-message-signing-auth-serializer
category: computing-software
field: messaging-and-integration
product: celery
tags: [celery-conf-serializers, celery-message-signing, celery, security, auth-serializer, setup-security, x509, signing, pickle]
level: practitioner
status: docs-checked
description: "Sign Celery messages with the auth serializer and public-key certificates, restrict accept_content, and call setup_security."
sources:
  - https://docs.celeryq.dev/en/stable/userguide/configuration.html
  - https://docs.celeryq.dev/en/stable/userguide/security.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Sign Celery messages with the auth serializer

Goal: make workers accept only messages signed by trusted clients.

Celery uses the `cryptography` library: clients sign with a private key, workers verify with a public certificate. Certificates are best signed by a Certificate Authority but may be self-signed.

## Steps
1. Set `task_serializer='auth'`.
2. Set `accept_content=['auth']` so workers only accept signed messages.
3. For events, set `event_serializer='auth'`.
4. Point at the files: `security_key`, `security_certificate`, `security_cert_store` (a directory or glob, e.g. `/etc/certs/*.pem`).
5. Optional: `security_digest` (default `sha256`, added 4.3); `security_key_password` (5.3.0+) if the private key is encrypted.
6. Call `setup_security()`; this also disables all insecure serializers so the worker will not accept untrusted content types.

```python
app = Celery()
app.conf.update(
    security_key='/etc/ssl/private/worker.key',
    security_certificate='/etc/ssl/certs/worker.pem',
    security_cert_store='/etc/ssl/certs/*.pem',
    security_digest='sha256',
    task_serializer='auth',
    event_serializer='auth',
    accept_content=['auth']
)
app.setup_security()
```

(The docs example omits some commas between the first keyword arguments; add them as above.)

## Gotchas
- Relative paths are allowed but absolute paths are recommended.
- The `auth` serializer does not encrypt message contents; enable encryption separately if needed.
- If the result is stored unsigned in the result backend, use `result_accept_content` to accept a different serializer for results.
- Signing does not replace broker security: put a firewall in front of the broker, use fine-grained access control where supported (e.g. RabbitMQ), and enable `broker_use_ssl` for end-to-end SSL where the transport supports it. By default workers trust broker data has not been tampered with.

## Checked

2026-11-07. Confirmed against the Celery 5.7.0 stable docs (userguide/configuration.html, userguide/security.html): the settings, defaults, parameters, code and wording kept in this skill. These are the pages' own claims, not independent tests. Nothing needed removing.

Method: documentation only; no commands were run.
