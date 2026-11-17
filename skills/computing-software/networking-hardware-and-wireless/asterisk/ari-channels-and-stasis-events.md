---
id: computing-software.networking-hardware-and-wireless.asterisk.ari-channels-and-stasis-events
name: ari-channels-and-stasis-events
category: computing-software
field: networking-hardware-and-wireless
product: asterisk
tags: [networking-hardware-and-wireless, asterisk, ari, channels, stasis, stasisstart, local-channel, subscription, uniqueid]
level: practitioner
status: docs-checked
description: "Understand ARI channels, UniqueID versus channel name, Local channel pairs, StasisStart and StasisEnd events, and the three ways an application gets events about a resource."
sources:
  - https://docs.asterisk.org/Configuration/Interfaces/Asterisk-REST-Interface-ARI/Introduction-to-ARI-and-Channels/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ARI channels and Stasis events
A channel is the path of signalling and media between an endpoint and Asterisk. Each has a **UniqueID** (a handle for its whole life, which the ARI client may supply, otherwise Asterisk assigns it) and a **Name** such as `PJSIP/Alice-00000001`. ARI operations use the UniqueID.

**Local channels** are internal and always come in pairs: `Local/myapp@default-00000000;1` and `;2`, with a virtual endpoint forwarding media between the halves. Creating one always creates both.

Channels reach ARI through the `Stasis` dialplan application. It hands control to the client and raises a `StasisStart` event; leaving raises `StasisEnd`.

Resources do not send events by default. An application receives events only when:
1. the resource is a channel that entered its Stasis application (implicit subscription, removed when it leaves);
2. a channel in Stasis interacts with another resource such as a bridge (subscription lasts while it interacts);
3. the application explicitly subscribes through the applications operations (the application owns it while the resource exists).

`GET /channels` lists existing channels. The page example uses ari-py with `ari.connect('http://localhost:8088', ...)` and `on_channel_event('StasisStart', ...)`.

## Checked
2026-11-09: read the cited Introduction to ARI and Channels page in full and confirmed UniqueID versus name, Local channel pairs and names, StasisStart and StasisEnd, the three subscription routes, GET /channels and the ari-py example. Nothing removed; every claim was confirmed.

Method: documentation only; no commands were run.
