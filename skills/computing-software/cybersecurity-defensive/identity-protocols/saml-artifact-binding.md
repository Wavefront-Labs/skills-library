---
id: computing-software.cybersecurity-defensive.identity-protocols.saml-artifact-binding
name: saml-artifact-binding
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [saml-artifact-binding, saml-bindings, artifact, samlart, artifactresolve, soap, back-channel, identity-protocols]
level: advanced
status: docs-checked
description: "Use the artifact binding to pass a small reference through the browser and resolve the message back-channel over SOAP, with its trust and timing rules."
sources:
  - https://docs.oasis-open.org/security/saml/v2.0/saml-bindings-2.0-os.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HTTP Artifact binding and ArtifactResolve

Goal: keep assertions off the browser.

Method: the issuer sends the browser a `SAMLart` parameter (URL query string with GET, or a hidden form control with POST; endpoints must support both). Type code 0x0004 is B64 of a 2-byte type code, 2-byte EndpointIndex, 20-byte SourceID (SHA-1 hash of the issuer's identification URL, not hex-encoded) and 20-byte MessageHandle (cryptographically strong random value of at least 16 bytes, padded to 20). The receiver finds the issuer by SourceID and the responder location by EndpointIndex (metadata can be used for this), then sends `samlp:ArtifactResolve` over a synchronous binding such as SOAP and receives `ArtifactResponse` containing the message.

Gotchas:
- All artifacts must have single-use semantics enforced by the issuer; receivers are recommended to enforce it too, and an artifact whose resolution fails should be blocked for a while.
- A direct path must exist from the receiver back to the issuer for the ArtifactResolve call, and the issuer must keep state while the artifact is pending, which matters in load-balanced environments.
- The callback may be mutually authenticated and integrity protected depending on the environment; if the message is meant for a specific recipient, the issuer must authenticate the ArtifactResolve sender first. Sending the artifact to and from the browser should be protected with TLS.
- An issuer that understands an ArtifactResolve must answer with an ArtifactResponse with status Success even if it does not return the message (for example the requester is not authorised or the artifact is no longer valid).

Verify: resolve the same artifact twice and confirm the second fails.

## Checked
Method: 2026-11-09 documentation only; no commands were run. Converted SAML V2.0 Bindings to text and read section 3.6 (HTTP Artifact binding: overview, message encoding, artifact format and type 0x0004, security considerations, error reporting, metadata). Removed the seconds-long lifetime, the firewall remark, the mutual-TLS-required-in-practice claim and the SaaS support remark (not stated).
