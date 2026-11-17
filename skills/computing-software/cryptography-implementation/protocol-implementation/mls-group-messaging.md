---
id: computing-software.cryptography-implementation.protocol-implementation.mls-group-messaging
name: mls-group-messaging
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [cryptography-implementation, protocol-implementation, end-to-end-encryption, e2ee, mls-protocol, rfc9420, treekem, group-messaging, delivery-service, openmls]
level: sme
status: docs-checked
description: "Build E2EE group messaging on MLS (RFC 9420): key packages, commits and proposals, epochs, the delivery/authentication services you must supply, and library choices."
sources: ["https://datatracker.ietf.org/doc/html/rfc9420", "https://datatracker.ietf.org/doc/html/rfc9750", "https://openmls.tech/book/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MLS group messaging

Messaging Layer Security (RFC 9420) gives end-to-end encrypted groups with
forward secrecy and post-compromise security. Its ratchet tree lets a sender
encrypt to all members except one with a number of ciphertexts logarithmic in
the group size.

## Core objects

- **KeyPackage**: a member's published, signed bundle of initial keying
  material (init key, credential, supported parameters). Others fetch it to
  add the member; a client that posts one MUST support every parameter in it.
- **Proposals**: add, update, remove, PreSharedKey, ReInit, ExternalInit,
  GroupContextExtensions.
- **Commit**: applies a set of proposals and advances the group to a new
  **epoch**; `Welcome` messages bring new members in.
- **Application messages**: encrypted under keys derived from the epoch's
  secrets.

## What you must build around MLS (RFC 9750 architecture)

- **Delivery Service (DS)**: stores and delivers initial public key material
  (KeyPackages) and distributes messages between group members. RFC 9750
  discusses ordering: a strongly consistent DS can reject messages that
  conflict, and clients must handle the rejection.
- **Authentication Service (AS)**: attests the binding between
  application-level identifiers and the public keys used for authentication,
  and issues and validates credentials. MLS endpoint authentication, and so
  group-key confidentiality, depends on the AS behaving correctly; a malicious
  DS cannot add itself to a group or recover the group key, but may learn
  membership or block group changes.
- **Policy**: who can add or remove members, whether external joins are
  allowed, and how often members refresh their keys (RFC 9750 recommends
  refreshing keying material regularly for forward secrecy).

## Ciphersuites

The mandatory-to-implement suite for MLS 1.0 is
`MLS_128_DHKEMX25519_AES128GCM_SHA256_Ed25519` (Curve25519, AES-128-GCM for
HPKE, HKDF over SHA2-256, Ed25519 signatures); clients MUST implement it.
The registry also lists a P-256 suite with ECDSA signatures. A group changes
parameters, including its cipher suite, by reinitialising through a ReInit
proposal into a completely new group.

## Libraries

OpenMLS is a Rust implementation of RFC 9420 (see its book). Use an existing
library; the state machine is complex.

## Operational issues

- Each device is its own member (its own leaf).
- A client that loses its state needs to rejoin or be re-added.
- Metadata: the DS may learn group membership; add privacy measures if that
  matters.

## Verify

- [ ] The DS has a defined behaviour for conflicting commits in one epoch.
- [ ] Credentials are validated by the AS before Add proposals are accepted.
- [ ] The chosen library interoperates with a second MLS implementation for the chosen suite.

## Checked

2026-11-01. Confirmed against RFC 9420 (mandatory-to-implement suite,
suite 0x0002 P-256, proposal types, ReInit semantics, logarithmic ciphertexts,
KeyPackage parameter rule), RFC 9750 (AS and DS roles, DS ordering and
rejection, malicious-DS limits, regular refresh) and the OpenMLS book (Rust
implementation of RFC 9420). Removed: deployer list (Webex, Wire, Discord,
RCS), O(n) pairwise comparison, mls-rs and MLSpp, test-vector repository
name, "PQ hybrid suites in drafts", and the size-growth note (not in the
sources).
Method: documentation only; no commands were run.
