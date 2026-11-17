---
id: computing-software.cybersecurity-defensive.authentik.email-configuration
name: email-configuration
category: computing-software
field: cybersecurity-defensive
product: authentik
tags: [authentik, email, smtp, test-email, tls, ssl-cert-file]
level: practitioner
status: docs-checked
description: "Configure global SMTP for authentik with AUTHENTIK_EMAIL__ variables or Helm email values, choose STARTTLS or SSL, test with ak test_email, and trust a private CA."
sources:
  - https://docs.goauthentik.io/install-config/email/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: working outbound mail for admin notifications, notification rules and Email stages using global settings (stages can instead carry their own SMTP settings). Some hosts block outgoing SMTP ports.

## TLS mode
STARTTLS (often port 587): `AUTHENTIK_EMAIL__USE_TLS=true`, `AUTHENTIK_EMAIL__USE_SSL=false`. Implicit TLS (often port 465): `USE_SSL=true`, `USE_TLS=false`. Plain: both false. Never enable both. Helm uses `email.use_tls` and `email.use_ssl`.

## `.env`
```sh
AUTHENTIK_EMAIL__HOST=localhost
AUTHENTIK_EMAIL__PORT=25
AUTHENTIK_EMAIL__USERNAME=
AUTHENTIK_EMAIL__PASSWORD=
AUTHENTIK_EMAIL__USE_TLS=false
AUTHENTIK_EMAIL__USE_SSL=false
AUTHENTIK_EMAIL__TIMEOUT=10
AUTHENTIK_EMAIL__FROM=authentik@example.com
```
Do not quote the password. In Helm the `email:` block (`host`, `port`, `username`, `password`, `use_tls`, `use_ssl`, `timeout`, `from`) sits under `authentik:`; `from` may be `"authentik <foo@bar.baz>"`.

## Test
```shell
docker compose exec worker ak test_email <to_address>
kubectl exec -it deployment/authentik-worker -c worker -- ak test_email <to_address>
```
Add `-S <stage_name>` to test one Email stage's own settings.

## Google Workspace relay
Host `smtp-relay.gmail.com`, port 587, `USE_TLS=true`, `USE_SSL=false`, timeout 30. In Google set Allowed Senders to `Only addresses in my domains`, authentication to `Only accept mail from the specified IP addresses`, leave Require SMTP Authentication off and select Require TLS encryption (add authentik's outbound IP).

## Private CA
Mount the CA certificate into server and worker and set `SSL_CERT_FILE` to it (Compose: volume `/path/<cert_name>.crt:/etc/ssl/certs/<cert_name>.crt:ro`; Kubernetes: ConfigMap mounted at `/etc/ssl/certs/ca-certificates.crt`).

## Checked

Method: docs-checked 2026-11-09 against https://docs.goauthentik.io/install-config/email/ (read in full).
