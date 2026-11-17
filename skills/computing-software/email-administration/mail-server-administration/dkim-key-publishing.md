---
id: computing-software.email-administration.mail-server-administration.dkim-key-publishing
name: dkim-key-publishing
category: computing-software
field: email-administration
product: mail-server-administration
tags: [dkim-key-publishing, dkim-dns-record, domainkey, dkim-selector-record]
level: practitioner
status: docs-checked
description: "Publish a DKIM public key as a TXT record at selector._domainkey, handle long keys and test it."
sources:
  - https://www.rfc-editor.org/rfc/rfc6376
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dkim key publishing

**Goal:** a record verifiers can parse.
## Steps
1. Name: `mail2026._domainkey.example.com. TXT "v=DKIM1; p=<base64 public key>"`. The verifier queries `<s=>._domainkey.<d=>` taken from the DKIM-Signature.
2. If the key does not fit in one string, split it into several quoted strings in one TXT record; verifiers concatenate the strings with no whitespace. The RFC's own example splits a `p=` value across lines this way.
3. Publish exactly one TXT record per selector name; with several records in the RRset the result is undefined.
4. Signers must use RSA keys of at least 1024 bits for long-lived keys, and verifiers must be able to validate keys from 512 to 2048 bits, so do not go above 2048 bits without checking your receivers.
## Failure modes
- Pasted line breaks or stray spaces inside the key value make the key unusable.
- The `t=y` flag means the domain is testing DKIM: verifiers must not treat mail from a signer in testing mode differently from unsigned mail. Remove it when live.
## Verify
- `dig +short TXT mail2026._domainkey.example.com` returns the key, as one record.

## Checked

2026-11-09. Confirmed on RFC 6376: the _domainkey namespace (section 3.6.2.1), TXT string concatenation and uniqueness per selector (3.6.2.2), the t=y testing flag, key size rules (3.3.3), and the split example in the appendix. Removed: opendkim-testkey and its output, the claim that 2048-bit keys exceed 255 characters and that DNS providers join strings (not stated by the RFC), the one-hour TTL advice, k=rsa, and the boilerplate Postfix/Dovecot notes.

Method: documentation only; no commands were run.
