---
id: computing-software.cryptography-implementation.protocol-implementation.certificate-validity-and-clock-skew
name: certificate-validity-and-clock-skew
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [protocol-implementation, cryptography-implementation, clock-skew, validity-period, x509, ntp, certificate-validation]
level: practitioner
status: docs-checked
description: "Handle certificate validity periods and clock skew: notBefore backdating, client clock errors, authenticated time (NTS) on devices, and diagnosing not yet valid errors."
sources: ["https://www.rfc-editor.org/rfc/rfc5280#section-4.1.2.5", "https://www.rfc-editor.org/rfc/rfc8915"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Certificate validity and clock skew

## The problem
RFC 5280 section 4.1.2.5 defines the validity period as the interval from notBefore to notAfter inclusive, during
which the CA warrants it will maintain status information. Validators compare the current time with that interval,
so a device with a wrong clock sees `not yet valid` or `expired` for a good certificate.

## Issuer side
- Set notBefore slightly in the past for freshly issued certificates so clients with small clock lag accept them;
  keep the backdating small and consistent with your CA policy.
- With short-lived certificates (hours or days), clock skew matters more: renew well before expiry.

## Client side
- Keep time synced. RFC 8915 defines Network Time Security (NTS), which authenticates NTP time with TLS-derived keys.
- Embedded devices without a battery-backed clock start at a default date: obtain trustworthy time before the first
  TLS connection, or use a build-time floor (`if now < BUILD_TIME then now = BUILD_TIME`).
- Do not disable time checks to work around skew. Use a validation-time override only when verifying historical
  data, and only via your TLS or X.509 library's documented option.

## Diagnose
Compare the host clock (UTC) with the certificate's notBefore and notAfter values, then re-run validation with the
correct time. Typical errors say the certificate is not yet valid or has expired.

## Verify
- [ ] Monitoring alerts on host clock offset; device firmware syncs time before first TLS connection.

## Checked
Date: 2026-11-01. Confirmed: RFC 5280 section 4.1.2.5 (validity period notBefore/notAfter) and RFC 8915 (Network
Time Security for NTP). Removed: the 2017 Chrome clock-error study claim (page not found), the Let's Encrypt one-hour
backdate and CT/audit remarks, Roughtime, Go and OpenSSL option names, OpenSSL error numbers, the monitoring threshold,
and the shell commands.
Method: documentation only; no commands were run.
