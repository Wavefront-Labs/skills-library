---
id: computing-software.firmware-embedded-development.iot-protocols.senml-payload
name: senml-payload
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [senml-payload, iot-payloads, senml, rfc8428, base-name, content-format, iot-protocols]
level: practitioner
status: docs-checked
description: "SenML payload format: Send sensor measurements in a standard format."
sources:
  - https://www.rfc-editor.org/rfc/rfc8428
  - https://www.rfc-editor.org/rfc/rfc8949
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SenML payload format

**Goal:** Send sensor measurements in a standard format.

## Steps
1. A SenML Pack is a JSON array of records using labels: bn base name, bt base time, bu base unit, n name, u unit, v value, vs string value, vb boolean value, t time (also bv, bs, bver, vd, s, ut)
2. Example `[{"bn":"urn:dev:mac:0024befffe804ff1/","n":"temp","u":"Cel","v":22.5}]`
3. Base fields apply to the record that carries them and to following records until changed; the Name is concatenated to the Base Name, and the Base Time is added to the Time
4. Units come from the IANA SenML Units registry, for example Cel (degrees Celsius), m (meter), V (volt)
5. In CBOR (application/senml+cbor) base fields use negative integer labels (bn -2, bt -3, bu -4) and the others non-negative ones (n 0, u 1, v 2, vs 3, vb 4)
6. CoAP Content-Format IDs: 110 for application/senml+json and 112 for application/senml+cbor

## Gotcha
A missing Base Time or Time counts as zero, and values below 2**28 mean seconds relative to "now" (zero means the sensor does not know the absolute time). A device with no clock can therefore send relative times and let the receiver apply its own receipt time. Take care that Base Time plus Time does not accidentally reach 2**28, which turns it into an absolute time.

## Verify
- [ ] Parser accepts the sample
- [ ] Base values resolve
- [ ] Units come from the registry

## Checked

2026-11-03. Confirmed in RFC 8428: label table including CBOR labels, Base Name and Base Time resolution, relative versus absolute time rules, the units registry entries Cel, m and V, and CoAP Content-Format IDs 110 and 112. Removed: the claim that LwM2M uses SenML (not stated in RFC 8428).
Method: documentation only; no commands were run.
