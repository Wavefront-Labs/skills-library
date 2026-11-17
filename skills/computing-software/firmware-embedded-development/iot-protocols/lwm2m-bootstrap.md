---
id: computing-software.firmware-embedded-development.iot-protocols.lwm2m-bootstrap
name: lwm2m-bootstrap
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [lwm2m-bootstrap, lwm2m-operations, lwm2m, bootstrap, security-object, iot-protocols]
level: practitioner
status: docs-checked
description: "LwM2M bootstrap: Provision server credentials onto a device at first boot."
sources:
  - https://www.openmobilealliance.org/release/LightweightM2M/V1_1_1-20190617-A/OMA-TS-LightweightM2M_Core-V1_1_1-20190617-A.pdf
  - https://www.openmobilealliance.org/release/LightweightM2M/V1_1_1-20190617-A/OMA-TS-LightweightM2M_Transport-V1_1_1-20190617-A.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LwM2M bootstrap

**Goal:** Provision server credentials onto a device at first boot.

## Steps
1. Four modes exist: Factory Bootstrap, Bootstrap from Smartcard, Client Initiated Bootstrap and Server Initiated Bootstrap (which triggers the client-initiated one)
2. Client initiated needs a Bootstrap-Server Account preloaded in the client, with DTLS/TLS and/or OSCORE credentials; the client sends `POST /bs?ep={Endpoint Client Name}` (optionally `&pct=` for content format)
3. The bootstrap server then sends Bootstrap-Write, Bootstrap-Delete, Bootstrap-Discover and Bootstrap-Read as needed, and must end with Bootstrap-Finish, a `POST /bs` with empty payload
4. Bootstrap-Delete may target `/` to delete all object instances except the Bootstrap-Server Account
5. Security object (ID 0) resource 2, Security Mode: 0 Pre-Shared Key, 1 Raw Public Key, 2 Certificate, 3 NoSec, 4 Certificate with EST; resource 1 marks the instance as the Bootstrap-Server
6. The client answers Bootstrap-Finish with 2.04 Changed when the loaded configuration is consistent
7. Unique high-entropy keys per device should be used for the Bootstrap-Server Account

## Gotcha
If no Bootstrap-Finish arrives within EXCHANGE_LIFETIME (RFC 7252), the bootstrap has failed and the Bootstrap-Server Account keeps its previous values. If the Account has to be replaced, the new one must be in place before the Finish response, otherwise the client returns Not Acceptable.

## Verify
- [ ] Device ends with correct /0 and /1
- [ ] Bootstrap-Finish received
- [ ] Failed bootstrap leaves the old Bootstrap-Server Account intact

## Checked

2026-11-03. Confirmed in the OMA LightweightM2M 1.1.1 Core spec (section 6.1.3, Appendix E.1 Security object, Appendix F example) and Transport spec (section 6.4.2): bootstrap modes, `/bs?ep=` and Bootstrap-Finish mapping, delete of `/`, security mode values 0 to 4, the EXCHANGE_LIFETIME failure rule, per-device key recommendation. Removed: the claim that a NoSec bootstrap leaks credentials (not stated), the "retries with backoff" check (not specified), and the claim that the Server object is written as `/1` by rule (the spec only says the server configures Bootstrap Information with Write and Delete).
Method: documentation only; no commands were run.
