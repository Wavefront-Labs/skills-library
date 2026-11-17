---
id: computing-software.cloud-infrastructure-engineering.fluentd.transport-section-tls
name: transport-section-tls
category: computing-software
field: cloud-infrastructure-engineering
product: fluentd
tags: [cloud-infrastructure-engineering, fluentd, transport-section, tls, certificates, private-ca, linger-timeout]
level: advanced
status: docs-checked
description: "Set up the Fluentd transport section for tcp, udp or tls: TLS versions and ciphers, CA-signed or generated certificates, client_cert_auth, linger_timeout."
sources:
  - https://docs.fluentd.org/configuration/transport-section
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fluentd transport section
For plugins using the `server` or `http_server` helper. Argument selects the protocol: `<transport tcp>` (default), `udp`, or `tls`.

General:
- `linger_timeout` (tcp, tls; since 1.14.6; default 0): 0 sends RST instead of FIN to avoid many TIME_WAIT connections; a positive value sends FIN. Windows always sends FIN.
- `receive_buffer_size` (since 1.18.0, `SO_RCVBUF`).

TLS settings:
- `version` (default `TLSv1_2`); to accept several, use `min_version` / `max_version` (`TLS1_1`, `TLS1_2`, `TLS1_3` when the system supports it).
- `ciphers` default `"ALL:!aNULL:!eNULL:!SSLv2"`; `insecure` default false; `ensure_fips` (since 1.18.0) aborts if FIPS mode is unsupported.

Public CA certificate:
```
<transport tls>
  cert_path /path/to/fluentd.crt
  private_key_path /path/to/fluentd.key
  private_key_passphrase YOUR_PASSPHRASE
</transport>
```
plus `ca_path`, `client_cert_auth` (reject requests without a valid client certificate) and `cert_verifier`.

Private CA: `ca_cert_path`, `ca_private_key_path`, `ca_private_key_passphrase`. Generated or self-signed: `generate_private_key_length` (2048), `generate_cert_country` (US), `generate_cert_state` (CA), `generate_cert_locality` (Mountain View), `generate_cert_common_name`, `generate_cert_expiration` (10 years), `generate_cert_digest` (`sha256`; also `sha1`, `sha384`, `sha512`).

## Checked

2026-11-04: read the fetched text of https://docs.fluentd.org/configuration/transport-section and confirmed: protocols, linger_timeout, TLS versions, ciphers, certificate parameters and generated-certificate defaults. Removed or reworded: nothing.

Method: documentation only; no commands were run.
