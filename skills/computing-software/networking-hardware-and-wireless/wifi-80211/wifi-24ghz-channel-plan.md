---
id: computing-software.networking-hardware-and-wireless.wifi-80211.wifi-24ghz-channel-plan
name: wifi-24ghz-channel-plan
category: computing-software
field: networking-hardware-and-wireless
product: wifi-80211
tags: [wifi-24ghz-channels, co-channel-interference, non-overlapping-channels, wifi-bands-channels]
level: practitioner
status: draft
description: "Choose 2.4 GHz channels 1, 6 and 11, use 20 MHz width and reduce power to limit co-channel interference."
sources:
  - https://www.ieee802.org/11/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# 2.4 GHz channel plan

- Channels are 5 MHz apart but a 20 MHz signal spans about four. In the Americas the non-overlapping set is 1, 6, 11; where channels up to 13 are legal, 1/5/9/13 is sometimes used.
- Use 20 MHz on 2.4 GHz in enterprise; 40 MHz leaves room for only one non-overlapping channel.
- Treat 2.4 GHz as a coverage/IoT band: disable it on some APs (for example every second or third) or lower its transmit power.
- Adjacent-channel interference (an AP on 3 next to one on 6) is worse than co-channel, because frames cannot be decoded and deferred to.
- Non-Wi-Fi interferers (Bluetooth, microwave ovens, ZigBee, cordless phones) live here; identify them with a spectrum analyser.

## Verify
- [ ] Controller channel report shows only the chosen set (1/6/11) in use.
- [ ] A survey shows neighbour AP counts per channel are balanced.
