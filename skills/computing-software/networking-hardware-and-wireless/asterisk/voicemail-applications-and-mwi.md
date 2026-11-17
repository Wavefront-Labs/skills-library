---
id: computing-software.networking-hardware-and-wireless.asterisk.voicemail-applications-and-mwi
name: voicemail-applications-and-mwi
category: computing-software
field: networking-hardware-and-wireless
product: asterisk
tags: [networking-hardware-and-wireless, asterisk, voicemail, voicemail-conf, voicemailmain, mwi, mailboxes, incoming-mwi-mailbox, res-external-mwi]
level: practitioner
status: docs-checked
description: "Use VoiceMail and VoiceMailMain (mailbox@context, u b s options) and deliver or receive message waiting indication: PJSIP mailboxes, incoming_mwi_mailbox, res_external_mwi."
sources:
  - https://docs.asterisk.org/Configuration/Applications/Voicemail/
  - https://docs.asterisk.org/Configuration/Applications/Voicemail/Message-Waiting-Indication/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# voicemail applications and mwi
`VoiceMail(mailbox@context,options)`: leave a message. Popular options: `u` (unavailable greeting), `b` (busy greeting), `s` (skip system instructions). Mailboxes are split into voicemail contexts, like dialplan contexts; an omitted context means the `default` one.

`VoiceMailMain(mailbox@context,options)`: owner retrieves messages and sets greetings and PIN. A missing context means `default`. Warning: with option `s` (skip PIN) anyone who can reach that extension can read the mailbox.

MWI to PJSIP endpoints: set `mailboxes` on the endpoint or the aor section (see the res_pjsip module reference).

Receiving MWI from other systems:
- chan_sip: outbound subscriptions via `mwi => user[:secret[:authuser]]@host[:port]/mailbox` (UDP only) or unsolicited NOTIFY storing a virtual mailbox; other peers use `mailbox=<value>@SIP_Remote`.
- `res_external_mwi`: an API for other systems to report MWI; mutually exclusive with `app_voicemail`, so load only one.
- chan_pjsip: endpoint `incoming_mwi_mailbox = <mailbox>@<context>` applies unsolicited `message-summary` NOTIFYs from that endpoint (the page says it was introduced in 13.18.0 and 14.7.0).
- Outbound SIP subscriptions are not available in res_pjsip.

The page marks its MWI content as under construction.

## Checked
2026-11-09: read the Voicemail and Message Waiting Indication pages in full and confirmed the application parameters and options, the s-option warning, the PJSIP mailboxes option, the chan_sip mwi and unsolicited_mailbox forms, res_external_mwi exclusivity, incoming_mwi_mailbox and its versions. Removed the claim that contexts are defined in voicemail.conf (not on the cited pages).

Method: documentation only; no commands were run.
