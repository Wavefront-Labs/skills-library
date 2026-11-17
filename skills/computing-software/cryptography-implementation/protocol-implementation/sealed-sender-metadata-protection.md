---
id: computing-software.cryptography-implementation.protocol-implementation.sealed-sender-metadata-protection
name: sealed-sender-metadata-protection
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [protocol-implementation, cryptography-implementation, sealed-sender, metadata-protection, e2ee, signal-protocol, sender-certificate]
level: sme
status: docs-checked
description: "Hide sender identity from the messaging server with sealed sender: sender certificates, delivery tokens for abuse control, and residual metadata leaks to address."
sources: ["https://signal.org/blog/sealed-sender/", "https://www.ndss-symposium.org/ndss-paper/improving-signals-sealed-sender/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sealed sender metadata protection

## Mechanism (Signal)
1. Clients periodically retrieve a short-lived **sender certificate** from the service attesting to their identity;
   in Signal's 2018 design it contains the phone number, public identity key and an expiration timestamp.
2. The sender encrypts the message with the Signal Protocol as usual, includes the sender certificate in an envelope,
   encrypts the envelope to the recipient, and hands it to the service without authenticating, along with the
   recipient's delivery token. The service sees the destination, not the sender.
3. The recipient decrypts the envelope and validates that the identity key used to encrypt the envelope matches the
   sender certificate (and the certificate's validity).
4. Abuse control: clients derive a 96-bit **delivery token** from their profile key and register it with the
   service, which requires proof of the token to accept sealed sender messages for that user. Only people with the
   profile key can derive it, which restricts sealed sender to contacts by default.

## Residual leaks
- Signal's announcement lists resistance to traffic correlation via timing attacks and IP addresses as ongoing
  work, so treat both as leaks.
- Delivery receipts and replies create sender-recipient correlations over time: the NDSS paper "Improving Signal's
  Sealed Sender" describes a statistical disclosure attack made effective by delivery receipts, linking users in as
  few as 5 messages in its models, even for users on Tor or VPNs, and proposes mitigations.

## Implementation notes
- Sender certificates must be short-lived and checked for expiry.
- Validate that the identity key used for the envelope matches the certificate.
- Signal offered an optional setting to accept sealed sender messages from non-contacts, at increased risk of
  abuse; leave it off unless you can bear the abuse.

## Verify
- [ ] Server logs for sealed messages contain no sender identifiers; forged certificate tests fail at recipients.

## Checked

2026-11-01. Confirmed against Signal's sealed sender announcement (sender certificate contents, delivery tokens from
the profile key, 96-bit size, unauthenticated send with the token, recipient validation, optional non-contact setting,
timing and IP work ongoing) and the NDSS paper abstract (statistical disclosure attack, delivery receipts, as few as
5 messages, Tor and VPN users). Removed: server key signature detail, "hours to days" lifetime, the 2021 date, the
ephemeral-identity mitigation, and the group, contact discovery and push metadata claims (not in the sources).
Method: documentation only; no commands were run.
