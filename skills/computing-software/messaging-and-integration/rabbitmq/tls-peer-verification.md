---
id: computing-software.messaging-and-integration.rabbitmq.tls-peer-verification
name: tls-peer-verification
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, tls-peer-verification]
level: advanced
status: docs-checked
description: "Require client certificates with verify_peer and fail_if_no_peer_cert and optionally map cert identity to users."
sources:
  - https://www.rabbitmq.com/docs/ssl
  - https://www.rabbitmq.com/docs/access-control
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TLS peer verification

**Goal:** Authenticate clients by certificate.

## Steps
1. `ssl_options.verify = verify_peer` and `ssl_options.fail_if_no_peer_cert = true`.
2. Enable `rabbitmq_auth_mechanism_ssl` and add `auth_mechanisms.1 = EXTERNAL` (clients must use the EXTERNAL mechanism).
3. Choose the identity with `ssl_cert_login_from`: `distinguished_name` (default), `common_name`, or `subject_alternative_name`. A user with the extracted name must exist.

## Failure modes
- `fail_if_no_peer_cert = false` accepts clients that present no certificate.

## Verify
- Connect without a certificate and expect rejection.

## Checked

Date: 2026-11-02. Confirmed on the TLS guide (peer verification, `rabbitmq_auth_mechanism_ssl` example) and Access Control guide. Nothing removed except the failure-mode wording, which now matches the guide.

Method: documentation only; no commands were run.
