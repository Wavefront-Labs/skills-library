---
id: computing-software.digital-forensics-incident-response.evidence-handling.evidence-transfer-and-shipping
name: evidence-transfer-and-shipping
category: computing-software
field: digital-forensics-incident-response
product: evidence-handling
tags: [evidence-transfer, chain-of-custody, encrypted-transfer, courier, dfir]
level: practitioner
status: draft
description: "Transfer evidence between parties safely: hand-carry vs courier, encrypted drives and secure file transfer, hash verification on receipt, and custody records."
sources: ["https://www.swgde.org/documents/published-complete-listing/", "https://www.rfc-editor.org/rfc/rfc3227"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Evidence transfer and shipping

**Goal:** evidence arrives intact, unread by anyone else, with custody documented and
integrity verified at the other end.

## Physical transfer
- Hand-carry by a named person when possible; otherwise a courier with tracking and
  signature on delivery. Record tracking number on the custody form as a transfer row
  ("released to courier X, tracking Y").
- Package: sealed evidence bag inside padded box, outer box unmarked as evidence; anti-static
  and shock protection; copy of custody form inside, original kept by sender.
- Encrypt drives being shipped (hardware-encrypted drive or VeraCrypt/BitLocker To Go);
  send the password by a different channel.

## Electronic transfer
- SFTP or a managed secure file transfer with per-case accounts and expiring access; avoid
  email and consumer file sharing.
- Encrypt the archive (7-Zip AES-256 with header encryption or GPG) before upload when the
  channel's provider is not trusted.
- Large images: split with hashes per segment (E01 segments already carry internal hashes).

## On receipt
1. Inspect seals; photograph package and seals before opening.
2. Recompute hashes and compare to sender's values; record result on custody form.
3. Log into evidence storage.

## Gotchas
- Cross-border transfers of personal data (GDPR Chapter V) and export controls on encryption
  in a few countries; involve legal for international shipments.
- Customs opening packages breaks seals; note it and re-verify hashes.

## Verify
Sender and receiver custody records match, hash comparison passed, and the transfer
method is documented.
