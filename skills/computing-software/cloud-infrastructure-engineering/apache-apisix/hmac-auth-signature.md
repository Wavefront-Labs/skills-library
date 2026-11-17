---
id: computing-software.cloud-infrastructure-engineering.apache-apisix.hmac-auth-signature
name: hmac-auth-signature
category: computing-software
field: cloud-infrastructure-engineering
product: apache-apisix
tags: [apache-apisix, apisix, hmac-auth, hmac, signature, authentication, digest, plugin]
level: advanced
status: docs-checked
description: "Configure APISIX hmac-auth: key_id and secret_key, allowed algorithms, clock_skew, signed_headers, body Digest validation and how the signing string is built."
sources:
  - https://raw.githubusercontent.com/apache/apisix/master/docs/en/latest/plugins/hmac-auth.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# hmac-auth signature

Consumer credential: `key_id` (matches `keyId` in the header) and `secret_key` (stored encrypted).

Route attributes and defaults:
- `allowed_algorithms`: `hmac-sha1`, `hmac-sha256`, `hmac-sha512`.
- `clock_skew`: 300 seconds between the `Date` header and APISIX time.
- `signed_headers`: `["date"]`; an empty array removes the requirement.
- `validate_request_body`: false; true checks a `Digest` header against the SHA-256 base64 body digest.
- `max_req_body_size`: 67108864; larger bodies get 413.
- `hide_credentials`: false; `anonymous_consumer`; `realm`: `hmac`.

Client sends `Authorization: Signature keyId="...",algorithm="hmac-sha256",headers="@request-target date",signature="..."`.

Signing string, built from the `headers` list in order, each line ending with a newline:
- `@request-target` becomes `<lowercase method> <path>`.
- Other headers become `<lowercase name>: <value>`.

APISIX looks up the consumer by `keyId`, computes the HMAC with `secret_key`, base64-decodes the supplied signature and compares, then checks `Date` against `clock_skew`.

Body digest header form: `SHA-256=<base64 of sha256(body)>`. A missing or mismatched digest returns 401 `{"message":"client request can't be validated"}`.

On success the upstream gets `X-Consumer-Username` and `X-Credential-Identifier`.

## Checked

2026-11-04. Confirmed against the APISIX hmac-auth plugin page: key_id and secret_key, allowed_algorithms, clock_skew 300, signed_headers default date, validate_request_body with Digest and max_req_body_size 413, hide_credentials, anonymous_consumer, realm, the Signature header format, the 401 message, upstream headers. Nothing removed.

Method: documentation only; no commands were run.

