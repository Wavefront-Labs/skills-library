---
id: computing-software.firmware-embedded-development.iot-protocols.coap-resource-discovery-link-format
name: coap-resource-discovery-link-format
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [coap-resource-discovery-link-format, coap-blockwise, coap, link-format, well-known-core, iot-protocols]
level: practitioner
status: docs-checked
description: "CoAP resource discovery: Discover resources on a device."
sources:
  - https://www.rfc-editor.org/rfc/rfc6690
  - https://www.rfc-editor.org/rfc/rfc7252
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CoAP resource discovery

**Goal:** Discover resources on a device.

## Steps
1. GET coap://host/.well-known/core returns application/link-format (Content-Format 40)
2. Entries like </sensors/temp>;rt="temperature";if="sensor";ct=0;obs
3. Filter with query ?rt=temperature
4. Attributes: rt resource type, if interface, sz size, ct content format
5. Multicast discovery goes to the All CoAP Nodes address: IPv4 224.0.1.187 or IPv6 FF0X::FD (link-local and site-local scopes are the ones CoAP needs, e.g. FF02::FD)

## Gotcha
Multicast requests must be Non-confirmable, and responders apply a leisure delay so many nodes do not answer at once (RFC 7252 section 8).

## Verify
- [ ] core lists all resources
- [ ] Query filter works
- [ ] Multicast request is Non-confirmable

## Checked

2026-11-03. Confirmed in RFC 6690 and RFC 7252: /.well-known/core, Content-Format 40, rt, if, sz, ct and obs attributes, the rt query filter, All CoAP Nodes addresses, NON multicast requests and leisure. Removed: the resource directory (RFC 9176) step, whose RFC was not read.
Method: documentation only; no commands were run.
