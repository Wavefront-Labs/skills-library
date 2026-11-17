---
id: computing-software.systems-network-administration.wireshark.eap-8021x-wireless-authentication-analysis
name: eap-8021x-wireless-authentication-analysis
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, eap-analysis, 802-1x, peap, eap-tls, eapol, radius, wpa2-enterprise]
level: practitioner
status: docs-checked
description: "Analyse 802.1X logins in Wireshark: EAP Identity, Nak method negotiation, EAP-TLS certificate exchange and alerts, fragmentation, and Success or Failure."
sources:
  - https://www.rfc-editor.org/rfc/rfc3748
  - https://www.rfc-editor.org/rfc/rfc5216
  - https://www.wireshark.org/docs/dfref/e/eap.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EAP / 802.1X wireless authentication analysis

Capture over the air for the client side, and on the authenticator uplink or the authentication
server for the server side. Correlate by time and client MAC.

## Sequence
1. The authenticator typically sends an initial EAP Identity Request, although RFC 3748 says an
   initial Identity Request is not required and MAY be bypassed.
2. The peer answers with its Identity. If it cannot accept the proposed method it replies with a Nak
   (Type 3) naming acceptable methods. A peer must not send a Nak after an initial non-Nak response.
3. Method exchange. For EAP-TLS (Type 13, RFC 5216) the server sends a TLS server certificate message
   (and a certificate_request when it wants client authentication, in which case the peer must also
   send certificate and certificate_verify messages).
4. The authenticator ends with EAP Success (Code 3) or EAP Failure (Code 4). Success and Failure are
   not retransmitted and carry no Type field.
Wireshark's eap dissector exposes `eap.code` and `eap.type` for filtering:
```
eap
eap.code == 4          # failure
eap.code == 3          # success
eap.type == 3          # Nak
eap.type == 13         # EAP-TLS
```

## Reading failures
| Seen | Likely cause |
|---|---|
| Peer sends an EAP-TLS response containing a TLS alert after the server certificate | the peer failed server authentication; RFC 5216 lets the peer send the alert so the server can log the cause, and the server then replies with EAP-Failure |
| Nak listing other types | server and client have no common method |
| Long exchange of many EAP messages with pauses | EAP has no fragmentation of its own; methods fragment, and large certificate chains need as many round trips as there are fragments (RFC 3748) |

## Verify
- [ ] For a failed login you can point to the exact EAP step and which side stopped.

## Checked
Method: docs-checked 2026-11-09 against RFC 3748 (Nak, Success/Failure and fragmentation sections grepped and read), RFC 5216 (TLS exchange and failure handling read) and the Wireshark eap display-filter reference (eap.code and eap.type grepped). Dropped unconfirmed claims: PEAP type number and inner MSCHAPv2 flow, TLS alert numbers, RADIUS filters and reject-code advice, the EAPOL 4-way handshake step, MS-MPPE key delivery, Framed-MTU advice, and the monitor-mode capture details.
