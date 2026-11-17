---
id: computing-software.cybersecurity-defensive.network-defence.email-arc
name: email-arc
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [arc, authenticated-received-chain, email-authentication, mailing-lists, email-forwarding, dmarc, email-security]
level: practitioner
status: docs-checked
description: "Handle ARC (Authenticated Received Chain): why forwarding breaks SPF/DKIM, how ARC seals preserve results, trusted ARC sealers in Microsoft 365 and Gmail, and limits."
sources: ["https://datatracker.ietf.org/doc/html/rfc8617", "https://learn.microsoft.com/en-us/defender-office-365/email-authentication-arc-configure", "https://support.google.com/a/answer/175365"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ARC (Authenticated Received Chain)

Forwarders and mailing lists break DMARC: SPF fails (new sending IP) and DKIM breaks if the list
modifies subject/footer. ARC (RFC 8617) lets each intermediary record the authentication results it saw
and seal them, so the final receiver can decide to trust them.

## Headers per hop (instance i=1,2...)
- `ARC-Authentication-Results`: SPF/DKIM/DMARC results the intermediary observed.
- `ARC-Message-Signature`: DKIM-like signature over the message.
- `ARC-Seal`: signature over the ARC headers, with `cv=` (chain validation: none/pass/fail).

## Receiver side
- ARC does not override DMARC on its own; receivers apply local policy: if the chain validates and the sealer is trusted, a DMARC failure can be overridden.
- **Microsoft 365:** Defender portal -> Email authentication settings -> ARC -> add trusted ARC sealers (domains of your legitimate intermediaries, e.g. a third-party security gateway or mailing list service that rewrites mail before EOP).
- **Google Workspace:** see the Google admin help page for ARC and trusted inbound gateways.

## Sender/intermediary side
If you operate a gateway or list server that modifies messages (subject tags, banners, URL rewriting)
before final delivery, enable ARC sealing on it (check your gateway vendor's documentation).

## Gotchas
- Adding every forwarder as trusted lets spoofed mail through any of them; trust only sealers you control or contract.

## Verify
- [ ] Message through the gateway shows `arc=pass` and `compauth=pass reason=130` (ARC override) in M365 headers when DMARC would otherwise fail.

## Checked

2026-10-28. Confirmed against: RFC 8617 (ARC header sets, cv= values, receiver policy); Microsoft Learn 'Configure trusted ARC sealers' (portal path, compauth reason=130 override); Google admin help page on ARC.

Removed as unconfirmed: Gmail automatic-trust claim, OpenARC/SEG support claim, Enhanced Filtering for Connectors gotcha.

Method: documentation only; no commands were run.
