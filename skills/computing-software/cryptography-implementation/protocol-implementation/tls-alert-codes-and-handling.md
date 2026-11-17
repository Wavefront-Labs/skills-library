---
id: computing-software.cryptography-implementation.protocol-implementation.tls-alert-codes-and-handling
name: tls-alert-codes-and-handling
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [protocol-implementation, cryptography-implementation, tls-alerts, tls-1-3, alert-protocol, handshake-failure, close-notify, troubleshooting, rfc-8446]
level: practitioner
status: docs-checked
description: "Read and emit TLS alerts correctly: RFC 8446 alert codes and likely causes, fatal versus close_notify semantics, and logging alerts for diagnosis."
sources: ["https://www.rfc-editor.org/rfc/rfc8446"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TLS alert codes and handling

In TLS 1.3 all defined alerts, and all unknown ones, are treated as fatal (RFC 8446 section 6.2), except the closure
alert `close_notify` and the generally-warning `user_canceled` (section 6.1). On a fatal alert both parties close the
connection. The alert tells you which side gave up and roughly why.

## Alerts and what usually causes them
Codes are from the RFC 8446 AlertDescription enum; the "usual cause" column is practitioner guidance.

| Code | Alert | Usual cause |
|---|---|---|
| 0 | close_notify | Orderly shutdown (absence = possible truncation) |
| 10 | unexpected_message | State machine bug, middlebox injecting data |
| 20 | bad_record_mac | Key mismatch, corruption, wrong cipher state |
| 40 | handshake_failure | No common cipher suite, group or signature algorithm |
| 42 / 46 | bad_certificate / certificate_unknown | Peer rejected your certificate (expired, wrong EKU, untrusted) |
| 45 | certificate_expired | Expired certificate in chain |
| 48 | unknown_ca | Chain does not lead to a trusted root; missing intermediate |
| 47 | illegal_parameter | Malformed or inconsistent field (bad key share, wrong curve point) |
| 50 | decode_error | Message could not be parsed (truncated, oversized) |
| 51 | decrypt_error | Handshake signature or Finished verification failed |
| 70 | protocol_version | No common TLS version |
| 71 | insufficient_security | Server requires stronger parameters |
| 80 | internal_error | Bug or resource failure on the sender |
| 86 | inappropriate_fallback | Downgrade-fallback retry detected |
| 109 | missing_extension | Required extension absent (e.g. supported_versions, key_share) |
| 112 | unrecognized_name | SNI name not served |
| 116 | certificate_required | Server needed a client certificate |
| 120 | no_application_protocol | No ALPN overlap |

## Reading library error text
Library messages usually say whether the alert was received from the peer or decided locally. A peer-sent alert means
the peer rejected something you sent; a local error means your side decided and will normally have sent an alert.

## Emitting alerts in your own code or config
- Send the most specific alert that applies; the RFC says to send the alert named in each rule when it sends any.
- Each party must send `close_notify` before closing its write side unless it already sent an error alert. Treat EOF
  without it as possible truncation where TLS delimits the data.

## Verify
- [ ] Logs capture alert direction (sent/received) and code for failed handshakes.
- [ ] Runbook maps top alert codes to fixes.

## Checked
2026-11-01: alert names and numeric codes, fatal semantics, close_notify and user_canceled behaviour confirmed against
RFC 8446 sections 6, 6.1, 6.2. Removed: ech_required row (not in RFC 8446), OpenSSL error-string examples, the
oracle-avoidance claim and the TLS_FALLBACK_SCSV detail (not confirmed in this batch).
Method: documentation only; no commands were run.
