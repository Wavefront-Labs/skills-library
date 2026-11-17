---
id: computing-software.systems-network-administration.zigbee2mqtt.zigbee2mqtt-serial-adapter-settings
name: zigbee2mqtt-serial-adapter-settings
category: computing-software
field: systems-network-administration
product: zigbee2mqtt
tags: [zigbee2mqtt, serial, adapter, zstack, ember, deconz, zigate, zboss, mdns, transmit-power, usb-adapter]
level: practitioner
status: docs-checked
description: "Configure the Zigbee2MQTT serial section: find the adapter port, pick the adapter driver, use network or mDNS adapters, and tune baudrate, rtscts and transmit_power."
sources: ["https://www.zigbee2mqtt.io/guide/configuration/adapter-settings.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Zigbee2MQTT serial and adapter settings

Zigbee2MQTT normally auto-detects a USB adapter. If startup fails with `USB adapter discovery error (No valid USB adapter found). Specify valid 'adapter' and 'port' in your configuration.`, add a `serial` section to `configuration.yaml`.

1. Find the port. Linux USB: `ls -l /dev/serial/by-id` and use the `/dev/serial/by-id` path shown there. Network adapters: use a static IP (reserve it on the router). Some adapters (the docs name ZigStar) default to network mode and will not talk over USB until put in USB mode.
2. Pick `adapter` from its adapter page: `zstack`, `ember`, `deconz`, `zigate` or `zboss`.

```yaml
serial:
    port: /dev/serial/by-id/usb-Texas_Instruments_TI_CC2531_USB_CDC___0X00124B0018ED3DDF-if00
    adapter: zstack
# network adapter: port: tcp://192.168.1.12:6638
```

Optional serial keys: `baudrate` (115200 for Z-Stack and EZSP, 38400 for deCONZ; some EZSP firmware needs 57600), `rtscts` (hardware flow control, default false), `disable_led`.

mDNS discovery: `port: mdns://slzb-06` (tested service types: `slzb-06`, `uzg-01`, `czc`). With mDNS the `adapter` and `baudrate` keys are ignored, and if two adapters advertise the same service type Zigbee2MQTT connects to a random one, so use an explicit IP and port instead.

Under `advanced`: `transmit_power` (dBm, default 5; CC2652R/RB max is 5, CC2652P and CC1352P-2 reach 20; firmware may cap it), `adapter_concurrent` (null uses the recommended value, e.g. 2 for CC2531), `adapter_delay` (Conbee/RaspBee only, try 200 on problems).

Not every feature works on every adapter; check the adapter's own page. USB adapters can be exposed over TCP as a remote adapter.

## Checked

2026-11-03. Confirmed against the Adapter settings page: discovery error text, port discovery, static IP for network adapters, adapter values, baudrate defaults, rtscts, disable_led, mDNS service types and ignored keys, transmit_power, adapter_concurrent, adapter_delay. Removed: the unverified startup-log verify line and the claim that by-id is preferred over ttyACM0 (the page only shows by-id).
Method: documentation only; no commands were run.
