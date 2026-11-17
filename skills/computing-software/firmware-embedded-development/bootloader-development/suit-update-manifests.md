---
id: computing-software.firmware-embedded-development.bootloader-development.suit-update-manifests
name: suit-update-manifests
category: computing-software
field: firmware-embedded-development
product: bootloader-development
tags: [suit-manifest, ab-update, cbor-cose, rfc9019, update-metadata, firmware-embedded-development]
level: sme
status: docs-checked
description: "Describe firmware updates with IETF SUIT manifests (RFC 9019/9124): CBOR/COSE structure, sequence numbers, conditions on vendor/class IDs, payload digests, and tool support."
sources:
  - https://www.rfc-editor.org/rfc/rfc9019
  - https://www.rfc-editor.org/rfc/rfc9124
  - https://datatracker.ietf.org/doc/draft-ietf-suit-manifest/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SUIT update manifests

SUIT (Software Updates for Internet of Things) is the IETF architecture (RFC 9019) and information
model (RFC 9124) for describing an update independently of the transport, with a concrete CBOR
manifest format (draft-ietf-suit-manifest, near-final). 

## What a manifest says
- **Sequence number**: manifests MUST carry monotonically increasing sequence numbers (RFC 9124); devices reject
  manifests with a smaller number than the one already accepted (anti-rollback).
- **Conditions**: vendor ID and class ID the device must match (class IDs are unique within a
  vendor ID scope, RFC 9124), optionally other conditions.
- **Directives**: where to fetch the payload (URI), where to write it (component ID: slot, external
  flash, radio core), how to install (copy, swap), what to invoke (boot).
- **Payload digest and size**: a digest of each image; payload may be integrated in the envelope
  or fetched separately.
- **Authentication**: the manifest is signed (COSE) inside the SUIT envelope; see the current
  draft-ietf-suit-manifest for the algorithms.
Encoding is CBOR.

## Why use it instead of a custom header
- Multi-component updates (application core + network core + external flash assets) in one signed
  description, with dependencies between components.
- Separation of roles: the author signs the manifest, a distributor can add delegation/fetch info.
- Standard tooling and security review; an IETF architecture (RFC 9019) rather than a private format.

## Tooling
- Look for the vendor SDK or an open-source reference implementation of the manifest draft;
  none is covered by the sources of this skill.

## Implementation notes
- Parsing CBOR in a bootloader: use a bounded, well-tested decoder (zcbor, QCBOR, NanoCBOR); fuzz it.
- Store the last accepted sequence number in tamper-resistant storage (OTP counter or secure
  storage), not plain flash.
- Check signatures before acting on any directive.

## Verify
- [ ] Device rejects a manifest with lower sequence number, wrong class ID, or a modified payload.
- [ ] Manifest parser fuzzed (libFuzzer/AFL) without crashes.

## Checked

2026-10-28. Confirmed in RFC 9124: monotonically increasing sequence numbers, devices reject smaller numbers, vendor ID and class ID scoping. RFC 9019 for the architecture; draft-ietf-suit-manifest is the manifest format reference.
Removed: vendor adoption claims (Nordic, RIOT), COSE algorithm names, size estimate, tool and make-target names, the EU CRA claim, and the SHA-256-only wording.

Method: documentation only; no commands were run.
