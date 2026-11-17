---
id: computing-software.networking-hardware-and-wireless.asterisk.pjsip-presence-and-extension-state
name: pjsip-presence-and-extension-state
category: computing-software
field: networking-hardware-and-wireless
product: asterisk
tags: [networking-hardware-and-wireless, asterisk, pjsip, presence, blf, hint, subscribe, publish, extension-state, outbound-publish]
level: practitioner
status: docs-checked
description: "Provide BLF and presence over PJSIP: dialplan hints, allow_subscribe, required res_pjsip modules, and publishing extension state with outbound-publish."
sources:
  - https://docs.asterisk.org/Configuration/Channel-Drivers/SIP/Configuring-res_pjsip/Configuring-res_pjsip-for-Presence-Subscriptions/
  - https://docs.asterisk.org/Configuration/Channel-Drivers/SIP/Configuring-res_pjsip/Publishing-Extension-State/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pjsip presence and extension state
Subscriptions: PJSIP supports RFC 3856 presence and RFC 4235 dialog info, as chan_sip did. Associate an extension with a device using a hint in `extensions.conf`: `exten => 1000,hint,PJSIP/alice`.

Endpoint options: `allow_subscribe` (enabled by default) and `context`.

Modules: `res_pjsip`, `res_pjsip_pubsub`, `res_pjsip_exten_state` (presence and dialog events), `res_pjsip_pidf_body_generator` and `res_pjsip_xpidf_body_generator` (presence bodies), `res_pjsip_dialog_info_body_generator` (dialog event). Add a custom presence state to a hint with `exten => 1000,hint,PJSIP/alice,CustomPresence:alice`, which needs `res_pjsip_pidf_digium_body_supplement`.

Publishing: instead of each device subscribing to Asterisk, a `type=outbound-publish` section sends one PUBLISH per change to an event state compositor. Required options: `multi_user=yes` and `@body` (application/dialog-info+xml, application/pidf+xml, application/xpidf+xml or application/cpim-pidf+xml). Optional regular-expression filters `@context` and `@exten`, for example `@context=^users`, `@exten=^1000`. Several publish sections are allowed if names differ.

## Checked

2026-11-09. Confirmed against the Asterisk presence subscriptions and Publishing Extension State pages: hint syntax, allow_subscribe, module list, CustomPresence module, outbound-publish options and body types. Narrowed the required options to the two the page states as required; its examples also set server_uri, from_uri and event.
Method: documentation only; no commands were run.
