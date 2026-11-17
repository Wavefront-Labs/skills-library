---
id: computing-software.networking-hardware-and-wireless.asterisk.ari-bridges
name: ari-bridges
category: computing-software
field: networking-hardware-and-wireless
product: asterisk
tags: [networking-hardware-and-wireless, asterisk, ari, bridges, mixing, holding, dtmf-events, proxy-media, announcer, subscription]
level: practitioner
status: docs-checked
description: "Create ARI bridges with mixing or holding types, understand dtmf_events and proxy_media, participant versus announcer roles, and why bridge events need an explicit subscription."
sources:
  - https://docs.asterisk.org/Configuration/Interfaces/Asterisk-REST-Interface-ARI/Introduction-to-ARI-and-Bridges/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ARI bridges
A bridge is a container for channels that passes media between them or plays media to them.

Attributes when creating a bridge:
- `mixing`: media passes between all channels. Cannot be combined with `holding`.
- `dtmf_events`: decode media in Asterisk so DTMF is recognised; without it DTMF events may not be raised because media can flow directly. Only affects `mixing`.
- `proxy_media`: media always goes through Asterisk even if clients could exchange it directly. Only affects `mixing`.
- `holding`: channels are entertained with media. A channel is a participant or an announcer. Participants do not share media with each other; an announcer's media is played to all participants.

Asterisk picks the most performant mixing technology compatible with the channel types and chosen attributes.

**Subscription:** unlike channels, bridges are not automatically subscribed to. Subscribe through `POST /applications/{app_name}/subscription` to get bridge events.

The page's example creates a holding bridge if none exists, adds each channel entering `Stasis(bridge-hold)` to it and starts music on hold on the bridge. Events about channels entering and leaving bridges arrive without a bridge subscription.

## Checked

2026-11-09. Confirmed against the Asterisk Introduction to ARI and Bridges page: mixing, dtmf_events, proxy_media and holding attributes, participant and announcer roles, the subscription operation and the bridge-hold example. Replaced the claim about sub-pages (not stated on the page) with the page's note that channel enter and leave events need no bridge subscription.
Method: documentation only; no commands were run.
