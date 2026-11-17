---
id: computing-software.systems-network-administration.wireshark.pcap-evidence-chain-of-custody
name: pcap-evidence-chain-of-custody
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, chain-of-custody, pcap-evidence, network-forensics, hashing]
level: practitioner
status: docs-checked
description: "Handle packet captures as evidence: hashing with capinfos, chain-of-custody records, restricted access and documented, verifiable derived files."
sources:
  - https://www.rfc-editor.org/rfc/rfc3227
  - https://www.wireshark.org/docs/man-pages/capinfos.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Evidence handling and hashing of captures

Captures used in incident response, HR or legal matters must be provably unaltered. RFC 3227
(Evidence Collection and Archiving) is the baseline for the habits below.

## At collection
1. Record who captured, where (device, interface, SPAN source), when, and the command and filters
   used. RFC 3227 says to record the extent of the system's clock drift and to document each step,
   including who was present.
2. Hash immediately. RFC 3227 advises generating checksums and cryptographically signing collected
   evidence where feasible, without altering the evidence. `capinfos -H <file>` displays the SHA256
   and SHA1 hashes of a capture (the man page notes SHA1 output may be removed in the future);
   `capinfos -a` and `-e` show earliest and latest packet timestamps.
3. Store the original securely. RFC 3227 requires evidence to be strictly secured, access to be
   extremely restricted and documented, and unauthorised access to be detectable. Prefer commonly
   used media for archiving.

## Chain of custody
Document: where, when and by whom the evidence was discovered and collected; where, when and by whom
it was handled or examined; who had custody and for what period, and how it was stored; and, when
custody changed, when and how the transfer occurred.

## During analysis
- Work on a copy. Never save over the original in Wireshark; derived files (filtered exports, sliced
  time windows) get new names and their own hashes.
- Log each derivation: source hash, command used, output hash.

## Documenting findings
Reference packets by frame number AND timestamp AND file hash so others can reproduce them.
Export specific packets to a separate capture file for exhibits.

## Pitfalls
- Ring buffer rotation can overwrite evidence: stop or copy out as soon as the incident is known.
- Clock differences between capture points: document offsets rather than editing timestamps in the
  original.
- Captures contain third-party data; restrict access and record who viewed them.

## Verify
- [ ] Re-hashing the stored original matches the collection hash, and every exhibit traces back to it.

## Checked
Method: docs-checked 2026-11-09 against RFC 3227 (sections 3 and 4 read: collection steps, clock drift, checksums, chain of custody, archiving) and the capinfos man page (-H, -a, -e options). The NIST SP 800-86 landing page was dropped as a source. Dropped unconfirmed items: sha256sum and chmod commands, WORM object lock, editcap options, and the packet-comment advice.
