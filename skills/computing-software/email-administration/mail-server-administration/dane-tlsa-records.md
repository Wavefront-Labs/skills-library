---
id: computing-software.email-administration.mail-server-administration.dane-tlsa-records
name: dane-tlsa-records
category: computing-software
field: email-administration
product: mail-server-administration
tags: [dane-tlsa-records, dane-smtp, dane, tlsa]
level: advanced
status: docs-checked
description: "Publish DNSSEC-signed TLSA records (usage 3 1 1 recommended) for your MX hosts and roll keys safely under opportunistic DANE (RFC 7672)."
sources:
  - https://www.rfc-editor.org/rfc/rfc7672
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dane tlsa records

**Goal:** DNSSEC-authenticated TLS keys for SMTP (RFC 7672).
## Steps
1. The zone that holds the TLSA records must be DNSSEC signed; senders only use DNSSEC-validated TLSA records. Do not publish validated TLSA records for a server that does not support TLS, because clients read their presence as a commitment to implement STARTTLS.
2. Publish the record at `_25._tcp.<mx-host-name>`, for example `_25._tcp.mail.example.com. TLSA 3 1 1 <SHA-256 digest of the public key>`. RFC 7672 recommends "DANE-EE(3) SPKI(1) SHA2-256(1)" records (that is `3 1 1`), with "DANE-TA(2) Cert(0) SHA2-256(1)" (`2 0 1`) as second choice.
3. A `3 1 1` record need not change across certificate renewals with the same key. With DANE-EE(3) the server certificate's expiry date is ignored by clients, and the validity of the binding comes from the DNSSEC signature on the TLSA record.
4. Key rotation: two TLSA records MUST be published before employing a new key, one matching the current key and one matching the new key. Wait until DNS caches have expired the previous TLSA RRset and its signatures, switch the server to the new key, then remove the record for the retired key.
## Failure modes
- Changing the server key without pre-publishing the new TLSA record: DANE-checking senders cannot authenticate the server.
- Unsigned zones: TLSA records in them are not usable for opportunistic DANE.
## Verify
- Query the TLSA name with a DNSSEC-aware tool and confirm the answer is validated and matches the digest of the key your server presents.

## Checked

2026-11-09. Confirmed on RFC 7672: the _25._tcp TLSA owner name, the recommendation for DANE-EE(3) SPKI(1) SHA2-256(1) and DANE-TA(2) Cert(0) SHA2-256(1) as second choice, no change across renewals with the same key, expiry date ignored for DANE-EE(3), no validated TLSA for servers without TLS, and the section 4 key management rule of two TLSA records. Removed: the OpenSSL digest command, Postfix settings, and the dig and s_client verification lines, none of which are in the RFC, and the boilerplate notes.

Method: documentation only; no commands were run.
