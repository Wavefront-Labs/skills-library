---
id: computing-software.networking-hardware-and-wireless.asterisk.stir-shaken-attestation-and-verification
name: stir-shaken-attestation-and-verification
category: computing-software
field: networking-hardware-and-wireless
product: asterisk
tags: [networking-hardware-and-wireless, asterisk, stir-shaken, attestation, verification, identity-header, stir-shaken-conf, passport, caller-id, tn]
level: advanced
status: docs-checked
description: "Configure STIR/SHAKEN in stir_shaken.conf: attestation levels A/B/C, tn, verification and profile objects, effective profiles, and listed deviations."
sources:
  - https://docs.asterisk.org/Deployment/STIR-SHAKEN/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# STIR/SHAKEN
Everything is configured in `stir_shaken.conf` (the sample is heavily commented). This describes the refactor of 1Q2024.

**Attestation** (outbound) adds a signed SIP `Identity` header. Levels: **A** full (you originate the call, know the customer, and verified their number), **B** partial (no verified number association), **C** gateway (you only pass the call on). The signing key and certificate usually come from your upstream provider with your DIDs.

**Verification** (inbound) must not be trusted blindly. The checks the page lists (most from ATIS-1000074) include: HTTPS certificate URL that does not resolve to special-purpose addresses; certificate retrieved and valid now; traceable to a trusted CA; CRL extension present and certificate not revoked; TNAuthList containing an SPC; CN of the form `SHAKEN <SPC>` matching it; signature verifies; `iat` and the SIP Date header close to now (`max_iat_age` and `max_date_header_age`, default 15 s); caller ID matches P-Asserted-Identity or From. On failure you may accept the call, accept with error data, or reject with specific 4XX codes.

Object types:
- `attestation` (one only; absent means attestation is globally disabled): `global_disable`, `private_key_file` (not group or world accessible), `public_cert_url`, `check_tn_cert_public_url` (network intensive), `attest_level`, `send_mky`. All but `global_disable` can be overridden per profile or tn.
- `tn`: one per caller-id; may be realtime (`stir_tn`).
- `verification` (one only).
- `profile`: set on a PJSIP endpoint with `stir_shaken_profile`; `endpoint_behavior` is `off`, `attest`, `verify` or `on`; most attestation and verification options can be overridden.

`stir_shaken show eprofiles` lists effective profiles.

Deviations: the destination TN is not validated; only the full PASSporT form is supported; certificate validation is basic (CA, validity dates and TNAuthList presence are checked, the Common Name content is not, and only CRLs configured in `stir_shaken.conf` are used, not the certificate's CRL URI); whether an SPC has authority over a telephone number cannot be checked.

## Checked
2026-11-09: read the cited STIR-SHAKEN page in full and confirmed the attestation levels, verification checks, failure options, object types and parameters, eprofiles command and the listed deviations. Corrected the verification description to say the CN content and the certificate's own CRL URI are not checked by Asterisk, and added the endpoint_behavior values and iat and Date defaults.

Method: documentation only; no commands were run.
