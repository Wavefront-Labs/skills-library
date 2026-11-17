---
id: computing-software.systems-network-administration.icinga-2.troubleshooting-certificates-and-pki-verify
name: troubleshooting-certificates-and-pki-verify
category: computing-software
field: systems-network-administration
product: icinga-2
tags: [systems-network-administration, icinga-2, troubleshooting, certificates, pki-verify, openssl, ca, csr-signing, ticket-salt]
level: practitioner
status: docs-checked
description: Verify Icinga 2 TLS certificates with icinga2 pki verify and openssl, check the shared CA and CN, and troubleshoot CSR auto-signing tickets and on-demand signing with ca list.
sources:
  - https://icinga.com/docs/icinga-2/latest/doc/15-troubleshooting/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Troubleshooting certificates
Tools: `openssl` (Linux/Unix, or `openssl.exe` on Windows) and `sslscan`. Certificates live in `/var/lib/icinga2/certs`.

**What a good certificate has:** version 3; issuer your CA (default `Icinga CA` for CLI-generated and auto-signed certificates); not expired; subject CN matching the endpoint name and FQDN; basic constraint `CA:TRUE` for `ca.crt` and `CA:FALSE` for node certificates; a Subject Alternative Name with the resolvable DNS name (needed for the REST API and browsers). Master, satellites and agents must be signed by the same CA; compare each node's `ca.crt` with the master's.

**`icinga2 pki verify`** (since 2.12) works without OpenSSL, also on Windows. `--cert <file>` prints the certificate. Exit codes follow the Plugin API, so check `echo $?`.

**Signing failures:**
- Auto-signing (ticket): ticket invalid, or the `api` feature lacks `ticket_salt` set to the `TicketSalt` constant created by the wizards.
- A 3+ level cluster: check the satellite forwarded the CSR and the master processed it.
- A directly connected master may be too slow; the connection then closes without a certificate response.
- On-demand signing: `icinga2 ca list` shows only pending requests since v2.11; add `--all` for signed ones. Old requests are purged after one week.

**Ciphers:** since v2.11 defaults are hardened, with TLS 1.2 as minimum.

## Checked

2026-11-04. Confirmed against the Icinga 2 troubleshooting chapter: certificate checklist (Icinga CA, CA:TRUE/FALSE, SAN), pki verify since 2.12 with --cert and Plugin API exit codes, ticket_salt, ca list --all since v2.11, one week purge, TLS 1.2 minimum.

Method: documentation only; no commands were run.
