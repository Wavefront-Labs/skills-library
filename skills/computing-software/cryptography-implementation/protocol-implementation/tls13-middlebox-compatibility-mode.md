---
id: computing-software.cryptography-implementation.protocol-implementation.tls13-middlebox-compatibility-mode
name: tls13-middlebox-compatibility-mode
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [protocol-implementation, cryptography-implementation, middlebox-compatibility, tls-1-3, change-cipher-spec, legacy-session-id, supported-versions, middleboxes, rfc-8446]
level: advanced
status: docs-checked
description: "Understand and debug TLS 1.3 middlebox compatibility mode: legacy_session_id, dummy ChangeCipherSpec, version fields, and how to handle the records."
sources: ["https://www.rfc-editor.org/rfc/rfc8446"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TLS 1.3 middlebox compatibility mode

Field measurements cited by RFC 8446 found many middleboxes misbehaving when TLS 1.3 is negotiated. Appendix D.4
makes the TLS 1.3 handshake look like TLS 1.2 session resumption on the wire.

## What it changes
- `legacy_version` in ClientHello and ServerHello stays `0x0303` (TLS 1.2); the real version is in the
  `supported_versions` extension (a ServerHello selecting TLS 1.3 carries 0x0304 there).
- The client always sends a non-empty `legacy_session_id`: a cached pre-1.3 session ID, or a freshly generated 32-byte
  value that should be unpredictable. The server echoes it in `legacy_session_id_echo`.
- Client: a dummy `change_cipher_spec` record immediately before its second flight (right after the first
  ClientHello if offering early data). Server: a dummy `change_cipher_spec` immediately after its first handshake
  message (ServerHello or HelloRetryRequest). If the client sent a non-empty session ID, the server MUST send it.
- Encrypted records use outer content type `application_data` with `legacy_record_version` 0x0303.

## Implementation rules
- Silently drop an unencrypted `change_cipher_spec` record containing the single byte 0x01 received after the first
  ClientHello and before the peer's Finished. Detect it before attempting to deprotect the record, since it may
  arrive where protected records are expected.
- Abort with `unexpected_message` on any other CCS value, on a protected CCS record, or on a CCS before the first
  ClientHello or after the peer's Finished.
- Never rely on record-layer version or legacy fields for negotiation (the record version must be ignored).

## Debugging
- A capture showing a ServerHello with `legacy_version 0x0303` and a CCS is normal TLS 1.3; check
  `supported_versions` in the ServerHello for 0x0304.
- If handshakes fail only through certain networks, suspect an inspection device and compare behaviour with the
  compatibility fields on and off.

## Verify
- [ ] The capture shows TLS 1.3 in the `supported_versions` extension of the ServerHello.
- [ ] Your parser drops a single 0x01 CCS during the handshake and aborts on one outside that window.

## Checked
2026-11-01. Confirmed against RFC 8446: Appendix D.4, section 4.1.2 (legacy_session_id, legacy_version), section 5
(CCS handling and legacy_record_version). Removed: OpenSSL option names, claims about other TLS stacks defaults,
byte-saving remarks, and the statement about QUIC and DTLS (not in this RFC).
Method: documentation only; no commands were run.
