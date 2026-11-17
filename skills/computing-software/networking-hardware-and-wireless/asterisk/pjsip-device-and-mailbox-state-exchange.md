---
id: computing-software.networking-hardware-and-wireless.asterisk.pjsip-device-and-mailbox-state-exchange
name: pjsip-device-and-mailbox-state-exchange
category: computing-software
field: networking-hardware-and-wireless
product: asterisk
tags: [networking-hardware-and-wireless, asterisk, pjsip, device-state, mailbox-state, publish, mwi, clustering, asterisk-publication]
level: advanced
status: docs-checked
description: "Share device and mailbox state between Asterisk instances over PJSIP with outbound-publish and asterisk-publication objects and optional regex filters."
sources:
  - https://docs.asterisk.org/Configuration/Channel-Drivers/SIP/Configuring-res_pjsip/Exchanging-Device-and-Mailbox-State-Using-PJSIP/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pjsip device and mailbox state exchange
The `res_pjsip_publish_asterisk` module sets up a unidirectional or bidirectional relationship in which state changes are sent to the peer in a PUBLISH with an Asterisk-specific body.

Objects needed on each instance:
- `type=endpoint` (every incoming request must map to an endpoint).
- `type=outbound-publish` with `server_uri` and `event=asterisk-devicestate` or `event=asterisk-mwi`.
- `type=inbound-publication` with `event_asterisk-devicestate=<name>` and `event_asterisk-mwi=<name>`.
- `type=asterisk-publication` with `devicestate_publish`, `mailboxstate_publish`, `device_state=yes`, `mailbox_state=yes`.
- optionally an `auth` object.

In the page's two-instance example, each side has an endpoint named after the other instance, and the `server_uri` uses the local instance name as the resource, e.g. `sip:instance1@172.16.10.2`. With no filters, all state is published.

Filtering: regular expressions on the device or mailbox, set as `@device_state_filter` and `@mailbox_state_filter` on publish types, with equivalents on `asterisk-publication`.

The page presents it as an alternative to the older res_xmpp and res_corosync approaches.

## Checked

2026-11-09. Confirmed against the Asterisk page on exchanging device and mailbox state using PJSIP: required objects, example server_uri resource naming, filter option names on publish and asterisk-publication types. Softened the claim that it replaces res_xmpp and res_corosync.
Method: documentation only; no commands were run.
