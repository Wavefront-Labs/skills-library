---
id: engineering-technology.automotive-vehicle-engineering.vehicle-electrical-architecture.uds-diagnostic-services
name: uds-diagnostic-services
category: engineering-technology
field: automotive-vehicle-engineering
product: vehicle-electrical-architecture
tags: [uds-diagnostics, uds, iso-14229, diagnostic-session, security-access, dtc, doip, iso-15765]
level: practitioner
status: gated
description: "Use UDS (ISO 14229) services correctly: sessions, DTC reading, data identifiers, security access, routines, negative responses and transport over CAN and DoIP."
sources:
  - "ISO 14229-1 UDS application layer (https://www.iso.org/standard/72439.html); ISO 15765-4 DoCAN (https://www.iso.org/standard/78384.html)"
  - "python-udsoncan documentation and source (https://udsoncan.readthedocs.io/en/latest/udsoncan/services.html)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# UDS diagnostic services

1. Request/response: service ID byte + parameters; positive response = SID + 0x40; negative response `0x7F <SID> <NRC>`.
2. Common services: `0x10` DiagnosticSessionControl (default, extended, programming), `0x11` ECUReset, `0x14` ClearDiagnosticInformation, `0x19` ReadDTCInformation, `0x22` ReadDataByIdentifier, `0x27` SecurityAccess (seed/key), `0x28` CommunicationControl, `0x2E` WriteDataByIdentifier, `0x31` RoutineControl, `0x34/0x36/0x37` download (request, transfer data, exit) for flashing, `0x3E` TesterPresent, `0x85` ControlDTCSetting.
3. Typical NRCs: `0x12` sub-function not supported, `0x13` incorrect message length, `0x22` conditions not correct, `0x31` request out of range, `0x33` security access denied, `0x35` invalid key, `0x78` response pending (extend timeouts, do not resend).
4. Session flow for flashing: extended session -> disable DTC setting and communication -> programming session -> security access -> download -> check -> reset.
5. Transport: ISO-TP (ISO 15765-2 (gated: unconfirmed, source is paywalled or blocked)) on CAN with single and multi-frame segmentation and flow control; DoIP (ISO 13400 (gated: unconfirmed, source is paywalled or blocked)) over Ethernet with vehicle announcement and routing activation.
6. DTC format: three-byte code plus status byte (test failed, confirmed, pending, etc.); status mask semantics (gated: unconfirmed, source is paywalled or blocked).
7. Tools: a diagnostic tester, trace logging (CANoe, Wireshark for DoIP), and scripting libraries.

**Gotchas:** tester-present timing; P2/P2* server timing; security-access algorithm secrecy.

## Verify
- [ ] Trace of the session shows expected positive responses and handles 0x78.
- [ ] DTC status byte interpreted correctly against the ECU's documentation.
