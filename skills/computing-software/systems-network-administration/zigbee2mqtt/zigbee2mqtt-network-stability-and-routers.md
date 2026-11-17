---
id: computing-software.systems-network-administration.zigbee2mqtt.zigbee2mqtt-network-stability-and-routers
name: zigbee2mqtt-network-stability-and-routers
category: computing-software
field: systems-network-administration
product: zigbee2mqtt
tags: [zigbee2mqtt, zigbee-mesh, routers, interference, usb-extension, wifi-coexistence, broadcasts, networkmap, linkquality, coordinator]
level: advanced
status: docs-checked
description: "Improve Zigbee mesh stability under Zigbee2MQTT: adapter choice, USB extension cable, interference, routers, broadcast limits, network map and settling time after heavy changes."
sources: ["https://www.zigbee2mqtt.io/advanced/zigbee/02_improve_network_range_and_stability.html", "https://www.zigbee2mqtt.io/guide/usage/troubleshooting.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Zigbee2MQTT network range and stability

Work down this list:

1. Adapter: use a recommended adapter; CC2530 and CC2531 are known to perform poorly.
2. Placement: use a USB extension cable (even 50 cm, preferably shielded) so the dongle is away from the host's USB 3, HDMI, SSD and Wi-Fi router interference. Try a USB 2 port. Rotating the dongle can change poor `linkquality` and ping failures dramatically.
3. Channel: Wi-Fi shares 2.4 GHz; change the Zigbee `channel` (see the network key and channel skill) away from your Wi-Fi channels.
4. Other 2.4 GHz sources: Bluetooth, wireless gaming dongles, wireless audio transmitters, smart meters, and a still-running Philips Hue hub (put it on another channel or move bulbs to Zigbee2MQTT).
5. Routers: raising `transmit_power` helps the forward path but responses from end devices may still fail; add mains-powered routers (a dedicated router dongle or mains Zigbee devices). Almost all AC-powered devices act as routers (exceptions are most AC relays that need no neutral wire). Some models are poor routers (the docs cite certain SONOFF S26R2ZB versions); AwoX devices are known to cause trouble, and removing them helps.
6. Hardware load: a Raspberry Pi 3 running Home Assistant plus Zigbee2MQTT may be starved of CPU or memory.
7. Broadcasts: Zigbee sustains about one broadcast per second on average; groups, route discovery and Green Power use broadcasts, so use them sparingly.

Diagnose routing with `zigbee2mqtt/bridge/request/networkmap`.

After moving, removing or re-pairing a router, or migrating the coordinator, routes are rebuilt and you may see route errors and slow responses. Leave the network alone to settle: minutes on a good network, up to a few hours otherwise.

## Checked

2026-11-03. Confirmed against the Improve network range and stability and Troubleshooting pages: CC2530/CC2531, USB extension and USB 2 advice, rotation and linkquality, Wi-Fi channel, other 2.4 GHz sources, Hue hub, routers and transmit power, SONOFF S26R2ZB and AwoX notes, Raspberry Pi 3 load, one broadcast per second, networkmap topic, settling time. Removed: ZiGate and ZBOSS status and the named recommended adapter list (not on these pages); router rule restated as the page words it.
Method: documentation only; no commands were run.
