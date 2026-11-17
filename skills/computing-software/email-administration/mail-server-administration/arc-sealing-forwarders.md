---
id: computing-software.email-administration.mail-server-administration.arc-sealing-forwarders
name: arc-sealing-forwarders
category: computing-software
field: email-administration
product: mail-server-administration
tags: [arc-sealing-forwarders, arc, arc-seal, arc-sealing]
level: advanced
status: docs-checked
description: "Add ARC seals when forwarding or running mailing lists so downstream receivers can trust the original authentication results."
sources:
  - https://www.rfc-editor.org/rfc/rfc8617
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Arc sealing forwarders

**Goal:** preserve authentication results across intermediaries (RFC 8617, an Experimental RFC).
## Steps
1. Make your handler act as an ARC validator on receipt and an ARC sealer when sending a message onward that it did not originate.
2. Each hop adds an ARC Set of three header fields sharing one instance tag: ARC-Authentication-Results (AAR), ARC-Message-Signature (AMS) and ARC-Seal (AS). Instance values range from 1 to 50; a new set uses one more than the highest existing instance (1 if there is no chain).
3. Perform all message modifications (including adding DKIM signatures) before sealing.
4. If the most recent AS already reports `cv=fail`, do not add a new set; stop.
5. The chain validation status is `none` (no chain on arrival), `fail` or `pass`. Receivers may use a passing chain to inform local policy for messages that fail authentication because of intermediate processing; it is not an override.
## Failure modes
- A broken or invalid chain gives a `fail` status, and sealers must not seal on top of a latest `cv=fail`.
- Modifying the message after sealing invalidates the seal; seal last.
## Verify
- A forwarded test message shows a chain with one set per ARC-participating hop and a `pass` validation status at a receiver that evaluates ARC.

## Checked

2026-11-09. Confirmed on RFC 8617: the three header fields and ARC Set, instance tag range 1 to 50 and the increment rule, the sealer steps (modifications before sealing, stop when the latest AS is cv=fail), the three chain validation statuses, and that a pass or none chain may inform local policy. Removed: Rspamd, OpenARC and OpenDKIM instructions, the DKIM-style key publishing step and arc=pass wording (not verified in the sections read), and the boilerplate notes.

Method: documentation only; no commands were run.
