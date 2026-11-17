---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.email-header-analysis
name: email-header-analysis
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [email-header-analysis, email-forensics, spf, dkim, dmarc, phishing, dfir]
level: practitioner
status: docs-checked
description: "Analyse email headers to trace origin and authenticity: trace-field order, Message-ID, Reply-To, and SPF, DKIM and DMARC results and alignment, with trust limits."
sources: ["https://datatracker.ietf.org/doc/html/rfc5322", "https://datatracker.ietf.org/doc/html/rfc7208", "https://datatracker.ietf.org/doc/html/rfc6376", "https://datatracker.ietf.org/doc/html/rfc7489"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Email header analysis

**Goal:** determine where a message really came from, whether it is authenticated for the
claimed domain, and which path it took.

## Get full headers
Export the complete raw message (for example an `.eml` file or the mail system's "view source" or
message-trace export) rather than a rendered view, so every trace and authentication header is
kept. Hash the export and keep the original.

## Read the trace fields bottom-up
RFC 5322 defines trace fields (including `Received:`) as a block prepended to the message, so
each hop adds its fields above the earlier ones: the **lowest** `Received:` is the first hop.
Anything below the point where your own infrastructure took the message was written by other
parties and can be forged by the sender. Note IPs, host names and timestamps; time gaps between
hops show queuing. The `Message-ID:` holds a single unique identifier and is retained when
trace fields are added in transit, so it is useful for matching a message against logs.

## Authentication results
Rely on the results recorded by the receiving system you trust, not on text supplied by the sender.
- **SPF** (RFC 7208): checks whether the connecting IP is authorised for the domain; results
  include `pass`, `fail`, `softfail` (a weak statement by the domain), `neutral`, `none`,
  `temperror` and `permerror`.
- **DKIM** (RFC 6376): a signature associates the `d=` domain name with a hash of the signed
  content; compare the `d=` domain with the visible From domain.
- **DMARC** (RFC 7489): passes when SPF or DKIM passes **and** the domain aligns with the
  RFC5322.From domain ("Identifier Alignment"; strict or relaxed mode). The domain owner's
  published policy is `none`, `quarantine` or `reject`, which tells receivers what to do with
  mail that fails.

## Spoofing patterns
- Display name that claims a person but an address on an unrelated domain.
- Lookalike domain (it can have its own valid SPF and DKIM, so authentication only shows the
  sender controls that domain).
- `Reply-To:` differing from `From:`: RFC 5322 says replies go to `Reply-To:` when present,
  so replies can be steered to another mailbox.
- Compromised legitimate account: authentication passes and aligns; look at the sending IP,
  the client, and the sender's mailbox audit logs instead.

## Verify
State origin IP and authentication verdicts from headers added by trusted MTAs only, and
corroborate with message trace logs on your side.

## Checked
Confirmed in the cited RFCs: trace fields prepended as a block, Message-ID retained when trace
fields are added, Reply-To behaviour (RFC 5322); SPF result names including softfail, temperror
and permerror (RFC 7208); DKIM `d=` association (RFC 6376); DMARC alignment and the
none/quarantine/reject policy values (RFC 7489). Removed as not in these pages: mail-client
menu paths, ARC (see the SPF/DKIM/DMARC investigation skill), Microsoft-specific headers
(`compauth`, `X-MS-Exchange-*`), `X-Mailer`, punycode/homoglyph detail and the sample
addresses.
Method: docs-only read of cited pages, 2026-11-08
